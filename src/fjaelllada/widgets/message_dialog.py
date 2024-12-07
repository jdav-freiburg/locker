from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QDialogButtonBox, QSizePolicy


class MessageDialog(QDialog):

    def __init__(self, parent, title: str, message: str, buttons: QDialogButtonBox.StandardButton = QDialogButtonBox.StandardButton.Ok):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle(title)

        title_label = QLabel(title, self)
        message_label = QLabel(message, self)

        self.buttons = QDialogButtonBox(buttons, Qt.Orientation.Horizontal, self)

        self.buttons.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        vbox = QVBoxLayout(self)
        vbox.addWidget(title_label, stretch=1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        vbox.addWidget(message_label, stretch=1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        vbox.addWidget(self.buttons, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

        self.showFullScreen()
        self.setFixedSize(320, 240)
        self.setGeometry(0, 0, 320, 240)

        self.setStyleSheet((Path(__file__).parent / 'style.qss').read_text())
