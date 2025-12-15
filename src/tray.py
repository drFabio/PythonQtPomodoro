from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QObject
from typing import Optional
from State import State
from Menu import Menu

class Tray(QSystemTrayIcon):

    def __init__(self,state:State, menu:Menu, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.state = state
        self.menu = menu
        self.setToolTip("Pomodoro Timer")
        self.update_icon()        
        self.setContextMenu(menu)
        self._plug_events()
        self.show()

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
   
    def _plug_events(self):
        self.state.start_event.connect(self._on_start)
        self.state.stop_event.connect(self._on_stop)
        self.state.tick_event.connect(self._on_tick)


    def _on_start(self):
        self.update_icon(1.0, self.state.current_interval.color)
 
    def _on_stop(self):
        self.update_icon(1.0, self.state.current_interval.color)
 
    def _on_tick(self):
        info = self.state.getTime()
        self.update_icon(info.percentage, self.state.current_interval.color)
