from dataclasses import dataclass
from typing import Iterator

from TimeSection import TimeSection

@dataclass
class State:
    interval: TimeSection | None = None
    ellapsed_time: int = 0
    intervals: Iterator[TimeSection] = iter([])
    class Status:
        RUNNING = "running"
        PAUSED = "paused"
        STOPPED = "stopped"

    status: str = Status.STOPPED