from typing import Optional, Any

from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import QObject


class Menu(QMenu):
    def __init__(self, tray: Any, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.tray = tray

        pause = self.addAction("Pause")
        pause.triggered.connect(self.tray.pause_event.emit)

        resume = self.addAction("Resume")
        resume.setDisabled(True)
        resume.triggered.connect(lambda: self.tray.update_icon(0.50))

        stop = self.addAction("Stop")
        stop.triggered.connect(self.tray.stop_event.emit)
        stop.triggered.connect(lambda: self.tray.update_icon(0.25))

        self.addSeparator()

        quit_action = self.addAction("Quit")
        quit_action.triggered.connect(
            lambda: self.tray.parent().quit() if self.tray.parent() else None
        )
