import card_auth
import totp_auth
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QStackedLayout
from PyQt5.QtWidgets import QWidget
from widgets.base import exc
from widgets.manage_users import ManageUsersPanel

from widgets.register import RegisterWidget


class AdminChoice(QWidget):
    register_admin = pyqtSignal()
    manage_admins = pyqtSignal()
    manage_users = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        # Create layout and add widgets
        register_admin_button = QPushButton("Register New Admin", self)
        register_admin_button.clicked.connect(self.register_admin)
        manage_admins_button = QPushButton("Manage Admins", self)
        manage_admins_button.clicked.connect(self.manage_admins)
        manage_users_button = QPushButton("Manage Users", self)
        manage_users_button.clicked.connect(self.manage_users)

        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(register_admin_button)
        layout.addWidget(manage_admins_button)
        layout.addWidget(manage_users_button)


class AdminPanel(QWidget):
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.stacked_layout = QStackedLayout(self)
        
        admin_choice = AdminChoice(self)
        admin_choice.register_admin.connect(self.register_admin)
        admin_choice.manage_admins.connect(self.manage_admins)
        admin_choice.manage_users.connect(self.manage_users)
        self.stacked_layout.addWidget(admin_choice)

        self.register_admin_widget = RegisterWidget(self)
        self.register_admin_widget.success.connect(self.finish)
        self.register_admin_widget.abort.connect(self.finish)
        self.stacked_layout.addWidget(self.register_admin_widget)

        self.manage_admins_widget = ManageUsersPanel(self, totp_auth.db)
        self.manage_admins_widget.finished.connect(self.finish)
        self.stacked_layout.addWidget(self.manage_admins_widget)

        self.manage_users_widget = ManageUsersPanel(self, card_auth.db)
        self.manage_users_widget.finished.connect(self.finish)
        self.stacked_layout.addWidget(self.manage_users_widget)

        self.stacked_layout.setCurrentIndex(0)

        # Set up timer for leaving
        self.clear_timer = QTimer(self)
        self.clear_timer.setSingleShot(True)
        self.clear_timer.start(300000)
        self.clear_timer.timeout.connect(self.finish)

    @exc
    def register_admin(self, *_):
        self.register_admin_widget.clear()
        self.stacked_layout.setCurrentIndex(1)
    
    @exc
    def manage_admins(self, *_):
        self.manage_admins_widget.clear()
        self.manage_admins_widget.update_users()
        self.stacked_layout.setCurrentIndex(2)

    @exc
    def manage_users(self, *_):
        self.manage_users_widget.clear()
        self.manage_users_widget.update_users()
        self.stacked_layout.setCurrentIndex(3)
    
    @exc
    def finish(self, *_):
        self.clear_timer.stop()
        self.clear()
        self.finished.emit()

    def clear(self):
        self.stacked_layout.setCurrentIndex(0)
        self.register_admin_widget.clear()
        self.manage_admins_widget.clear()
        self.manage_users_widget.clear()
