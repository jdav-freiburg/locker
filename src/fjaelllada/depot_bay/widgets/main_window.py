from pathlib import Path

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedLayout
from PyQt5.QtWidgets import QWidget

from fjaelllada import totp_db
from fjaelllada.widgets.base import exc
from fjaelllada.widgets.bay import BayWidget
from fjaelllada.widgets.pin_input import PinInput
from fjaelllada.depot_bay.register import RegisterWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Pin Input")
        self.showFullScreen()  # Set the window to fullscreen mode
        self.setGeometry(0, 0, 800, 480)
        self.setCursor(Qt.BlankCursor)

        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(self.create_layout())
        self.setCentralWidget(central_widget)
        self.setStyleSheet((Path(__file__).parent / "style.qss").read_text())

        # Set up timer for auto logout
        self.logout_timer = QTimer(self)
        self.logout_timer.setSingleShot(True)
        self.logout_timer.timeout.connect(self.logout)

        if auth.db.is_empty():
            self.show_register_page()

    @exc
    def create_layout(self):
        # Create stacked layout and add layouts
        stacked_layout = QStackedLayout()
        pin_input = PinInput(self)
        pin_input.pin_output.connect(self.pin_input)
        pin_input.setFont(QFont("Arial", 40))
        stacked_layout.addWidget(pin_input)
        bay_container = BayWidget(self)
        bay_container.close.connect(self.show_pin_page)
        bay_container.setFont(QFont("Arial", 20))
        stacked_layout.addWidget(bay_container)
        register_container = RegisterWidget(self)
        register_container.setFont(QFont("Arial", 10))
        register_container.success.connect(self.show_pin_page)
        register_container.close.connect(self.show_pin_page)
        stacked_layout.addWidget(register_container)
        stacked_layout.setCurrentIndex(0)
        return stacked_layout

    def logout(self):
        self.show_pin_page()

    def reset_logout_timer(self):
        self.logout_timer.stop()
        self.logout_timer.start(300000)

    @exc
    def pin_input(self, code: str):
        if len(code) == 7 and code[0] == "0":
            is_register = True
            code = code[1:]
        else:
            is_register = False
        if len(code) == 6 and totp_db.db.verify(code):
            if is_register:
                self.show_register_page()
            else:
                self.show_result_page()

    @exc
    def show_pin_page(self, *_):
        self.centralWidget().layout().setCurrentIndex(0)

    @exc
    def show_result_page(self, *_):
        # Start timer for logout
        self.reset_logout_timer()

        self.centralWidget().layout().setCurrentIndex(1)

    @exc
    def show_register_page(self, *_):
        self.centralWidget().layout().setCurrentIndex(2)
