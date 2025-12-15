from PyQt6.QtCore import QTimer

from State import State


TICK_INTERVAL = 1_000

class IconCycler:
    def __init__(self,state :State) -> None:
        self.timer = QTimer()
        self.state = state
        self.timer.timeout.connect(self.__tick)        
        self._plug_events()
    
    def _plug_events(self):
        self.state.pause_event.connect(self._on_pause)
        self.state.resume_event.connect(self._on_resume)
        self.state.stop_event.connect(self._on_stop)
        self.state.start_event.connect(self._on_start)


    def start(self) -> None:
        print(f"Starting interval: {self.state.current_interval.name}")
        self.timer.start(TICK_INTERVAL) 

    def _on_pause(self) ->None:
        print("Pausing")
        self.timer.stop()

    def _on_resume(self) ->None:
        print("Resuming")
        self.timer.start(TICK_INTERVAL) 


    def _on_stop(self)->None:
        self.timer.stop()


    def _next_cycle(self):
        self._on_stop()
        self.state.start()

    def __tick(self) -> None:
        info = self.state.getTime()
        print(f"Remaining: {info.remaining} {self.state.current_interval.name}")
        self.state.tick_event.emit()
        if info.remaining <= 0:
            self._next_cycle()
            return


    def _on_start(self)-> None:
        self.start()
