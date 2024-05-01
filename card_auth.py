from datetime import datetime, timezone
import os.path
from typing import Generator, List, Tuple


def now_timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_to_localtz(timestamp: str) -> datetime:
    timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    timestamp_dt = timestamp_dt.replace(tzinfo=timezone.utc)
    return datetime.fromtimestamp(timestamp_dt.timestamp())


class CardDatabase:
    # key, name, last_login, (offset_last_login, size_last_login), (offset_entry, size_entry)
    _entries: List[Tuple[bytes, bytes, bytes, Tuple[int, int], Tuple[int, int]]]

    def __init__(self, path: str):
        self._f = open(path, 'rb+')
        if os.path.isfile(path):
            self._entries = []
            for line in self._f:
                if not line.strip():
                    continue
                key, name, last_login = line.strip().rsplit(b";", 2)
                date_offset = self._f.tell() - len(line) + line.rindex(b';') + 1
                self._entries.append((key, name, last_login, (date_offset, len(last_login)), (self._f.tell() - len(line), len(line.rstrip()))))
        else:
            self._entries = []

    def is_empty(self) -> bool:
        return len(self._entries) == 0

    def register(self, key: str, name: str) -> None:
        last_login = now_timestamp()
        entry_offset = self._f.tell()
        entry_raw = (key + ";" + name + ";" + last_login + "\n").encode()
        self._f.write(entry_raw)
        self._f.flush()
        last_login_offset = self._f.tell() - len(last_login) - 1
        self._entries.append((key.encode(), name.encode(), last_login.encode(), (last_login_offset, len(last_login)), (entry_offset, len(entry_raw) - 1)))

    def verify(self, code: str):
        code_b = code.encode()
        for idx, (key, *_) in enumerate(self._entries):
            if key == code_b:
                key, name, timestamp, (timestamp_offset, timestamp_size), entry_offsets = self._entries[idx]
                timestamp = now_timestamp().encode()
                self._entries[idx] = (key, name, timestamp, (timestamp_offset, timestamp_size), entry_offsets)
                if timestamp_size == len(timestamp):
                    self._f.seek(timestamp_offset)
                    self._f.write(timestamp)
                    self._f.seek(0, 2)
                return True
        return False
    
    def remove(self, index: int):
        print(f"Remove {index}")
        entry_offset, entry_size = self._entries[index][4]
        del self._entries[index]
        self._f.seek(entry_offset)
        # Blank out the entry
        self._f.write(b" " * entry_size)
        self._f.flush()
        self._f.seek(0, 2)
    
    def get_all(self) -> Generator[Tuple[str, datetime], None, None]:
        for _, name, last_login, *_ in self._entries:
            yield name.decode(), timestamp_to_localtz(last_login.decode())


db = CardDatabase('card_db.txt')


def check_code(code: str) -> bool:
    return db.verify(code)


def register(code: str, name: str):
    db.register(code, name)
