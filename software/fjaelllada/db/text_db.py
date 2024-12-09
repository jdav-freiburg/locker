from abc import abstractmethod
from contextlib import contextmanager
from filelock import FileLock
from pathlib import Path
from typing import Generator, List, Tuple

from fjaelllada.db import Db


class TextDatabase(Db):
    # *data, (offset_entry, size_entry)
    _entries: List[tuple]
    _path: Path
    _lockfile: Path

    def __init__(self, path: str):
        self._path = Path(path)
        self._lockfile = self._path.with_name(self._path.name + ".lock")
        self._read_file()

    @contextmanager
    def _lock(self):
        lock = FileLock(self._lockfile)
        with lock:
            self._check_update()
            yield
    
    @abstractmethod
    def _reset(self): ...

    @abstractmethod
    def _add_entry(self, fields: Tuple[str]): ...
    
    def _read_file(self):
        self._entries = []
        self._reset()
        if self._path.is_file():
            self._last_changed = self._path.stat().st_mtime_ns
            with open(self._path, 'rb') as rf:
                for line in rf:
                    if not line.strip():
                        continue
                    fields = line.strip().rsplit(b";")
                    fields = [f.decode() for f in fields]
                    entry = (*fields, (rf.tell() - len(line), len(line.rstrip())))
                    self._entries.append(entry)
                    self._add_entry(entry)

    def _check_update(self):
        if self._path.is_file() and self._path.stat().st_mtime_ns > self._last_changed:
            self._read_file()

    def is_empty(self) -> bool:
        with self._lock():
            return len(self._entries) == 0

    def _register(self, fields: Tuple[str, ...]) -> None:
        with self._lock():
            entry_raw = (";".join(fields) + "\n").encode()
            with open(self._path, 'ab') as wf:    
                entry_offset = wf.tell()
                wf.write(entry_raw)
                wf.flush()
            self._entries.append((*fields, (entry_offset, len(entry_raw) - 1)))
            self._add_entry(fields)

    @abstractmethod
    def _remove(self, index: int, fields: Tuple[str, ...]): ...

    def remove(self, index: int):
        # This must be fetched before updating
        *fields, (entry_offset, entry_size) = self._entries[index]
        with self._lock():
            print(f"Remove {index}")
            del self._entries[index]
            with open(self._path, 'rb+') as wf:
                wf.seek(entry_offset)
                # Blank out the entry
                wf.write(b" " * entry_size)
                wf.flush()
            self._remove(index, fields)

    def _get_all(self) -> Generator[Tuple[str, ...], None, None]:
        with self._lock():
            for *data, _offs in self._entries:
                yield data
