from typing import Any, List, Optional
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHeaderView
from PyQt6.QtCore import Qt

class StatsTable(QTableWidget):
    def __init__(self, rows: List[Any], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.rows = rows
        self._setup_ui()

    def _setup_ui(self):
        # Columns: ID, Start Time, End Time, Interval Label
        headers = ["ID", "Start Time", "End Time", "Label"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        self.setRowCount(len(self.rows))

        for row_idx, row_data in enumerate(self.rows):
            # row_data is expected to be a tuple/list like (id, start, end, label)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.setItem(row_idx, col_idx, item)

        # Adjust column widths
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Stretch the label column
        
        # basic table settings
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
