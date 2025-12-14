from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from typing import Optional
from State import State
from Menu import Menu

class PomodoroTray(QSystemTrayIcon):
    stop_event = pyqtSignal()
    pause_event = pyqtSignal()
    resume_event = pyqtSignal()
    skip_event = pyqtSignal()

    def __init__(self,state:State, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.state = state
        self.setToolTip("Pomodoro Timer")
        self.update_icon()        
        self.setup_menu()
        self.show()

    def setup_menu(self) -> None:
        menu = Menu(self)
        self.setContextMenu(menu)
        self.menu = menu


        

    def update_icon(self, percentage: float=0,fill_color: QColor = QColor("#FF6347")) -> None:
        icon = self.create_circular_icon(percentage, fill_color)
        self.setIcon(icon)

    def create_circular_icon(self, fill_percentage: float, fill_color: QColor = QColor("#FF6347")) -> QIcon:
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

       
        margin = 4
        rect = 0 + margin, 0 + margin, size - 2*margin, size - 2*margin
        
       
        bg_color = QColor(200, 200, 200, 50)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(*rect)

     
        start_angle = 90 * 16
        span_angle = int(fill_percentage * 360 * 16)
        painter.setBrush(QBrush(fill_color))
        painter.drawPie(margin, margin, size - 2*margin, size - 2*margin, start_angle, span_angle)

        painter.end()
        return QIcon(pixmap)
