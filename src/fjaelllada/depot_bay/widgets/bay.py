import traceback
from typing import List

from PyQt5.QtCore import QTimer, QRectF, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget

from fjaelllada.depot_bay import config
from fjaelllada.depot_bay.bay.station import station
from fjaelllada.depot_bay.config import BayConfig
from fjaelllada.widgets.base import exc


class BayWidget(QWidget):
    close = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMinimumSize(100, 100)
        self.open_bays = set()

        rows = sorted(list(set(bay.id[1] for bay in config.bays)))
        bays_by_row = {row: [] for row in rows}
        for bay in config.bays:
            bays_by_row[bay.id[1]].append(bay)
        self.rows: List[List[BayConfig]] = [bays_by_row[row] for row in reversed(rows)]

        self.close_button_size = 50

        # Set up timer for updating open state
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_open)
        self.update_timer.start(100)

    @exc
    def update_open(self):
        try:
            next_open = set(
                key for key, is_open in station.get_states().items() if is_open
            )
            if next_open != self.open_bays:
                self.open_bays = next_open
                self.repaint()
        except BaseException:
            traceback.print_exc()

    @exc
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        box_color = QColor(140, 60, 27, 255)
        open_color = QColor(128, 128, 128, 100)

        # Draw grid lines
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        row_height = self.height() / len(self.rows)
        total_width = self.width()
        y = 0
        alignment = (
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignLeft
            | Qt.TextFlag.TextDontClip
        )
        for row in self.rows:
            width_scale = total_width / sum(bay.width for bay in row)
            x = 0
            for bay in row:
                width = bay.width * width_scale
                rect = QRectF(x, y, width, row_height)
                painter.fillRect(rect, box_color)
                if bay.id in self.open_bays:
                    painter.fillRect(rect, open_color)
                painter.drawRect(rect)
                painter.drawText(rect, alignment, bay.id)
                x += width

            y += row_height

        btn_color = QColor(200, 200, 200, 255)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        close_rect = QRectF(
            self.width() - 10 - self.close_button_size,
            10,
            self.close_button_size,
            self.close_button_size,
        )
        painter.fillRect(close_rect, btn_color)
        painter.drawRect(close_rect)
        painter.drawText(close_rect, Qt.AlignmentFlag.AlignCenter, "X")

    @exc
    def mousePressEvent(self, event):
        self.parent.reset_logout_timer()
        close_rect = QRectF(
            self.width() - 10 - self.close_button_size,
            10,
            self.close_button_size,
            self.close_button_size,
        )
        if close_rect.contains(event.x(), event.y()):
            self.close.emit()
            return

        row_height = self.height() / len(self.rows)
        total_width = self.width()
        y = 0
        for row in self.rows:
            if y <= event.y() < y + row_height:
                width_scale = total_width / sum(bay.width for bay in row)
                x = 0
                for bay in row:
                    width = bay.width * width_scale
                    if x <= event.x() < x + width:
                        if bay.actuator_controller_id:
                            station.open_bay(bay.id)
                        return
                    x += width

            y += row_height
