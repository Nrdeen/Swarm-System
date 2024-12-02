import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox,QLineEdit,QLabel
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QIcon,QPixmap
from menu import Menu
from map import Map
from custom_boxes import CustomBoxes
from background import Background
from gosterge import Gosterge
from ihaBaglan  import Baglan
import time
from dronekit import VehicleMode
import serial.tools.list_ports
import math


class Main(QMainWindow):
    def __init__(self):
        self.konum_alindi = False  # Bayrak başlangıçta False olarak ayarlanır
        super().__init__()

        self.setWindowTitle("SKY BRIDGE Swarm System")
        self.setMinimumSize(QSize(1200, 900))
        self.setWindowIcon(QIcon('./img/arkaplan/icon.png'))
        self.resize(1900,980)

        # Sabitler
        self.BUTTON_GAP = 20
        self.HORIZONTAL_GAP = 50
        self.FOOTER_HEIGHT = 80
        self.MENU_HEIGHT = 80

        # Arka planı ayarla
        self.background = Background(self)      

        # Ana widget'i oluştur ve ayarla
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Menü, özel kutular, harita ve kamera bileşenlerini oluştur
        self.menu = Menu(self)
        self.custom_boxes = CustomBoxes(self)
        self.map = Map(self)

      # Özel kutuların ve kamera widget'inin geometrisini ayarla
        custom_boxes_y = self.MENU_HEIGHT + self.BUTTON_GAP * 2 + 250 * 2
        custom_boxes_height = self.height() - self.MENU_HEIGHT - self.FOOTER_HEIGHT - self.BUTTON_GAP * 2 - 250 * 2
        self.custom_boxes.setGeometry(0, custom_boxes_y, self.width(), custom_boxes_height)
        self.custom_boxes.setStyleSheet("background-color: transparent;")
    

        image_path = "img/gostergeler/"

        self.gosterge1 = Gosterge(self.centralWidget, image_path, "0, 70, 300, 300", "0.png", "ibre.png")
        self.gosterge2 = Gosterge(self.centralWidget, image_path, "0, 380, 300, 300", "2.png", "drone_on.png", ["nokta.png"])
        self.gosterge3 = Gosterge(self.centralWidget, image_path, "0, 690, 300, 300", "1.png", "ibre.png")
        self.gosterge4 = Gosterge(self.centralWidget, image_path, "301, 70, 300, 300", "3.png", "drone_ust.png")
        self.gosterge5 = Gosterge(self.centralWidget, image_path, "301, 380, 300, 300", "dis_cerceve1.png","ic2.png",["d2.png"])
        self.gosterge6 = Gosterge(self.centralWidget, image_path, "301, 690, 300, 300", "5.png", "ibre.png")
        
         # Gosterge widget'ının konumu ve boyutu hangi açıda başlasın 
         
        self.gosterge1.setRotation( 3.6 +53)
        self.gosterge6.setRotation( 3.6 +53)
        self.gosterge3.setRotation(3.6 +177)
       


        self.menu.comboBox.setGeometry(1590, 10, 150, 25)  # Konum ve boyut ayarları
        self.menu.comboBox.currentIndexChanged.connect(self.comboBoxChanged)

        self.menu.comboBox_baud.setGeometry(1590, 40, 150, 25)  # Konum ve boyut ayarları
        self.menu.comboBox_baud.currentIndexChanged.connect(self.comboBoxChanged_baud)
        self.menu.comboBox_baud.addItem("57600")
        self.menu.comboBox_baud.addItem("115200")

        # COM portlarını tarayıp listeleme
        self.list_serial_ports()

        self.baglanti = Baglan()  # Bağlanma işlemini değişkene ata

        # havaHizyaz widget'ının boyutunu ve konumunu gosterge1'in üstüne yerleştirme
        self.havahizyaz = QLineEdit("0.00 m/s", self)
        self.havahizyaz.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.havahizyaz.setGeometry(120,267, 70, 25)
        self.havahizyaz.raise_()

        # Dikey Hizyaz widget'ının boyutunu ve konumunu gosterge1'in üstüne yerleştirme
        self.dikeyhizyaz = QLineEdit("0.00 m/s", self)
        self.dikeyhizyaz.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.dikeyhizyaz.setGeometry(418,890, 70, 25)
        self.dikeyhizyaz.raise_()



        # Yükseklik widget'ının boyutunu ve konumunu gosterge1'in üstüne yerleştirme
        self.Yukseklikyaz = QLineEdit("0.00 m", self)
        self.Yukseklikyaz.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.Yukseklikyaz.setGeometry(120,885, 70, 25)
        self.Yukseklikyaz.raise_()

        # CUSTOM BOXES KUTU İÇERİKLERİ
        # longitude widget'ının boyutunu ve konumunu gosterge1'in üstüne yerleştirme
        self.longitudeyaz = QLineEdit("0.00000", self)
        self.longitudeyaz.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.longitudeyaz.setGeometry(635,765, 100, 25)
        self.longitudeyaz.raise_()


         # latitude widget'ının boyutunu ve konumunu gosterge1'in üstüne yerleştirme
        self.latitudeYaz = QLineEdit("0.00000", self)
        self.latitudeYaz.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.latitudeYaz.setGeometry(770,765, 100, 25)
        self.latitudeYaz.raise_()

        # Yükseklik widget'ının boyutunu ve konumunu gosterge1'in üstüne yerleştirme
        self.Yukseklikyaz2 = QLineEdit("0.00", self)
        self.Yukseklikyaz2.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.Yukseklikyaz2.setGeometry(920,765, 100, 25)

        self.hizyaz = QLineEdit("0.00 m/s", self)
        self.hizyaz.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.hizyaz.setGeometry(780,950, 100, 35)
        self.hizyaz.raise_()


        self.Armed = QLineEdit("KALKMADI", self)
        self.Armed.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.Armed.setGeometry(790,855, 100, 35)
        self.Armed.raise_()

        self.Guided = QLineEdit("NONE", self)
        self.Guided.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 15px;
            }
        """)
        self.Guided.setGeometry(650,855, 100, 35)
        self.Guided.raise_()

        self.Aracmodu = QLineEdit("Hava aracı", self)
        self.Aracmodu.setStyleSheet("""
            QLineEdit {
                background-color:transparent;
                color: darkblue;
                border:none;
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)
        self.Aracmodu.setGeometry(920,850, 100, 45)
        self.Aracmodu.raise_()


        # Timer for updating speed and altitude every 0.5 seconds
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_drone_values) 
        self.update_timer.start(300)


        # Bağlanıyor etiketi oluştur ve gizle
       
        self.menu.connecting_label.setGeometry(1200,20, 250, 30)
        self.menu.connecting_label.hide()

        self.menu.notconnecting_label.setGeometry(1200,20, 250, 30)
        self.menu.notconnecting_label.hide()


    def list_serial_ports(self):
        # ports = serial.tools.list_ports.comports()
        # if ports:
        #     for port in ports:
        #         print(f"Found port: {port.device}")  # Hata ayıklama çıktısı
        #         self.menu.comboBox.addItem(port.device)
        # else:
        #     print("No COM ports found")  # Hata ayıklama çıktısı
        #     # Manuel olarak ekleme
        self.menu.comboBox.addItem("UDP")
        self.menu.comboBox.addItem("COM4")
        self.menu.comboBox.addItem("COM5")
        self.menu.comboBox.addItem("COM6")
    

    def comboBoxChanged(self, index):
        self.secilen_port = self.menu.comboBox.currentText()
        print(f"Selected index: {index}, Selected item: {self.secilen_port}")

    
    def comboBoxChanged_baud(self, index):
        self.secilen_baud = self.menu.comboBox_baud.currentText()
        print(f"Selected index: {index}, Selected item: {self.secilen_baud}")

   

    def resizeEvent(self, event):
        # Menünün yerinin ayarlanması
        self.menu.setGeometry(0, 0, self.width(), self.MENU_HEIGHT)

        # Arkaplan resminin ayarlanması
        self.background.label.setGeometry(0, 0, self.width(), self.height())
        
        # Map'in yerinin ayarlanması
        self.map.setGeometry(0, 0, self.width(), self.height())
    
        # Veri kutucuklarının ayarlanması
        horizontal_margin = 200
        custom_boxes_width = (self.width() - 3 * horizontal_margin) // 3
        custom_boxes_left = self.HORIZONTAL_GAP + 250 + 300  # 300 piksel sağa kaydırıldı
    
        if self.width() < self.minimumSize().width():
            custom_boxes_left = (self.width() - custom_boxes_width * 2 - horizontal_margin) // 2
    
        # custom_boxes'ın yüksekliğini azaltmak için ayarlama yapıyoruz
        custom_boxes_height = self.height() - self.MENU_HEIGHT - self.FOOTER_HEIGHT - self.BUTTON_GAP * 2 - 510
    
        self.custom_boxes.setGeometry(
            custom_boxes_left, 
            self.MENU_HEIGHT + self.BUTTON_GAP * 5 + 525, 
            custom_boxes_width, 
            custom_boxes_height
        )

        #self.camera_widget.setGeometry(
          #  self.HORIZONTAL_GAP + 980, 
           # self.MENU_HEIGHT + self.BUTTON_GAP * 5 + 525, 
          #  880, 
          #  300
        #)   
        
        event.accept()  

    

    def connect_drone(self):
        try:

            # Bağlanıyor etiketi göster
            self.menu.connecting_label.show()
            baud = self.secilen_baud
            print("Seçili COM baud:", baud)  # Hata ayıklama çıktısı

            #QApplication.processEvents()  # Arayüz güncellemesi için


            # Eğer zaten bir bağlantı varsa, tekrar bağlantı yapma
            if not self.baglanti.vehicle:
                udp_endpoint = '192.168.2.2:14550'
                self.baglanti.connect_drone_iha(udp_endpoint,baud )
                
               
                self.menu.wifi_status_label.setText("Bağlandı")
                self.menu.wifi_status_label.setStyleSheet("color: lightgreen;")
                self.menu.wifi_icon.setPixmap(QPixmap("./img/menu/wifi_yesil.png"))

                self.menu.drone_connect_button.setText("Bağlantiyi Kes")
                
                
            else:
                self.menu.wifi_status_label.setText("Bağlanti Kesildi")
                self.menu.wifi_status_label.setStyleSheet("color: orange;")
                self.menu.wifi_icon.setPixmap(QPixmap("./img/menu/wifi_red.png"))
                self.disconnect_drone()
        except Exception as e:
            # Bağlantı hatası durumunda
            self.menu.wifi_status_label.setText("Bağlanmadı")
            self.menu.wifi_status_label.setStyleSheet("color: red;")
            self.menu.wifi_icon.setPixmap(QPixmap("./img/menu/wifi_red.png"))
            print(f"Bağlantı hatası: {e}")

        finally:
            # Bağlanıyor etiketi gizle
            self.menu.connecting_label.hide()

            
    def ucur(self):
 
        # Takeoff ve görev ekleme fonksiyonlarını çağır
        self.baglanti.takeoff(0.5)
        self.update_drone_values()
        iha = self.baglanti.vehicle
        if self.baglanti.vehicle.armed == True:
            self.Armed.setText("Uçuş Aktif")

        if self.baglanti.vehicle.mode == VehicleMode("GUIDED"):
            self.Guided.setText("Yönlendirildi")

        if self.baglanti.vehicle.armed == False:
            self.Aracmodu.setText("KARA aracı  ")
    
           

        self.baglanti.vehicle.commands.next = 0
        self.baglanti.vehicle.mode = VehicleMode("AUTO")

        while not iha.armed:
            next_waypoint = self.baglanti.vehicle.commands.next
            print(f"Sıradaki komut {next_waypoint}")
            self.update_drone_values()
            time.sleep(1)
            if next_waypoint == 5:
                print("Görev bitti.")
                iha.armed = False  # Dronu silahsızlandır
                break

        print("Döngüden çıkıldı.")

        if not self.baglanti.vehicle.armed:  # Dron silahsızlandırıldıktan sonra kontrol edilir
            self.Aracmodu.setText("KARA aracı")

    
    def disconnect_drone(self):
        try:
            # Bağlantıyı kesme işlemleri burada yapılacak
            self.baglanti.disconnect()
            self.menu.notconnecting_label.show()
            QApplication.processEvents()  # Arayüz güncellemesi için
            print("Drone bağlantısı kesiliyor...")
            self.menu.drone_connect_button.setText("Tekrar bağlan")

        except Exception as e:
            # Bağlantı hatası durumunda
            self.menu.wifi_status_label.setText("Bağlantı kesilmedi")
            self.menu.wifi_status_label.setStyleSheet("color: red;")
            self.menu.wifi_icon.setPixmap(QPixmap("./img/menu/wifi_red.png"))
            print(f"Bağlantı hatası: {e}")

        finally:
            # Bağlanıyor etiketi gizle
            self.menu.notconnecting_label.hide()

        
    def konumver(self):
        if not self.konum_alindi:  # Bayrak kontrolü
            if self.baglanti.vehicle:
                self.konumX = self.baglanti.Konum()
                print(f"1 adet Alınan KonumMMM: {self.konumX}")
                
                # Konumu map.py'deki bir metoda gönder
                self.map.get_konum(self.konumX)
                
                self.konum_alindi = True  # Bayrak True olarak ayarlanır, böylece metod tekrar çalıştırılmaz


    def Dronekonum(self):
        if self.baglanti.vehicle:
                self.konumX = self.baglanti.Konum()
                self.yawdeger = self.baglanti.get_attitude()
                self.yaw = self.yawdeger['yaw']
                print(f"1 adet Alınan Dronekonum KonumMMM: {self.konumX},{self.yaw}")
                
                # Konumu map.py'deki bir metoda gönder
                self.map.get_konumDrone(self.konumX,self.yaw)


    def update_battery_status(self):
        battery_status = self.baglanti.get_battery_status()
        print(f"Update battery status: {battery_status}")
        if battery_status and "seviye" in battery_status:
            battery_level = battery_status["seviye"]
            if battery_level is not None:
                self.menu.battery_status_label.setText(f"{battery_level}%")
                # self.update_battery_icon(battery_level)
            else:
                # Batarya seviyesi None ise
                self.menu.battery_status_label.setText("N/A")
                self.menu.battery_icon.setPixmap(QPixmap("./img/menu/batarya_red.png"))
        else:
            # Batarya durumu alınamadığında veya eksik olduğunda yapılacaklar
            self.menu.battery_status_label.setText("N/A")
            self.menu.battery_icon.setPixmap(QPixmap("./img/menu/batarya_red.png"))
      
    def update_drone_values(self):
        if self.baglanti.vehicle:
            # Hız vektörünü al
            velocity = self.baglanti.get_airspeed()

            # x, y, z hız bileşenlerini al

            self.airspeed_x = velocity[0]
            self.airspeed_y = velocity[1]
            self.airspeed_z = velocity[2]

            #Hızın büyüklüğünü hesapla

            self.airspeed = math.sqrt(self.airspeed_x**2 + self.airspeed_y**2 + self.airspeed_z**2)

            self.ground_speed = self.baglanti.get_ground_speed()
            self.dikey_hiz = self.baglanti.get_vertical_speed_status()
            self.batarya = self.baglanti.get_battery_status()
            self.altitude = self.baglanti.yukseklik()
            self.konumX = self.baglanti.Konum()
            print(f"Alınan Konum: {self.konumX}")

            # Konumu map.py'deki bir metoda gönder
            #self.map.get_konum(self.konumX)
            

            self.konumyaz(self.konumX)

            
            self.konumver()
            self.Dronekonum()


            print(f"Ground Speed: {self.ground_speed} m/s, Altitude: {self.altitude} m")

            print(f"KOnum: {self.konumX} ")
            
            print(f"Dikey Hız: {self.dikey_hiz} ")


            self.havahizyaz.setText(f"{self.airspeed:.2f} m/s")
            self.hizyaz.setText(f"{self.ground_speed:.2f}")
            self.Yukseklikyaz.setText(f"{self.altitude:.2f}")
            self.dikeyhizyaz.setText(f"{self.dikey_hiz:.2f}") 
            self.Yukseklikyaz2.setText(f"{self.altitude:.2f}")  


            if self.baglanti.vehicle.armed == True:
                self.Armed.setText("Uçuş Aktif")
            else :
                self.Armed.setText("Kalkmadı")

            if self.baglanti.vehicle.mode == VehicleMode("GUIDED"):
                self.Guided.setText("Yönlendirildi")
            else :
                self.Guided.setText("---")


            if self.baglanti.vehicle.armed == False:
                self.Aracmodu.setText("KARA aracı  ")

            else :
                self.Aracmodu.setText("HAVA Aracı")
             
            self.HIZ_gösterge_rotasyonunu_güncelle()

            # Ufuk göstergesini güncelle 
            self.update_horizon()

            # yukseklik göstergesini güncelle
            self.Yukseklik_gösterge_rotasyonunu_güncelle()

            # Dikey_HIZ göstergesini güncelle
            self.Dikey_HIZ_gösterge_rotasyonunu_güncelle()

            self.update_battery_status()

            

    def konumyaz(self, konum):
        try:
            latitude, longitude = map(float, konum.split(','))
            self.latitude = latitude
            self.longitude = longitude

            self.latitudeYaz.setText(f"{self.latitude:.4f}")
            self.longitudeyaz.setText(f"{self.longitude:.4f}")
            print(f"MAİNDEKİ konum .py'de güncellenen konum: {self.latitude}, {self.longitude}")
        except ValueError:
            print("Geçersiz konum formatı.")
        except Exception as e:
            print(f"Hata oluştu: {e}")        
    


    def HIZ_gösterge_rotasyonunu_güncelle(self):
        # Minimum ve maksimum dönme açıları
        min_aci = 53
        max_aci = 304
        
        # Ground speed aralığı
        min_speed = 0
        max_speed = 10
        
        # Ground speed'e göre dönme miktarını hesapla
        rotation = ((self.ground_speed - min_speed) / (max_speed - min_speed)) * (max_aci - min_aci) + min_aci
        
        # Göstergeyi döndür
        self.gosterge1.setRotation(rotation)
        
        print(f"hız açı: {rotation} degrees")
        print(f"hız : {self.ground_speed} ")


    def Dikey_HIZ_gösterge_rotasyonunu_güncelle(self):
        # Minimum ve maksimum dönme açıları
        min_aci = 53
        max_aci = 304
        
        # Ground speed aralığı
        min_speed = -5
        max_speed = 5
        
        # Ground speed'e göre dönme miktarını hesapla
        rotation = ((self.dikey_hiz - min_speed) / (max_speed - min_speed)) * (max_aci - min_aci) + min_aci
        
        # Göstergeyi döndür
        self.gosterge6.setRotation(rotation)
        
        print(f"dikey hız: {rotation} degrees")
        print(f"dikey hız: {self.dikey_hiz} ")


    def Yukseklik_gösterge_rotasyonunu_güncelle(self):
        # Minimum ve maksimum dönme açıları
        min_aci = 177
        max_aci = 537
        
        # yukseklik aralığı
        min_h = 0
        max_h = 40
        
        # Ground speed'e göre dönme miktarını hesapla
        rotation = ((self.altitude - min_h) / (max_h - min_h)) * (max_aci - min_aci) + min_aci
        
        # Göstergeyi döndür
        self.gosterge3.setRotation(rotation)
        
        print(f"yukseklik: {rotation} degrees")
        print(f"yukseklik: {self.altitude} ")


    def update_horizon(self):
        if self.baglanti.vehicle: 
            self.attitude = self.baglanti.get_attitude()
            roll = self.attitude['roll']
            pitch = self.attitude['pitch']  
            yaw = self.attitude['yaw']
            
            # Ufuk ekranını güncellemek için roll ve pitch değerlerini kullanın
            self.gosterge5.setRoll(roll)
            self.gosterge5.setPitch(pitch)
            self.gosterge4.setYaw(yaw)

            self.gosterge2.setRoll(roll)

            print(f"Horizon updated - Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}")          

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())