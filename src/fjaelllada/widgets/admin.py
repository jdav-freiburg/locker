from typing import Optional
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QStackedLayout
from PyQt5.QtWidgets import QWidget
from fjaelllada.db.card_db import CardDatabase
from fjaelllada.db.totp_db import TotpDatabase
from fjaelllada.widgets.base import exc
from fjaelllada.widgets.manage_users import ManageUsersPanel
from fjaelllada.widgets.nfc_reader import NFCReader

from fjaelllada.widgets.register_admin import RegisterAdminWidget
from fjaelllada.widgets.register_user import RegisterUserWidget


class AdminChoice(QWidget):
    register_user = pyqtSignal()
    manage_users = pyqtSignal()
    register_admin = pyqtSignal()
    manage_admins = pyqtSignal()

    def __init__(self, parent, can_manage_users: bool):
        super().__init__(parent)

        # Create layout and add widgets
        register_user_button = QPushButton("Register New User", self)
        register_user_button.clicked.connect(self.register_user)
        if can_manage_users:
            manage_users_button = QPushButton("Manage Users", self)
            manage_users_button.clicked.connect(self.manage_users)
        register_admin_button = QPushButton("Register New Admin", self)
        register_admin_button.clicked.connect(self.register_admin)
        manage_admins_button = QPushButton("Manage Admins", self)
        manage_admins_button.clicked.connect(self.manage_admins)

        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(register_user_button)
        layout.addWidget(manage_users_button)
        layout.addWidget(register_admin_button)
        layout.addWidget(manage_admins_button)


class AdminPanel(QWidget):
    finished = pyqtSignal()

    def __init__(self, parent, card_reader: NFCReader, admin_db: TotpDatabase, user_db: Optional[CardDatabase], qr_size: int):
        super().__init__(parent)

        self.stacked_layout = QStackedLayout(self)
        
        admin_choice = AdminChoice(self, can_manage_users=user_db is not None)
        admin_choice.register_user.connect(self.register_user)
        admin_choice.manage_users.connect(self.manage_users)
        admin_choice.register_admin.connect(self.register_admin)
        admin_choice.manage_admins.connect(self.manage_admins)
        self.stacked_layout.addWidget(admin_choice)

        self.register_user_widget = RegisterUserWidget(self, card_reader, user_db)
        self.register_user_widget.success.connect(self.finish)
        self.register_user_widget.abort.connect(self.finish)
        self.stacked_layout.addWidget(self.register_user_widget)

        if user_db is not None:
            self.manage_users_widget = ManageUsersPanel(self, user_db)
            self.manage_users_widget.finished.connect(self.finish)
            self.stacked_layout.addWidget(self.manage_users_widget)

        self.register_admin_widget = RegisterAdminWidget(self, admin_db, qr_size)
        self.register_admin_widget.success.connect(self.finish)
        self.register_admin_widget.abort.connect(self.finish)
        self.stacked_layout.addWidget(self.register_admin_widget)

        self.manage_admins_widget = ManageUsersPanel(self, admin_db)
        self.manage_admins_widget.finished.connect(self.finish)
        self.stacked_layout.addWidget(self.manage_admins_widget)

        self.stacked_layout.setCurrentIndex(0)

        # Set up timer for leaving
        self.clear_timer = QTimer(self)
        self.clear_timer.setSingleShot(True)
        self.clear_timer.start(300000)
        self.clear_timer.timeout.connect(self.finish)

    @exc
    def register_user(self, *_):
        self.register_user_widget.clear()
        self.stacked_layout.setCurrentIndex(1)

    @exc
    def manage_users(self, *_):
        self.manage_users_widget.clear()
        self.manage_users_widget.update_users()
        self.stacked_layout.setCurrentIndex(2)

    @exc
    def register_admin(self, *_):
        self.register_admin_widget.clear()
        self.stacked_layout.setCurrentIndex(3)
    
    @exc
    def manage_admins(self, *_):
        self.manage_admins_widget.clear()
        self.manage_admins_widget.update_users()
        self.stacked_layout.setCurrentIndex(4)

    @exc
    def finish(self, *_):
        self.clear_timer.stop()
        self.clear()
        self.finished.emit()

    def clear(self):
        self.stacked_layout.setCurrentIndex(0)
        self.register_user_widget.clear()
        self.manage_users_widget.clear()
        self.register_admin_widget.clear()
        self.manage_admins_widget.clear()
