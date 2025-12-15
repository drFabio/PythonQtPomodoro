from typing import Iterator
import time
from collections import namedtuple
from TimeSection import TimeSection
from PyQt6.QtCore import QObject, pyqtSignal
import itertools
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
    start_event = pyqtSignal()
    quit_event = pyqtSignal()
    tick_event = pyqtSignal()

    def __init__(self, intervals: [TimeSection] = []) -> None:
        super().__init__()
        self._intervals = intervals
        self._reset_state()

    def start(self):
        interval =  next(self.cycle)
        self.current_interval = interval
        self._set_initial_state()
        self.start_event.emit()
        return interval
    
    def pause(self) -> None:
        info = self.getTime()
        self.ellapsed_time = info.ellapsed
        print(f"Saving ellapsed time ${info.ellapsed}")
        self.status = Status.PAUSED
        self.pause_event.emit()

    
    def resume(self) -> None:
        self._set_initial_state()
        self.resume_event.emit()


    def stop(self):
        self._reset_state()
        self.stop_event.emit()

    def _set_initial_state(self):
        self.status = Status.RUNNING
        self.start_time = int(time.time())

    def _reset_state(self):
        self.cycle: Iterator[TimeSection] = itertools.cycle(self._intervals)
        self.interval: TimeSection | None = None
        # Time elapsed on the current cycle (in seconds)
        self.ellapsed_time: int = 0
        self.start_time: int = 0
        self.stop_time: int = 0
        self.cycles_count: int = 0
        self.status: str = Status.STOPPED
        self.current_interval: TimeSection | None = None


    def getTime(self) -> TimeInfo:
        now = int(time.time()) 
        ellapsed = now - self.start_time  + self.ellapsed_time
        total = self.current_interval.duration
        remaining = total -ellapsed
        return TimeInfo(ellapsed,remaining,total,remaining/total)

    def quit(self):
        self.quit_event.emit()