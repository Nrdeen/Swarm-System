from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CustomBoxes(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Arka plan rengi ve gölge eklemesi
        self.setStyleSheet("background-color: #2c3e50; border-radius: 10px; border: 2px solid gray;")
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(5)

        # İçerik için düzen
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.create_info_boxes()

    def resizeEvent(self, event):
        # Pencere boyutu küçüldüğünde yazının boyutunu ayarla
        font_size = min(self.width(), self.height()) // 20
        font = QFont("Arial", font_size, QFont.Bold)
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setFont(font)

    def create_info_boxes(self):
        section_values = {
            "X": "",
            "Y": "",
            "İrtifa": "",
            "Kılavuz": "",
            "Kalkış": "",
            "Araç Modu" : "",
            "Hız": ""
        }

        hbox = QHBoxLayout()
        self.layout.addLayout(hbox)

        count = 0
        for section, value in section_values.items():
            if count % 3 == 0 and count != 0 :
                
                hbox = QHBoxLayout()
                self.layout.addLayout(hbox)

            box = QFrame()
            box.setStyleSheet("background-color: #E8CDB3; border-radius: 10px; border: 2px solid #070944;")
            box_layout = QVBoxLayout()
            box.setLayout(box_layout)

            section_label = QLabel(section)
            section_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            section_label.setFont(QFont("Arial", 12, QFont.Bold))
            box_layout.addWidget(section_label)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("background-color: #070944;")
            box_layout.addWidget(line)

            value_label = QLabel(value)
            value_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            value_label.setFont(QFont("Century Gothic", 16))
            box_layout.addWidget(value_label)

            hbox.addWidget(box)

            count += 1

            # Hover efekti için olaylar
            box.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Enter:
            obj.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #070944;")
        elif event.type() == event.Leave:
            obj.setStyleSheet("background-color: #E8CDB3; border-radius: 10px; border: 2px solid #070944;")

        return super().eventFilter(obj, event)
