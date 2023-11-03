import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *


class SecondWindow(QtWidgets.QWidget):
    def __init__(self,
                 parent=None):  # если собрался передавать аргументы, то не забудь их принять (nameofargument, self, parent=None)
        super().__init__(parent, QtCore.Qt.Window)
        self.build()  # ну и передать в открывающееся окно соответственно (nameofargument, self)

    def build(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('NoTittle')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('NoTittle')

        self.btn = QPushButton('Butn', self)
        self.btn.resize(100, 100)
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.openWin)

    def openWin(self):
        self.secondWin = SecondWindow(self)
        self.secondWin.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
