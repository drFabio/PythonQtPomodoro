from typing import Any, List, Optional
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHeaderView
from PyQt6.QtCore import Qt

class StatsTable(QTableWidget):
    def __init__(self, rows: List[Any], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.rows = rows
        self._setup_ui()

    def _setup_ui(self):
        headers = ["ID", "Start Time", "End Time", "Label"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        self.setRowCount(len(self.rows))

        for row_idx, row_data in enumerate(self.rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.setItem(row_idx, col_idx, item)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
