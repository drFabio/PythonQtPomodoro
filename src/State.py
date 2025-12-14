from dataclasses import dataclass
from typing import Iterator
import time

from TimeSection import TimeSection

class Status:
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

@dataclass
class State:
    interval: TimeSection | None = None
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

    def stop(self):
        self.status = Status.STOPPED