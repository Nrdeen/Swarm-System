from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QComboBox
from rotatable import RotatableLabel


class Gosterge:
    def __init__(self, centralWidget, image_path, position, image_file, rotatable_file=None, overlay_files=[]):
        self.panel_widget = QWidget(centralWidget)
        self.panel_widget.setGeometry(QtCore.QRect(*map(int, position.split(','))))
        self.panel_widget.setObjectName("panel_widget")

        self.label_out = QtWidgets.QLabel(centralWidget)
        self.label_out.setGeometry(QtCore.QRect(*map(int, position.split(','))))
        self.label_out.setPixmap(QtGui.QPixmap(image_path + image_file))
        self.label_out.setScaledContents(True)
        self.label_out.setAlignment(QtCore.Qt.AlignCenter)
        self.label_out.setObjectName("label_out")

        if rotatable_file: 

            self.label_in = RotatableLabel(centralWidget)
            self.label_in.setGeometry(QtCore.QRect(*map(int, position.split(','))))
            self.label_in.setPixmap(QtGui.QPixmap(image_path + rotatable_file))
            self.label_in.setAlignment(QtCore.Qt.AlignCenter)
            self.label_in.setObjectName("label_in")
        else:
            self.label_in = None

        self.overlay_labels = []
        for overlay_file in overlay_files:
            overlay_label = QtWidgets.QLabel(centralWidget)
            overlay_label.setGeometry(QtCore.QRect(*map(int, position.split(','))))
            overlay_label.setPixmap(QtGui.QPixmap(image_path + overlay_file))
            overlay_label.setScaledContents(True)
            overlay_label.setAlignment(QtCore.Qt.AlignCenter)
            overlay_label.setObjectName("overlay_label")
            self.overlay_labels.append(overlay_label)

            

        
        
        
        # Only raise label_out for gosterge5
        if image_file == "dis_cerceve1.png":
            self.label_out.raise_()  # Ensure this label is on top of all other labels
            

     #Döndürmeyi ayarla
    def setRotation(self, angle):
        if self.label_in:
            self.label_in.setRotation(angle)
        

      #  Yatay Ofseti ayarla
    def setHorizontalOffset(self, offset):
        if self.label_in:
            self.label_in.setHorizontalOffset(offset)
            self.label_in.update()

    # Dikey Ofseti ayarla
    def setVerticalOffset(self, ofset):
        if self.label_in:
            self.label_in.setVerticalOffset(ofset)
            self.label_in.update()

    def setRoll(self, roll):
        if self.label_in:
            # Roll değerine göre döndürme
            roll_degrees = roll * (180.0 / 3.14159265)  # Radyanları dereceye çevir
            self.label_in.setRotation(roll_degrees)

    def setPitch(self, pitch):
        if self.label_in:
            # Pitch değerine göre kaydırma
            pitch_ofset = pitch * 10  # Pitch değerini uygun bir ölçekle çarp
            self.setVerticalOffset(pitch_ofset)

    def setYaw(self, yaw):
        if self.label_in:
            # Yaw değerine göre döndürme
            yaw_derece = yaw * (180.0 / 3.14159265)  # Radyanları dereceye çevir
            self.setRotation(yaw_derece)