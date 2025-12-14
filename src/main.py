import sys
from PyQt6.QtWidgets import QApplication
from tray import PomodoroTray
from cycler import IconCycler

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    tray = PomodoroTray(app)
    
    cycler = IconCycler(tray)
    cycler.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
