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
        self._on_start()


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
