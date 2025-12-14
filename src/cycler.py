from PyQt6.QtCore import QTimer

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
        self._plug_events()
    
    def _plug_events(self):
        self.state.pause_event.connect(self.pause)
        self.state.resume_event.connect(self.resume)


    def start(self) -> None:
        self.interval = self.state.start()
        print(f"Starting interval: {self.interval.name}")
        self.timer.start(TICK_INTERVAL) 
        self.tray.update_icon(1.0, self.interval.color)

    def pause(self) ->None:
        print("Pausing")
        self.halt()
        self.state.pause()

    def resume(self) ->None:
        print("Resuming")
        self.timer.start(TICK_INTERVAL) 
        self.state.resume()

    def halt(self) -> None:
        self.timer.stop()

    def __tick(self) -> None:
        info = self.state.getTime()

        print(f"Remaining: {info.remaining} {self.interval.name}")
        if info.remaining <= 0:
            self.halt()
            self.start()
            return
        self.tray.update_icon(info.percentage, self.interval.color)
