from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QDialogButtonBox


class MessageDialog(QDialog):

    def __init__(self, parent, title: str, message: str, buttons: QDialogButtonBox.StandardButton = QDialogButtonBox.StandardButton.Ok):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle(title)

        self.showFullScreen()
        self.setFixedSize(320, 240)

        title_label = QLabel(title, self)
        message_label = QLabel(message, self)

        self.buttons = QDialogButtonBox(buttons, Qt.Orientation.Horizontal, self)

        vbox = QVBoxLayout(self)
        vbox.addWidget(title_label, stretch=1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        vbox.addWidget(message_label, stretch=1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        vbox.addWidget(self.buttons, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
