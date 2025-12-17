from pathlib import Path
from typing import Optional, List, Tuple
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from StatsTable import StatsTable

class StatsWindow(QWidget):
    def __init__(self, db_path: Optional[str] = None) -> None:
        super().__init__()
        if db_path is None:
            db_path = str(Path(__file__).resolve().parent / "pomodoro_stats.db")
        self.db_path = db_path
        
        self.setWindowTitle("Pomodoro Stats")
        self.resize(600, 400)
        
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        
        self._load_data_and_setup_ui()

    def _load_data_and_setup_ui(self):
        rows = self._fetch_data()
        if not rows:
            pass

        self.table = StatsTable(rows)
        self._layout.addWidget(self.table)

    def _fetch_data(self) -> List[Tuple[int, str, str, str]]:
        if not Path(self.db_path).exists():
            return []

        connection_name = "stats_connection"
        if QSqlDatabase.contains(connection_name):
            db = QSqlDatabase.database(connection_name)
        else:
            db = QSqlDatabase.addDatabase("QSQLITE", connection_name)
            db.setDatabaseName(self.db_path)

        if not db.open():
            print(f"Failed to open database for stats: {db.lastError().text()}")
            return []

        query = QSqlQuery(db)
        if not query.exec("SELECT id, start_time, end_time, interval_label FROM pomodoro_cycles ORDER BY id DESC"):
            print(f"Failed to query stats: {query.lastError().text()}")
            db.close()
            return []

        results = []
        while query.next():
            row_id = query.value(0)
            start = query.value(1)
            end = query.value(2)
            label = query.value(3)
            results.append((row_id, start, end, label))

        db.close()
        return results
