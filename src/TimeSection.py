from dataclasses import astuple, dataclass
from PyQt6.QtGui import  QColor

@dataclass
class TimeSection:
    name:str
    duration:int
    color: QColor
    def __iter__(self):
        return iter(astuple(self))
    
    def __getitem__(self, keys):
        return iter(getattr(self, k) for k in keys)
