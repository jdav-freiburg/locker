from pathlib import Path
from typing import Generator, Tuple, cast, Optional, List

import pyotp


from fjaelllada.db.text_db import TextDatabase
from fjaelllada.env import TOTP_ISSUER

valid_window = 1


class TotpDatabase(TextDatabase):
    _totp_entries: List[pyotp.TOTP]
    _path: Path
    _lockfile: Path

    def __init__(self, path: str):
        super().__init__(path)
    
    def _reset(self):
        self._totp_entries = []
    
    def _add_entry(self, fields: Tuple[str]):
        self._totp_entries.append(cast(pyotp.TOTP, pyotp.parse_uri(fields[0])))

    def register(self, provisioning_uri: str, verification_code: Optional[str] = None) -> bool:
        totp = cast(pyotp.TOTP, pyotp.parse_uri(provisioning_uri))
        if verification_code is not None:
            if not totp.verify(verification_code, valid_window=valid_window):
                return False
        self._register((provisioning_uri,))
        return True

    def verify(self, code: str) -> Optional[str]:
        with self._lock():
            for entry in self._totp_entries:
                if entry.verify(code, valid_window=valid_window):
                    return entry.name
            #return False or code == "000000"
            return None

    def _remove(self, index: int, fields: Tuple[str, ...]):
        del self._totp_entries[index]

    def get_all(self) -> Generator[str, None, None]:
        with self._lock():
            for totp in self._totp_entries:
                yield totp.name

    @staticmethod
    def new_uri(username: str) -> str:
        return pyotp.TOTP(pyotp.random_base32(), name=username, issuer=TOTP_ISSUER).provisioning_uri()
