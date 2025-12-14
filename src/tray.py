from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import Qt

class PomodoroTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip("Pomodoro Timer")
        
       
        self.fill_percentage = 1.0 
        self.update_icon()
        
       
        self.setup_menu()
        
       
        self.show()

       
        self.activated.connect(self.on_activated)

    def setup_menu(self):
        menu = QMenu()
        
       
        action_75 = menu.addAction("75%")
        action_75.triggered.connect(lambda: self.set_fill(0.75))
        
        action_50 = menu.addAction("50%")
        action_50.triggered.connect(lambda: self.set_fill(0.50))
        
        action_25 = menu.addAction("25%")
        action_25.triggered.connect(lambda: self.set_fill(0.25))
        
        menu.addSeparator()
        
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(lambda: self.parent().quit() if self.parent() else None)
        
        self.setContextMenu(menu)
        self.menu = menu

    def on_activated(self, reason):
       
       
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
           
            self.menu.popup(self.geometry().center())

    def set_fill(self, percentage,fill_color=QColor("#FF6347")):
        self.fill_percentage = percentage
        self.update_icon(fill_color)
        self.setToolTip(f"Pomodoro: {int(percentage * 100)}%")

    def update_icon(self,fill_color=QColor("#FF6347")):
        icon = self.create_circular_icon(self.fill_percentage,fill_color)
        self.setIcon(icon)

    def create_circular_icon(self, fill_percentage, fill_color=QColor("#FF6347")):
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
        print(f"paiting fill: {fill_color.getRgb()}")
        painter.setBrush(QBrush(fill_color))
        painter.drawPie(margin, margin, size - 2*margin, size - 2*margin, start_angle, span_angle)

        painter.end()
        return QIcon(pixmap)
