import functools

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget

from widgets.base import exc


class QT9Button(QPushButton):
    pass


class T9Input(QWidget):
    success = pyqtSignal(str)

    next_char_interval = 1000

    def __init__(self, parent, label_text: str):
        super().__init__(parent)

        # Create pin input widgets
        pin_label = QLabel(label_text)
        self.text_input = QLineEdit()
        self.text_input.textChanged.connect(self.text_changed)

        # Create digit buttons
        digit_layout = QGridLayout()
        digit_layout.setSpacing(1)
        digit_layout.setContentsMargins(1, 1, 1, 1)
        digits = ["1", "ABC2", "DEF3", "GHI4", "JKL5", "MNO6", "PQRS7", "TUV8", "WXYZ9", "←", "_0", "Ok"]
        positions = [(i, j) for i in range(4) for j in range(3)]
        for position, digit in zip(positions, digits):
            if digit == "←":
                button = QT9Button(digit)
                button.clicked.connect(self.text_input.backspace)
            elif digit == 'Ok':
                button = QT9Button("Ok")
                button.clicked.connect(self.confirm)
            else:
                button = QT9Button(digit)
                button.clicked.connect(functools.partial(self.push_button, digit))
            digit_layout.addWidget(button, *position)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        text_line = QHBoxLayout()
        text_line.setSpacing(1)
        text_line.setContentsMargins(1, 1, 1, 1)
        text_line.addWidget(pin_label)
        text_line.addWidget(self.text_input)
        layout.addLayout(text_line)
        layout.addLayout(digit_layout)
        self.setLayout(layout)

        # Set up timer for clearing input
        self.next_char_timer = QTimer(self)
        self.next_char_timer.setSingleShot(True)
        self.next_char_timer.timeout.connect(self.next_char_timeout)
    
    @exc
    def push_button(self, button_label: str, *_):
        if self.text_input.hasSelectedText():
            if self.text_input.selectionLength() == 1:
                if self.text_input.selectedText() in button_label:
                    # Replace current selection
                    insert_text = button_label[(button_label.index(self.text_input.selectedText()) + 1) % len(button_label)]
                    restore_selection = (self.text_input.selectionStart(), self.text_input.selectionStart() + 1)
                else:
                    # Append after current character
                    self.text_input.setSelection(self.text_input.selectionEnd(), self.text_input.selectionEnd())
                    insert_text = button_label[0]
                    restore_selection = (self.text_input.cursorPosition(), self.text_input.cursorPosition() + 1)
            else:
                # Replace current multi-selection
                insert_text = button_label[0]
                restore_selection = (self.text_input.selectionStart(), self.text_input.selectionStart() + 1)
            self.text_input.insert(insert_text)
            self.text_input.setSelection(*restore_selection)
        else:
            self.text_input.insert(button_label[0])
            self.text_input.setSelection(self.text_input.cursorPosition() - 1, self.text_input.cursorPosition())
        self.next_char_timer.stop()
        self.next_char_timer.start(self.next_char_interval)
    
    @exc
    def next_char_timeout(self, *_):
        if self.text_input.hasSelectedText() and self.text_input.selectionLength() == 1:
            self.text_input.setSelection(self.text_input.selectionEnd(), self.text_input.selectionEnd())
    
    @exc
    def text_changed(self, *_):
        self.next_char_timer.stop()

    @exc
    def confirm(self, *_):
        code = self.text_input.text()
        self.success.emit(code)
    
    def clear(self):
        self.text_input.clear()
