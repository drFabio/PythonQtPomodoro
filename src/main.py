import sys
from PyQt6.QtWidgets import QApplication
from IoHandler import IoHandler
from Menu import Menu
from State import State
from Tray import Tray
from IconCycler import IconCycler
from TimeSection import TimeSection

from common import colors

def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    Pomodoro,Short,Long = [
        TimeSection(name="Pomodoro", duration=25, color=colors['RED']),
        TimeSection(name="Short Break", duration=5, color=colors['YELLOW']),
        TimeSection(name="Long Break", duration=15, color=colors['ORANGE']),
    ]
    state = State(intervals= [Pomodoro,Short,Pomodoro,Short, Pomodoro,Long])
    io = IoHandler(state)
    menu = Menu(state)
    Tray(state,menu, app)    
    cycler = IconCycler(state)
    state.quit_event.connect(lambda: app.quit())
    cycler.start()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
