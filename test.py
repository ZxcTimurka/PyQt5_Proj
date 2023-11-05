import sqlite3
import sys
import threading

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QVBoxLayout, QLineEdit

from ai import LicensePlateDetector


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.build()

    def build(self):
        con = sqlite3.connect('LicensePlates.db')
        cur = con.cursor()
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('База данных')
        self.bdt = QLineEdit(self)
        self.bdt.resize(40, 20)
        self.bdt.move(350, 250)
        self.bdbtn = QPushButton('Вывести', self)
        self.bdbtn.clicked.connect(self.print_im)
        self.bdbtn.resize(55, 20)
        self.bdbtn.move(340, 220)
        self.bdp = QVBoxLayout()
        self.bdl = QLabel(self)
        elems = []
        try:
            res = cur.execute('SELECT * FROM car_numbers').fetchall()
            for elem in res:
                elems.append(str(elem[:-1])[1:-1])
                self.bdl.setText('\n'.join(elems))
                self.bdl.show()
                self.bdp.addWidget(self.bdl)
            self.setLayout(self.bdp)
            con.close()
        except Exception as e:
            print(e)

    def print_im(self):
        try:
            con = sqlite3.connect('LicensePlates.db')
            cur = con.cursor()
            res = cur.execute(f'SELECT * FROM car_numbers WHERE id = "{self.bdt.text()}";').fetchall()
            for elem in res:
                path = (str(elem[3:])[2:-3])
            con.close()
            self.label = QLabel(self)
            pixmap = QPixmap(path)
            self.label.setPixmap(pixmap)
            self.label.move(200, 10)
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.show()
        except Exception as e:
            print(e)


class Detector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    @classmethod
    def b(self):
        self.ai = LicensePlateDetector()

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle('Детектор номеров')

        self.btn = QPushButton('Выбрать фото', self)
        self.btn.clicked.connect(self.load_image)
        self.label1 = QLabel('Изображение:', self)
        self.label1.move(10, 30)
        self.label1.show()
        self.layout1 = QVBoxLayout()
        self.layout1.addStretch()
        self.open_btn = QPushButton('БД', self)
        self.open_btn.move(100, 0)
        self.open_btn.clicked.connect(self.openWin)

    def openWin(self):
        self.secondWin = SecondWindow(self)
        self.secondWin.show()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_name:
            self.n_detected = self.ai.run(file_name)

            from PIL import Image

            image = Image.open(file_name)

            self.label2 = QLabel(self)
            self.text = '\n'.join(self.ai.reader())
            self.label2.setText(self.text)
            self.label2.show()

            for j in self.ai.coords:
                cropped_image = image.crop(j)
                # cropped_image.save(f'{j}.png')

                label1 = QLabel()
                pixmap = QPixmap(f'{j}.png')
                label1.setPixmap(pixmap)
                self.layout1.addWidget(label1)
                self.layout1.addWidget(self.label2)

            self.setLayout(self.layout1)
            self.layout1.addStretch()


def run_program():
    print('Loading')
    app = QApplication(sys.argv)
    ex = Detector()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    ai_thread = threading.Thread(target=run_program)
    t5 = threading.Thread(target=Detector.b)
    ai_thread.start()
    t5.start()
    ai_thread.join()
    t5.join()
