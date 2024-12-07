
from dataclasses import dataclass
from datetime import datetime
from typing import List, Union
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFontMetrics, QResizeEvent
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QStackedLayout, QScroller, QScrollArea, QHBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt5.QtWidgets import QWidget
from fjaelllada.totp_auth import TotpDatabase
from fjaelllada.widgets.base import exc
from fjaelllada.card_auth import CardDatabase, db as card_db


@dataclass
class UserEntry:
    index: int
    name: str
    last_login: datetime


class EllipsisLabel(QLabel):
    text: str

    def __init__(self, text, parent):
        super().__init__(parent)
        self.setText(text)
    
    def updateText(self):
        metrics = QFontMetrics(self.font());
        super().setText(metrics.elidedText(self.text, Qt.TextElideMode.ElideRight, self.width()))
    
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        super().resizeEvent(a0)
        self.updateText()

    def setText(self, text):
        self.text = text
        self.updateText()


class UsersListEntry(QWidget):
    options = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        self.label = EllipsisLabel("User", self)
        self.label.setFixedWidth(190)
        layout.addWidget(self.label, stretch=1)
        button = QPushButton("Opt", self)
        layout.addWidget(button, stretch=0)
        button.clicked.connect(lambda *_: self.options.emit(self.user.index))
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        # self.setFixedSize(320, 40)
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    def set_user(self, user: UserEntry):
        self.user = user

        last_login_str = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
        self.label.setText(f"{self.user.name} {last_login_str}")


class UsersList(QWidget):
    options = pyqtSignal(int)
    user_entries: List[UsersListEntry]

    def __init__(self, parent):
        super().__init__(parent)

        self.vbox_layout = QVBoxLayout(self)
        self.vbox_layout.setSpacing(1)
        self.vbox_layout.setContentsMargins(1, 1, 1, 1)
        self.user_entries = []
    
    def update_users(self, users: List[UsersListEntry]):
        while len(self.user_entries) < len(users):
            user_widget = UsersListEntry(self)
            user_widget.options.connect(self.options)
            self.vbox_layout.insertWidget(len(self.user_entries), user_widget)
            self.user_entries.append(user_widget)
            user_widget.show()
        while len(self.user_entries) > len(users):
            user_widget = self.user_entries.pop()
            user_widget.deleteLater()
        for user, user_widget in zip(users, self.user_entries):
            user_widget.set_user(user)
        self.vbox_layout.update()
        self.update()
        self.updateGeometry()
        self.repaint()


class UserDetails(QWidget):
    finish = pyqtSignal()
    
    remove_user = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.name_label = QLabel("Name", self)
        layout.addWidget(self.name_label)

        self.last_login_label = QLabel("Last Login", self)
        layout.addWidget(self.last_login_label)

        remove_button = QPushButton("Remove", self)
        remove_button.clicked.connect(lambda *_: self.remove_user.emit(self.user.index))
        layout.addWidget(remove_button)

        back_button = QPushButton("←", self)
        back_button.clicked.connect(self.finish)
        layout.addWidget(back_button)
    
    def set_user(self, user: UserEntry):
        self.user = user

        self.name_label.setText(user.name)
        self.last_login_label.setText("Last Login: " + user.last_login.strftime("%Y-%m-%d %H:%M:%S"))
    
    def clear(self):
        self.name_label.setText("Name")
        self.last_login_label.setText("Last Login")



class ManageUsersPanel(QWidget):
    finished = pyqtSignal()

    def __init__(self, parent, db: Union[TotpDatabase, CardDatabase]):
        super().__init__(parent)

        self.users = []
        self.db = db

        self.stacked_layout = QStackedLayout(self)

        main = QWidget(self)
        main_layout = QVBoxLayout(main)

        top_bar_layout = QHBoxLayout()

        back_button = QPushButton("←")
        back_button.clicked.connect(self.finish)
        top_bar_layout.addWidget(back_button)

        main_layout.addLayout(top_bar_layout)
        
        scroll_area = QScrollArea(self)
        scroll_area.horizontalScrollBar().setEnabled(False)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        self.users_widget = UsersList(scroll_area)
        self.users_widget.options.connect(self.show_user_details)
        self.users_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        scroll_area.setWidget(self.users_widget)
        QScroller.grabGesture(scroll_area.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        main_layout.addWidget(scroll_area)

        self.stacked_layout.addWidget(main)

        self.user_details = UserDetails(self)
        self.user_details.finish.connect(self.show_main_list)
        self.user_details.remove_user.connect(self.remove_user)
        self.stacked_layout.addWidget(self.user_details)

        self.stacked_layout.setCurrentIndex(0)
    
    def update_users(self):
        self.users = [
            UserEntry(index=idx, name=user, last_login=last_login)
            for idx, (user, last_login) in enumerate(self.db.get_all())
        ]
        self.users_widget.update_users(self.users)

    @exc
    def show_main_list(self):
        self.stacked_layout.setCurrentIndex(0)
        self.user_details.clear()

    @exc
    def show_user_details(self, user_index: int):
        self.stacked_layout.setCurrentIndex(1)
        self.user_details.set_user(self.users[user_index])

    @exc
    def remove_user(self, user_index: int):
        self.show_main_list()
        del self.users[user_index]
        self.db.remove(user_index)
        for user in self.users[user_index:]:
            user.index -= 1
        self.users_widget.update_users(self.users)

    @exc
    def finish(self, *_):
        self.clear()
        self.finished.emit()

    def clear(self):
        self.stacked_layout.setCurrentIndex(0)
        self.users.clear()
        self.users_widget.update_users([])
        self.user_details.clear()
