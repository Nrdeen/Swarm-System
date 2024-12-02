from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QSize, QUrl, Qt
from map_viewer import MapViewer  # map_viewer dosyasından MapViewer sınıfını içe aktarın

class Map(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # MapViewer sınıfından bir örnek oluşturun
        self.map_view = MapViewer(self)
        self.konum = None

        # Layout oluşturun ve harita bileşenini layouta ekleyin
        layout = QVBoxLayout(self)
        layout.addWidget(self.map_view)

    # Pencere boyutu değiştiğinde yeniden boyutlandırmak için resizeEvent'i yeniden tanımlayın
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Haritanın boyutunu ayarla
        width = self.parent().width() * 6 // 7
        height = self.parent().height() * 4 // 7

        # Haritayı daha fazla kırpabilmek için belirli bir oranla boyutunu azalt
        width -= 350  # Örnek olarak 300 piksel sağdan ve soldan kırp
        height += 70
        self.resize(width, height)

        # Haritayı pencerenin tam ortasına taşı
        #self.move((self.parent().width() - width) // 2, (self.parent().height() - height) // 5)

        self.move(self.parent().width() - width, (self.parent().height() - height) // 5)

    
    
    def get_konumdeneme(self):
        return self.map_view.update_konum()
            
    def get_konum(self, konum):
        self.konum = konum
        print(f"Map.py'de güncellenen konum: {self.konum}")
        # Konumu map.py'deki bir metoda gönder
        self.map_view.update_konum(self.konum)
    
    

    def get_konumDrone(self, konum,yaw):
        self.konum = konum
        self.yaw = yaw
        print(f"Map.py'de güncellenen droneee konum: {self.konum} ,{self.yaw}")
        # Konumu map.py'deki bir metoda gönder
        self.map_view.update_konumDrone(self.konum,self.yaw)

        