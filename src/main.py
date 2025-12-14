import sys
from PyQt6.QtWidgets import QApplication
from tray import PomodoroTray

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    tray = PomodoroTray(app)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
