from re import S
from typing import Optional

from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import QObject
from State import State


class Menu(QMenu):
    def __init__(self, state:State, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.state = state
        # Status display for current cycle and remaining time
        self.status_action = self.addAction("")
        self.status_action.setDisabled(True)
        self.pause = self.addAction("Pause")
        self.pause.triggered.connect(self._on_pause)
        self.resume = self.addAction("Resume")
        self.resume.triggered.connect(self._on_resume)
        self.stop = self.addAction("Stop")
        self.stop.triggered.connect(self._on_stop)
        self.start = self.addAction("Start")
        self.start.triggered.connect(self._on_start)
        self.addSeparator()
        self.quit_action = self.addAction("Quit")
        self.quit_action.triggered.connect(self._on_quit)
        # Keep status text in sync with timer state
        self.state.tick_event.connect(self._update_status)
        self.state.start_event.connect(self._update_status)
        self._update_status()
        self._on_start()


    def _format_time(self, seconds: int) -> str:
        if seconds < 0:
            seconds = 0
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"


    def _update_status(self):
        interval = self.state.current_interval
        if interval is None:
            self.status_action.setText("Idle")
            return
        info = self.state.getTime()
        remaining = info.remaining
        self.status_action.setText(
            f"{interval.name} - {self._format_time(remaining)} remaining"
        )


    def _on_pause(self):
        self.pause.setDisabled(True)
        self.resume.setDisabled(False)
        self.state.pause()


    def _on_resume(self):
        self.resume.setDisabled(True)
        self.pause.setDisabled(False)
        self.state.resume()


    def _on_stop(self):
        self.start.setDisabled(False)
        self.stop.setDisabled(True)
        self.state.stop()


    def _on_start(self):
        self.resume.setDisabled(True)
        self.start.setDisabled(True)
        self.stop.setDisabled(False) 
        self.state.start()   

    def _on_quit(self):
        self.state.quit()
