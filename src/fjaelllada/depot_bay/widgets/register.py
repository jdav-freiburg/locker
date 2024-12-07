import qrcode
import qrcode.image.base

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget

from devctl import auth
from devctl.widgets.base import exc
from devctl.widgets.qr_code_pixmap import QRCodePixmap


class RegisterWidget(QWidget):
    success = pyqtSignal()
    close = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        # Create the username prompt and image label widgets
        self.username_edit = QLineEdit()
        self.qrcode_label = QLabel()
        self.qrcode_label.setAlignment(Qt.AlignCenter)
        close_button = QPushButton("X")
        close_button.clicked.connect(self.close)

        # Create the button to load the image
        self.load_button = QPushButton("Generate")
        self.load_button.clicked.connect(self.generate_qr)

        # Create a layout for the username prompt and button
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Name:"))
        username_layout.addWidget(self.username_edit)
        username_layout.addWidget(self.load_button)
        username_layout.addWidget(close_button)

        # Create a layout for the image label
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.qrcode_label)

        # Create confirm prompt
        self.code_edit = QLineEdit()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)

        # Create a layout for code confirmation
        verify_layout = QHBoxLayout()
        verify_layout.addWidget(QLabel("Code:"))
        verify_layout.addWidget(self.code_edit)
        verify_layout.addWidget(self.save_button)

        self.info_label = QLabel()

        # Add both layouts to the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(username_layout)
        main_layout.addLayout(image_layout)
        main_layout.addLayout(verify_layout)
        main_layout.addWidget(self.info_label)

    @exc
    def generate_qr(self, *_):
        # Get the username from the QLineEdit widget
        username = self.username_edit.text()

        self.uri = auth.db.new_uri(username)

        # Generate the QR code and save it to a file
        qr = qrcode.QRCode(version=None, box_size=7, border=4)
        qr.add_data(self.uri)
        qr.make(fit=True)
        self.qrcode_label.setPixmap(qr.make_image(QRCodePixmap).get_image())

        self.info_label.setPalette(QPalette(QColor(200, 200, 0, 255)))
        self.info_label.setText("Scan QR code with authenticator app")

    @exc
    def save(self, *_):
        if auth.db.register(self.uri, self.code_edit.text()):
            self.success.emit()
        else:
            self.info_label.setPalette(QPalette(QColor(200, 0, 0, 255)))
            self.info_label.setText("Code did not match, try again")
