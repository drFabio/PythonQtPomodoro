from re import S
from typing import Optional

from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import QObject
from State import State


class Menu(QMenu):
    def __init__(self, state:State, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.state = state
        self.pause = self.addAction("Pause")
        self.pause.triggered.connect(lambda: state.pause_event.emit())
        self.resume = self.addAction("Resume")
        self.resume.triggered.connect(lambda: state.resume_event.emit())
        self.stop = self.addAction("Stop")
        self.stop.triggered.connect(lambda: state.stop_event.emit())
        self.start = self.addAction("Start")
        self.start.triggered.connect(lambda: state.start_event.emit())
        self.addSeparator()
        self.quit_action = self.addAction("Quit")
        self.quit_action.triggered.connect(lambda: state.quit_event.emit())
        self._plug_events()
        self._on_start()
    
    def _plug_events(self):
        self.state.pause_event.connect(self._on_pause)
        self.state.resume_event.connect(self._on_resume)
        self.state.stop_event.connect(self._on_stop)

    def _on_pause(self):
        self.pause.setDisabled(True)
        self.resume.setDisabled(False)

    def _on_resume(self):
        self.resume.setDisabled(True)
        self.pause.setDisabled(False)

    def _on_stop(self):
        self.start.setDisabled(False)
        self.stop.setDisabled(True)

    def _on_start(self):
        self.resume.setDisabled(True)
        self.start.setDisabled(True)
        self.stop.setDisabled(False)    



