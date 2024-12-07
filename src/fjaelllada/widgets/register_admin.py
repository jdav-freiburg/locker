import fjaelllada.qrcode
import fjaelllada.qrcode.image.base

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout, QWidget, QDialogButtonBox

import fjaelllada.totp_auth
from fjaelllada.widgets.base import exc
from fjaelllada.widgets.message_dialog import MessageDialog
from fjaelllada.widgets.pin_input import PinInput
from fjaelllada.widgets.qr_code_pixmap import QRCodePixmap
from fjaelllada.widgets.text_input import T9Input


class QRCodeWidget(QWidget):
    next = pyqtSignal()
    prev = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        prev_button = QPushButton("←")
        prev_button.clicked.connect(self.prev)

        info_label = QLabel("Scan with authenticator app", self)
        info_label.setPalette(QPalette(QColor(200, 200, 0, 255)))

        next_button = QPushButton("Ok")
        next_button.clicked.connect(self.next)

        self.qrcode_label = QLabel()
        self.qrcode_label.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(prev_button)
        hbox.addWidget(info_label)
        hbox.addWidget(next_button)
        hbox.setSpacing(1)
        hbox.setContentsMargins(1, 1, 1, 1)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addWidget(self.qrcode_label)
        vbox.setSpacing(1)
        vbox.setContentsMargins(1, 1, 1, 1)
    
    def clear(self):
        self.qrcode_label.clear()

    def set_data(self, data: str):
        qr = qrcode.QRCode(version=None, box_size=4, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        self.qrcode_label.setPixmap(qr.make_image(QRCodePixmap).get_image())


class RegisterAdminWidget(QWidget):
    success = pyqtSignal()
    abort = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        # Create stacked layout and add layouts
        self.stacked_layout = QStackedLayout(self)
        self.stacked_layout.setStackingMode(QStackedLayout.StackingMode.StackOne)

        self.name_input = T9Input(self, "Name:")
        self.name_input.success.connect(self.username_next)
        self.stacked_layout.addWidget(self.name_input)

        self.qr_code = QRCodeWidget(self)
        self.qr_code.prev.connect(self.qr_code_prev)
        self.qr_code.next.connect(self.qr_code_next)
        self.stacked_layout.addWidget(self.qr_code)

        self.confirm_pin_input = PinInput(self, pin_label_text="Verify PIN", pin_visible=True)
        self.confirm_pin_input.pin_output.connect(self.confirm_pin)
        self.stacked_layout.addWidget(self.confirm_pin_input)

        self.stacked_layout.setCurrentIndex(0)

    def clear(self):
        self.name_input.clear()
        self.qr_code.clear()
        self.confirm_pin_input.clear()
        self.stacked_layout.setCurrentIndex(0)
    
    @exc
    def _abort(self, *_):
        self.clear()
        self.abort.emit()

    @exc
    def username_next(self, username: str):
        if not username:
            dlg = MessageDialog(self, "No name", "Please enter a name", QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Abort)
            dlg.buttons.accepted.connect(lambda *_: dlg.close())
            dlg.buttons.rejected.connect(lambda *_: dlg.close() and self._abort())
            dlg.exec()
            return
        # Get the username from the QLineEdit widget
        self.uri = totp_auth.db.new_uri(username)
        self.qr_code.set_data(self.uri)
        self.stacked_layout.setCurrentIndex(1)
    
    @exc
    def qr_code_prev(self):
        self.stacked_layout.setCurrentIndex(0)
    
    @exc
    def qr_code_next(self):
        self.stacked_layout.setCurrentIndex(2)
    
    @exc
    def confirm_pin(self, pin: str):
        if totp_auth.db.register(self.uri, pin):    
            self.clear()
            self.success.emit()
        else:
            dlg = MessageDialog(self, "Invalid PIN", "Pin could not be verified, try again", QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Abort)
            dlg.buttons.accepted.connect(lambda *_: dlg.close())
            dlg.buttons.rejected.connect(lambda *_: dlg.close() and self._abort())
            dlg.exec()
