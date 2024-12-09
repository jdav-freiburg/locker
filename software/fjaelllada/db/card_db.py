from typing import Dict, Generator, Optional, Tuple

from fjaelllada.db.text_db import TextDatabase


class CardDatabase(TextDatabase):
    # key, name, (offset_entry, size_entry)
    _entries_by_key: Dict[str, Tuple[str, str, Tuple[int, int]]]

    def __init__(self, path: str):
        super().__init__(path)

    def _reset(self):
        self._entries_by_key = {}
    
    def _add_entry(self, fields: Tuple[str, str]):
        self._entries_by_key[fields[0]] = fields

    def register(self, key: str, name: str) -> None:
        self._register((key, name))
    
    def verify(self, code: str) -> Optional[str]:
        with self._lock():
            entry = self._entries_by_key.get(code)
            if entry is None:
                return None
            return entry[1]
    
    def _remove(self, index: int, fields: Tuple[str, ...]):
        del self._entries_by_key[fields[0]]
    
    def get_all(self) -> Generator[str, None, None]:
        for _, name in self._get_all():
            yield name
