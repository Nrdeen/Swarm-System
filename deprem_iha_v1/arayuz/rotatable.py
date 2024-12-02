from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QWidget
from PyQt5.QtCore import QSize, QTimer , QPoint
from PyQt5.QtGui import QIcon, QPainter

class RotatableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._pixmap = None  # Pixmap'i tutmak için bir değişken ekleyin
        self._vertical_offset = 0
        self._horizontal_offset = 0  # Yatay konum için değişken ekle


    def paintEvent(self, event):
        if self._pixmap is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Resmin dönme merkezini hesaplayın
            center = self.rect().center()
            painter.translate(center)

            painter.rotate(self._angle)
            
            # Resmi çizmek için uygun bir alan ayarlayın
            pixmap_rect = self._pixmap.rect()
            pixmap_rect.moveCenter(QtCore.QPoint(self._horizontal_offset, self._vertical_offset))
            painter.drawPixmap(pixmap_rect, self._pixmap)
        else:
            super().paintEvent(event)

    def setRotation(self, angle):
        self._angle = angle
        self.update()

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()

    def setVerticalOffset(self, offset):
        self._vertical_offset = int(offset)
        self.update()

    def setHorizontalOffset(self, offset):
        self._horizontal_offset = int(offset)
        self.update()

    def move(self, x, y):
        super().move(x + self._horizontal_offset, y + self._vertical_offset)  # Yatay konumu da hesaba kat
