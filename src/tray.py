from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QObject
from typing import Optional

class PomodoroTray(QSystemTrayIcon):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.setToolTip("Pomodoro Timer")
        
        self.update_icon()        
        self.setup_menu()
        self.show()
        self.activated.connect(self.on_activated)

    def setup_menu(self) -> None:
        menu = QMenu()
        
       
        action_75 = menu.addAction("75%")
        action_75.triggered.connect(lambda: self.update_icon(0.75))
        
        action_50 = menu.addAction("50%")
        action_50.triggered.connect(lambda: self.update_icon(0.50))
        
        action_25 = menu.addAction("25%")
        action_25.triggered.connect(lambda: self.update_icon(0.25))
        
        menu.addSeparator()
        
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(lambda: self.parent().quit() if self.parent() else None)
        
        self.setContextMenu(menu)
        self.menu = menu

    def on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
       
       
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
           
            self.menu.popup(self.geometry().center())

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
