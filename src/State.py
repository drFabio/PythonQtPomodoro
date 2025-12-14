from dataclasses import dataclass
from typing import Iterator
import time
from collections import namedtuple
from TimeSection import TimeSection

TimeInfo = namedtuple('TimeInfo', ['ellapsed', 'remaining', 'total','percentage'])

class Status:
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

@dataclass
class State:
    interval: TimeSection | None = None
    # Time elapsed on the current cycle (in seconds)
    ellapsed_time: int = 0
    start_time: int = 0
    stop_time: int = 0
    cyles: int = 0
    intervals: Iterator[TimeSection] = iter([])
    status: str = Status.STOPPED
    current_interval: TimeSection | None = None

    def start(self):
        self.status = Status.RUNNING
        self.start_time =  int(time.time())
        interval =  next(self.intervals)
        self.current_interval = interval
        return interval
    
    def pause(self) -> None:
        info = self.getTime()
        self.ellapsed_time += info.ellapsed
        self.status = Status.PAUSED
        
    def stop(self):
        self.status = Status.STOPPED

    def getTime(self) -> TimeInfo:
        now = int(time.time()) 
        ellapsed = now - self.start_time  + self.ellapsed_time
        total = self.current_interval.duration
        remaining = total -ellapsed
        return TimeInfo(ellapsed,remaining,total,remaining/total)
