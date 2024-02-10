import functools
from typing import Callable

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget

import totp_auth
from widgets.base import exc


class QPinButton(QPushButton):
    pass


class PinInput(QWidget):
    pin_output = pyqtSignal(str)

    def __init__(self, parent, pin_label_text: str = "PIN", pin_visible: bool = False):
        super().__init__(parent)

        # Create pin input widgets
        pin_label = QLabel(pin_label_text)
        self.pin_input = QLineEdit()
        if not pin_visible:
            self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.textChanged.connect(self.reset_timer)

        # Create digit buttons
        digit_layout = QGridLayout()
        digit_layout.setSpacing(1)
        digit_layout.setContentsMargins(1, 1, 1, 1)
        digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "←", "0", "Ok"]
        positions = [(i, j) for i in range(4) for j in range(3)]
        for position, digit in zip(positions, digits):
            if digit == "←":
                button = QPinButton(digit)
                button.clicked.connect(self.pin_input.backspace)
            elif digit == 'Ok':
                button = QPinButton("Ok")
                button.clicked.connect(self.confirm)
            else:
                button = QPinButton(digit)
                button.clicked.connect(functools.partial(self.pin_input.insert, digit))
            digit_layout.addWidget(button, *position)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        pin_line = QHBoxLayout()
        pin_line.setSpacing(1)
        pin_line.setContentsMargins(1, 1, 1, 1)
        pin_line.addWidget(pin_label)
        pin_line.addWidget(self.pin_input)
        layout.addLayout(pin_line)
        layout.addLayout(digit_layout)
        self.setLayout(layout)

        # Set up timer for clearing input
        self.clear_timer = QTimer(self)
        self.clear_timer.setSingleShot(True)
        self.clear_timer.timeout.connect(self.pin_input.clear)

    @exc
    def reset_timer(self, *_):
        # Reset the timer and start counting again
        self.clear_timer.stop()
        self.clear_timer.start(10000)
    
    def clear(self):
        self.pin_input.clear()

    @exc
    def confirm(self, *_):
        self.pin_output.emit(self.pin_input.text())
        self.pin_input.clear()
