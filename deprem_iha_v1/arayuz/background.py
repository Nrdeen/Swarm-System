from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class Background:
    def __init__(self, parent):
        self.parent = parent
        self.label = QLabel(self.parent)
        self.image = QPixmap("./img/arkaplan/background2.png")
        self.label.setPixmap(self.image)
        self.label.setGeometry(0, 0, self.parent.width(), self.parent.height())
        self.label.setScaledContents(True)
