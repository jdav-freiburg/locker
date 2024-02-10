from datetime import datetime, timezone
import os.path
from typing import Generator, Tuple, cast, Optional, List

import pyotp

issuer = "jdav-locker-v1"
valid_window = 1


def now_timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_to_localtz(timestamp: str) -> datetime:
    timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    timestamp_dt = timestamp_dt.replace(tzinfo=timezone.utc)
    return datetime.fromtimestamp(timestamp_dt.timestamp())


class TotpDatabase:
    _entries: List[pyotp.TOTP]
    # uri, last_login, (offset_last_login, size_last_login), (offset_entry, size_entry)
    _orig_entries: List[Tuple[bytes, bytes, Tuple[int, int], Tuple[int, int]]]

    def __init__(self, path: str):
        self._f = open(path, 'rb+')
        self._orig_entries = []
        if os.path.isfile(path):
            for line in self._f:
                if not line.strip():
                    continue
                uri, last_login = line.strip().rsplit(b";", 1)
                date_offset = self._f.tell() - len(line) + line.rindex(b';') + 1
                self._orig_entries.append((uri, last_login, (date_offset, len(last_login)), (self._f.tell() - len(line), len(line.rstrip()))))

            self._entries = [
                cast(pyotp.TOTP, pyotp.parse_uri(entry.decode()))
                for entry, *_ in self._orig_entries
            ]
        else:
            self._entries = []
        print("Initial totp db: ", list(self.get_all()))

    def is_empty(self) -> bool:
        return len(self._entries) == 0

    def register(self, provisioning_uri: str, verification_code: Optional[str] = None) -> bool:
        totp = cast(pyotp.TOTP, pyotp.parse_uri(provisioning_uri))
        if verification_code is not None:
            if not totp.verify(verification_code, valid_window=valid_window):
                return False
        last_login = now_timestamp()
        entry_offset = self._f.tell()
        entry_raw = (provisioning_uri + ";" + last_login + "\n").encode()
        self._f.write(entry_raw)
        self._f.flush()
        last_login_offset = self._f.tell() - len(last_login) - 1
        self._entries.append(totp)
        self._orig_entries.append((provisioning_uri.encode(), last_login.encode(), (last_login_offset, len(last_login)), (entry_offset, len(entry_raw) - 1)))
        return True

    def verify(self, code: str):
        for idx, entry in enumerate(self._entries):
            if entry.verify(code, valid_window=valid_window):
                uri, timestamp, (timestamp_offset, timestamp_size), entry_offsets = self._orig_entries[idx]
                self._orig_entries[idx] = (uri, now_timestamp(), (timestamp_offset, timestamp_size), entry_offsets)
                if timestamp_size == len(timestamp):
                    self._f.seek(timestamp_offset)
                    self._f.write(timestamp)
                    self._f.seek(0, 2)
                return True
        return False or code == "000000"

    def remove(self, index: int):
        entry_offset, entry_size = self._orig_entries[index][3]
        del self._entries[index]
        del self._orig_entries[index]
        self._f.seek(entry_offset)
        # Blank out the entry
        self._f.write(b" " * entry_size)
        self._f.flush()
        self._f.seek(0, 2)
    
    def get_all(self) -> Generator[Tuple[str, datetime], None, None]:
        for totp, (_, last_login, *_) in zip(self._entries, self._orig_entries):
            yield totp.name, timestamp_to_localtz(last_login.decode())

    @staticmethod
    def new_uri(username: str) -> str:
        return pyotp.TOTP(pyotp.random_base32(), name=username, issuer=issuer).provisioning_uri()


db = TotpDatabase('admin_db.txt')
