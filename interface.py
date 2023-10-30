import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QFileDialog, QLabel, QVBoxLayout

from ai import LicensePlateDetector


class RandomString(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ai = LicensePlateDetector()

    def initUI(self):
        self.setGeometry(0, 0, 600, 600)

        self.btn = QPushButton('Выбрать фото', self)
        self.btn.clicked.connect(self.load_image)
        self.setWindowTitle('Детектор номеров')
        self.text_label = QLabel('Изображение:', self)
        self.text_label.move(10, 30)
        self.text_label.show()
        self.layout = QVBoxLayout()
        self.layout.addStretch()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)')
        if file_name:
            self.n_detected = self.ai.run(file_name)
            print(self.n_detected)
            from PIL import Image
            image = Image.open(file_name)
            for j in self.ai.coords:
                cropped_image = image.crop(j)
                cropped_image.save(f'{j}.png')
                label = QLabel()
                pixmap = QPixmap(f'{j}.png')
                label.setPixmap(pixmap)
                self.layout.addWidget(label)
                os.remove(f'{j}.png')
            self.setLayout(self.layout)
            self.layout.addStretch()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RandomString()
    ex.show()
    sys.exit(app.exec())
