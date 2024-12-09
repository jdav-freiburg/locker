from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable


class Db(ABC):

    @abstractmethod
    def is_empty(self) -> bool: ...
    
    @abstractmethod
    def verify(self, code: str): ...

    @abstractmethod
    def remove(self, index: int): ...

    @abstractmethod
    def get_all(self) -> Iterable[str]: ...
