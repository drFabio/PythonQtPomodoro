from typing import List, Tuple, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont
from PyQt6.QtCore import Qt, QRect

class Chart(QWidget):
    def __init__(self, db_path: str, parent=None) -> None:
        super().__init__(parent)
        self.db_path = db_path
        self.data: List[Tuple[str, int]] = []
        self._fetch_data()
        self.setMinimumSize(400, 300)

    def _fetch_data(self):
        connection_name = "chart_connection"
        if QSqlDatabase.contains(connection_name):
            db = QSqlDatabase.database(connection_name)
        else:
            db = QSqlDatabase.addDatabase("QSQLITE", connection_name)
            db.setDatabaseName(self.db_path)

        if not db.open():
            print(f"Failed to open database for chart: {db.lastError().text()}")
            return

        query = QSqlQuery(db)
        sql = """
            SELECT 
                interval_label, 
                SUM(CAST(end_time AS INTEGER) - CAST(start_time AS INTEGER)) as duration 
            FROM pomodoro_cycles 
            GROUP BY interval_label
        """
        
        if not query.exec(sql):
            print(f"Failed to query chart data: {query.lastError().text()}")
            db.close()
            return

        self.data = []
        while query.next():
            label = query.value(0)
            duration = query.value(1)
            self.data.append((label, duration))
        
        db.close()
        self.update() # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        if not self.data:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No data available")
            return

        # Dimensions
        margin = 40
        available_width = self.width() - 2 * margin
        available_height = self.height() - 2 * margin
        
        # Find max value for scaling
        max_duration = max(d[1] for d in self.data)
        if max_duration == 0:
            max_duration = 1
            
        num_bars = len(self.data)
        bar_width = available_width / num_bars * 0.6 # 60% of slot width
        gap = available_width / num_bars * 0.4
        slot_width = available_width / num_bars

        # Draw bars
        for i, (label, duration) in enumerate(self.data):
            # Calculate height relative to max
            bar_h = (duration / max_duration) * available_height
            
            x = margin + i * slot_width + (slot_width - bar_width) / 2
            y = self.height() - margin - bar_h
            
            rect = QRect(int(x), int(y), int(bar_width), int(bar_h))
            
            # Draw bar
            painter.setBrush(QBrush(QColor(100, 150, 200)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(rect)
            
            # Draw label
            painter.setPen(Qt.GlobalColor.black)
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            
            label_rect = QRect(int(x - 10), int(self.height() - margin + 5), int(bar_width + 20), 20)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, label)
            
            # Draw value (minutes)
            value_text = f"{duration // 60}m"
            value_rect = QRect(int(x), int(y - 20), int(bar_width), 20)
            painter.drawText(value_rect, Qt.AlignmentFlag.AlignCenter, value_text)
            
        # Draw axes
        painter.setPen(Qt.GlobalColor.black)
        # X Axis
        painter.drawLine(margin, self.height() - margin, self.width() - margin, self.height() - margin)
        # Y Axis
        painter.drawLine(margin, margin, margin, self.height() - margin)
