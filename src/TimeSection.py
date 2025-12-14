from dataclasses import astuple, dataclass
from PyQt6.QtGui import  QColor
from typing import Iterator, Any, Iterable

@dataclass
class TimeSection:
    name: str
    duration: int
    color: QColor
    def __iter__(self) -> Iterator[Any]:
        return iter(astuple(self))
    
    def __getitem__(self, keys: Iterable[str]) -> Iterator[Any]:
        return iter(getattr(self, k) for k in keys)
