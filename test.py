import os
import sys
import threading

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QVBoxLayout

from ai import LicensePlateDetector


class Detector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def b(self):
        self.ai = LicensePlateDetector()

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)

        self.btn = QPushButton('Выбрать фото', self)
        self.btn.clicked.connect(self.load_image)
        self.setWindowTitle('Детектор номеров')
        self.label1 = QLabel('Изображение:', self)
        self.label1.move(10, 30)
        self.label1.show()
        self.layout1 = QVBoxLayout()
        self.layout1.addStretch()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_name:
            def detector():
                self.n_detected = self.ai.run(file_name)

            def a():

                from PIL import Image

                image = Image.open(file_name)

                self.label2 = QLabel(self)
                self.label2.setText('\n'.join(self.ai.reader()))
                self.label2.show()

                for j in self.ai.coords:
                    cropped_image = image.crop(j)
                    cropped_image.save(f'{j}.png')

                    label1 = QLabel()
                    pixmap = QPixmap(f'{j}.png')
                    label1.setPixmap(pixmap)
                    self.layout1.addWidget(label1)
                    self.layout1.addWidget(self.label2)

                    os.remove(f'{j}.png')
                self.setLayout(self.layout1)
                self.layout1.addStretch()

            t3 = threading.Thread(target=detector)
            t4 = threading.Thread(target=a)
            t3.start()
            t4.start()
            t3.join()
            t4.join()


def run_program():
    app = QApplication(sys.argv)
    ex = Detector()
    ex.show()
    sys.exit(app.exec())


# def init():
#     ai = LicensePlateDetector()


if __name__ == '__main__':
    ai_thread = threading.Thread(target=run_program)
    # t2 = threading.Thread(target=init)
    t5 = threading.Thread(target=Detector.b)
    ai_thread.start()
    t5.start()
    # t2.start()
    ai_thread.join()
    t5.join()
    # t2.join()
