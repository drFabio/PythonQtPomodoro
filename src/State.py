from typing import Iterator
import time
from collections import namedtuple
from TimeSection import TimeSection
from PyQt6.QtCore import QObject, pyqtSignal

TimeInfo = namedtuple('TimeInfo', ['ellapsed', 'remaining', 'total','percentage'])

class Status:
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

class State(QObject):
    stop_event = pyqtSignal()
    pause_event = pyqtSignal()
    resume_event = pyqtSignal()
    skip_event = pyqtSignal()
    quit_event = pyqtSignal()

    def __init__(self, intervals: Iterator[TimeSection] = iter([])) -> None:
        super().__init__()
        self.interval: TimeSection | None = None
        # Time elapsed on the current cycle (in seconds)
        self.ellapsed_time: int = 0
        self.start_time: int = 0
        self.stop_time: int = 0
        self.cyles: int = 0
        self.intervals: Iterator[TimeSection] = intervals
        self.status: str = Status.STOPPED
        self.current_interval: TimeSection | None = None

    def start(self):
        interval =  next(self.intervals)
        self.current_interval = interval
        self.resume()
        return interval
    
    def pause(self) -> None:
        info = self.getTime()
        self.ellapsed_time = info.ellapsed
        print(f"Saving ellapsed time ${info.ellapsed}")
        self.status = Status.PAUSED

    def resume(self) -> None:
        self.status = Status.RUNNING
        self.start_time = int(time.time())


    def stop(self):
        self.status = Status.STOPPED

    def getTime(self) -> TimeInfo:
        now = int(time.time()) 
        ellapsed = now - self.start_time  + self.ellapsed_time
        total = self.current_interval.duration
        remaining = total -ellapsed
        return TimeInfo(ellapsed,remaining,total,remaining/total)
