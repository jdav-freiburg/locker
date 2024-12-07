from typing import Dict, Generator, Tuple

from fjaelllada.db.text_db import TextDatabase


class CardDatabase(TextDatabase):
    # key, name, (offset_entry, size_entry)
    _entries_by_key: Dict[bytes, Tuple[bytes, bytes, Tuple[int, int]]]

    def __init__(self, path: str):
        super().__init__(path, 2)

    def _reset(self):
        self._entries_by_key = {}
    
    def _add_entry(self, fields: Tuple[str]):
        self._entries_by_key[fields[0]] = fields

    def register(self, key: str, name: str) -> None:
        self._register((key, name))

    def verify(self, code: str):
        with self._lock():
            code_b = code.encode()
            return code_b in self._entries_by_key
    
    def _remove(self, index: int, fields: tuple):
        del self._entries_by_key[fields[0]]
    
    def get_all(self) -> Generator[str, None, None]:
        for _, name in self._get_all():
            yield name
