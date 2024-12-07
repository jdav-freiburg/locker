from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget

from bus import open
from fjaelllada.widgets.base import exc


class BayWidget(QWidget):
    close = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMinimumSize(100, 100)
        # Set up timer for updating open state
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_open)
        self.update_timer.start(100)

    @exc
    def update_open(self):
        pass

    def on_show(self):
        open()
