import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from fjaelllada.seil_locker.widgets.main_window import MainWindow


def main():
    # Create the application and show the pin input window
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DisableHighDpiScaling, True)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
