from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import Qt

class PomodoroTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip("Pomodoro Timer")
        
        # Initial state
        self.fill_percentage = 1.0  # 100%
        self.update_icon()
        
        # Setup menu
        self.setup_menu()
        
        # Show tray icon
        self.show()

        # Handle activation (click)
        self.activated.connect(self.on_activated)

    def setup_menu(self):
        menu = QMenu()
        
        # Actions for different fill levels
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
        # On macOS, the tray icon behavior is slightly different and handled by the OS mostly,
        # but for cross-platform consistency or specific behavior:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Show context menu on left click
            self.menu.popup(self.geometry().center())

    def set_fill(self, percentage):
        self.fill_percentage = percentage
        self.update_icon()
        self.setToolTip(f"Pomodoro: {int(percentage * 100)}%")

    def update_icon(self):
        icon = self.create_circular_icon(self.fill_percentage)
        self.setIcon(icon)

    def create_circular_icon(self, fill_percentage):
        size = 64  # High resolution for retina displays, will be scaled down
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background circle (empty/outline)
        margin = 4
        rect = 0 + margin, 0 + margin, size - 2*margin, size - 2*margin
        
        # Background (faint or empty)
        bg_color = QColor(200, 200, 200, 50)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(*rect)

     
        start_angle = 90 * 16
        span_angle = -int(fill_percentage * 360 * 16)
        
        fill_color = QColor("#FF6347")
        painter.setBrush(QBrush(fill_color))
        painter.drawPie(margin, margin, size - 2*margin, size - 2*margin, start_angle, span_angle)

        painter.end()
        return QIcon(pixmap)
