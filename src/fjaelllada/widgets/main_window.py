from pathlib import Path

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QStackedLayout
from PyQt5.QtWidgets import QWidget
from fjaelllada.bus import open_bay
from fjaelllada.card_auth import check_code

import totp_auth
from widgets.admin import AdminPanel
from widgets.base import exc
from widgets.message_dialog import MessageDialog
from widgets.nfc_reader import NFCReader
from widgets.pin_input import PinInput


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Control")
        self.showFullScreen()  # Set the window to fullscreen mode
        #self.setGeometry(0, 0, 320, 240)
        self.setFixedSize(320, 240)
        self.setCursor(Qt.BlankCursor)

        # Create stacked layout and add layouts
        self.stacked_layout = QStackedLayout()
        
        pin_input = PinInput(self)
        pin_input.pin_output.connect(self.check_pin)
        self.stacked_layout.addWidget(pin_input)

        self.card_reader = NFCReader()
        self.card_reader.read_card.connect(self.read_card)
        
        self.admin_panel = AdminPanel(self, self.card_reader)
        self.admin_panel.finished.connect(self.show_pin_page)
        self.stacked_layout.addWidget(self.admin_panel)

        # dbg_panel = ManageUsersPanel(self)
        # dbg_panel.finished.connect(self.show_pin_page)
        # dbg_panel.update_users()
        # self.stacked_layout.addWidget(dbg_panel)
        
        self.stacked_layout.setCurrentIndex(0)

        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)
        self.setStyleSheet((Path(__file__).parent / 'style.qss').read_text())

        # Set up timer for auto logout
        self.logout_timer = QTimer(self)
        self.logout_timer.setSingleShot(True)
        self.logout_timer.timeout.connect(self.logout)

        self.card_reader.start()

        if totp_auth.db.is_empty():
            self.show_admin_page()

    @exc
    def check_pin(self, code: str):
        if totp_auth.db.verify(code):
            self.show_admin_page()
        else:
            dlg = MessageDialog(self, "Invalid PIN", "Try again")
            dlg.buttons.accepted.connect(lambda *_: dlg.close())
            dlg.exec()

    @exc
    def read_card(self, card_code: str):
        if check_code(card_code):
            open_bay()
        else:
            print("Card not registered")

    def logout(self):
        self.show_pin_page()
        self.admin_panel.clear()
        if totp_auth.db.is_empty():
            self.show_admin_page()

    def reset_logout_timer(self):
        self.logout_timer.stop()
        self.logout_timer.start(300000)

    @exc
    def show_pin_page(self, *_):
        self.stacked_layout.setCurrentIndex(0)

    # @exc
    # def show_result_page(self, *_):
    #     # Start timer for logout
    #     self.reset_logout_timer()

    #     self.centralWidget().layout().setCurrentIndex(1)

    @exc
    def show_admin_page(self, *_):
        self.stacked_layout.setCurrentIndex(1)
