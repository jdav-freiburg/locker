from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QStackedLayout, QWidget, QDialogButtonBox, QVBoxLayout, QLabel, QPushButton

from fjaelllada.db.card_db import CardDatabase
from fjaelllada.widgets.base import exc
from fjaelllada.widgets.message_dialog import MessageDialog
from fjaelllada.widgets.nfc_reader import NFCReader
from fjaelllada.widgets.text_input import T9Input


class CaptureCard(QWidget):
    save = pyqtSignal(str)
    abort = pyqtSignal()

    def __init__(self, parent: QWidget, card_reader: NFCReader) -> None:
        super().__init__(parent)
        self.card_reader = card_reader
        abort = QPushButton("X", self)
        abort.clicked.connect(self.abort)
        self.info = QLabel("", self)
        self.next = QPushButton("Save", self)
        self.next.clicked.connect(self._on_save)
        layout = QVBoxLayout(self)
        layout.addWidget(abort)
        layout.addWidget(self.info)
        layout.addWidget(self.next)
        self.clear()

    def activate(self):
        self.card_reader.capture_read_card.connect(self.read_card)
    
    def deactivate(self):
        if self.card_reader.receivers(self.card_reader.capture_read_card) > 0:
            self.card_reader.capture_read_card.disconnect()

    def read_card(self, code: str):
        self.info.setText(f"Got card {code}")
        self.code = code
        self.next.setDisabled(False)

    def clear(self):
        self.code = ""
        self.next.setDisabled(True)
        self.info.setText("Waiting for card...")
    
    def _on_save(self, *_):
        self.save.emit(self.code)


class RegisterUserWidget(QWidget):
    success = pyqtSignal()
    abort = pyqtSignal()

    username = ""

    def __init__(self, parent, card_reader: NFCReader, card_db: CardDatabase):
        super().__init__(parent)

        self.card_db = card_db

        # Create stacked layout and add layouts
        self.stacked_layout = QStackedLayout(self)
        self.stacked_layout.setStackingMode(QStackedLayout.StackingMode.StackOne)

        self.name_input = T9Input(self, "Name:")
        self.name_input.success.connect(self.username_next)
        self.stacked_layout.addWidget(self.name_input)

        self.register_card = CaptureCard(self, card_reader)
        self.register_card.abort.connect(self._abort)
        self.register_card.save.connect(self.card_next)
        self.stacked_layout.addWidget(self.register_card)

        self.stacked_layout.setCurrentIndex(0)

    def clear(self):
        self.username = ""
        self.register_card.clear()
        self.register_card.deactivate()
        self.name_input.clear()
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
        self.username = username
        self.stacked_layout.setCurrentIndex(1)
        self.register_card.clear()
        self.register_card.activate()

    @exc
    def card_next(self, code: str):
        self.register_card.clear()
        self.register_card.deactivate()

        assert self.username
        self.card_db.register(code, self.username)
        self.clear()
        self.success.emit()
