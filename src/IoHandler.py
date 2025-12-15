from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlError, QSqlQuery

from State import State

DateTimeLike = Union[QDateTime, str]


class IoHandler:

    def __init__(
        self,
        state:State,
        db_path: Optional[str] = None,
        connection_name: str = "pomodoro_connection",
    ) -> None:
        self.state = state
        if db_path is None:
            db_path = str(Path(__file__).resolve().parent / "pomodoro_stats.db")
        print("DB PATH", db_path)
        self._db_path = db_path
        self._connection_name = connection_name
        self._db: Optional[QSqlDatabase] = None
        self._plug_events()

    def _plug_events(self):
        self.state.cycle_ended_event.connect(self._on_cycle_end)

    def _on_cycle_end(self, cycle_info: dict):
        print(f"Saving cycle {cycle_info}")
        self.save_cycle(
            start=cycle_info['start'],
            end=cycle_info['end'],
            interval_label=cycle_info['name'],
        )

    def save_cycle(
        self,
        start: DateTimeLike,
        end: DateTimeLike,
        interval_label: str,
    ) -> bool:
        db = self._ensure_connection()
        if db is None:
            return False

        if not self._ensure_schema():
            return False

        start_iso = self._to_iso(start)
        end_iso = self._to_iso(end)

        query = QSqlQuery(db)
        query.prepare(
            """
            INSERT INTO pomodoro_cycles (start_time, end_time, interval_label)
            VALUES (?, ?, ?)
            """.strip()
        )
        query.addBindValue(start_iso)
        query.addBindValue(end_iso)
        query.addBindValue(interval_label)

        if not query.exec():
            return False

        return True

    def _ensure_connection(self) -> Optional[QSqlDatabase]:
        if self._db is not None and self._db.isOpen():
            return self._db

        if QSqlDatabase.contains(self._connection_name):
            db = QSqlDatabase.database(self._connection_name)
        else:
            db = QSqlDatabase.addDatabase("QSQLITE", self._connection_name)
            db.setDatabaseName(self._db_path)

        if not db.isOpen() and not db.open():
            return None

        self._db = db
        return db

    def _ensure_schema(self) -> bool:
        db = self._ensure_connection()
        if db is None:
            return False

        query = QSqlQuery(db)
        ddl = (
            "CREATE TABLE IF NOT EXISTS pomodoro_cycles ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "start_time TEXT NOT NULL, "
            "end_time TEXT NOT NULL, "
            "interval_label TEXT NOT NULL"  # e.g. 'work', 'short_break'
            ")"
        )

        if not query.exec(ddl):
            return False

        return True

    def _to_iso(self, value: DateTimeLike) -> str:
        if isinstance(value, QDateTime):
            return value.toString(Qt.DateFormat.ISODate)
        return str(value)
