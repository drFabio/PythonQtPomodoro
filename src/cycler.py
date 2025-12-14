from PyQt6.QtCore import QTimer
import itertools
import time

from TimeSection import TimeSection
from common import colors

TICK_INTERVAL = 1_000
Pomodoro,Short,Long = [
    TimeSection(name="Pomodoro", duration=25, color=colors['RED']),
    TimeSection(name="Short Break", duration=5, color=colors['YELLOW']),
    TimeSection(name="Long Break", duration=15, color=colors['ORANGE']),
]

class IconCycler:
    def __init__(self, tray):
        self.tray = tray
        self.timer = QTimer()
        self.timer.timeout.connect(self.__tick)
        
        self.intervals = itertools.cycle([Pomodoro,Short,Pomodoro,Short, Pomodoro,Long])

    def start(self):
        self.start_time = int(time.time())
        self.interval = next(self.intervals)
        print(f"Starting interval: {self.interval.name}")
        self.timer.start(TICK_INTERVAL) 
        self.tray.set_fill(1,self.interval.color)


    
    def halt(self):
        self.timer.stop()

    def __tick(self):
        now = int(time.time())
        ellapsed = now - self.start_time 
        remaining=self.interval.duration-ellapsed
        print(f"Remaining: {remaining}")
        if remaining<0:
            self.halt()
            self.start()
            return
        percentage=(remaining/self.interval.duration)
        self.tray.set_fill(percentage,self.interval.color)
