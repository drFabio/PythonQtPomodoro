from PyQt6.QtCore import QTimer
import time

from State import State

from tray import PomodoroTray

TICK_INTERVAL = 1_000

class IconCycler:
    def __init__(self, tray: PomodoroTray,state :State) -> None:
        self.tray = tray
        self.timer = QTimer()
        self.state = state
        self.timer.timeout.connect(self.__tick)        
        self.start_time: int

    def start(self) -> None:
        self.interval = self.state.start()
        print(f"Starting interval: {self.interval.name}")
        self.timer.start(TICK_INTERVAL) 
        self.tray.update_icon(1.0, self.interval.color)

    
    def halt(self) -> None:
        self.state.stop()
        self.timer.stop()

    def __tick(self) -> None:
        now = int(time.time())
        ellapsed = now - self.state.start_time 
        remaining = self.interval.duration - ellapsed
        print(f"Remaining: {remaining}")
        if remaining <= 0:
            self.halt()
            self.start()
            return
        percentage = remaining / self.interval.duration
        self.tray.update_icon(percentage, self.interval.color)
