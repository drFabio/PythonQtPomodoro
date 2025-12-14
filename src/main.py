import sys
from PyQt6.QtWidgets import QApplication
from Menu import Menu
from State import State
from tray import PomodoroTray
from cycler import IconCycler
from TimeSection import TimeSection
import itertools
from common import colors

def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    Pomodoro,Short,Long = [
        TimeSection(name="Pomodoro", duration=25, color=colors['RED']),
        TimeSection(name="Short Break", duration=5, color=colors['YELLOW']),
        TimeSection(name="Long Break", duration=15, color=colors['ORANGE']),
    ]
    state = State(intervals= itertools.cycle([Pomodoro,Short,Pomodoro,Short, Pomodoro,Long]))
    menu = Menu(state)
    tray = PomodoroTray(state,menu, app)    
    cycler = IconCycler(tray, state)
    state.quit_event.connect(lambda: app.quit())
    cycler.start()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
