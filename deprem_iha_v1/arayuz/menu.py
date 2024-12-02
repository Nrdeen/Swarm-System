from PyQt5.QtWidgets import QFrame, QPushButton, QLabel,QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import requests

class Menu(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(0, 0, self.parent.width(), self.parent.MENU_HEIGHT)
        self.setStyleSheet("color: #E8CDB3;")
        self.create_menu()
        self.update_weather_data()  # Hava durumu verilerini güncellemek için

        # QTimer oluştur ve başlat
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_satellite_status)

    def create_menu(self):
        self.drone_connect_button = QPushButton("Bağlan", self)
        self.drone_connect_button.setGeometry(1750, 10, 140, 60)
        self.drone_connect_button.clicked.connect(self.parent.connect_drone)
        self.drone_connect_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(232, 205, 179, 180), stop:1 rgba(7, 9, 68, 180));
                color: white;
                font: bold 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(232, 205, 179, 255), stop:1 rgba(7, 9, 68, 255));
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(232, 205, 179, 200), stop:1 rgba(7, 9, 68, 200));
            }
        """)

        # ComboBox ekleme
        self.comboBox = QComboBox(self)
        
        

        # Profesyonel görünüm için stil ayarları
        self.comboBox.setStyleSheet("""
            QComboBox {
                border: 1px solid #050947;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
                background-color: #E6CDB4;
                color: #050947;
            }
            QComboBox:editable {
                background: #E6CDB4;
                color: #050947;
            }
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: #E6CDB4;
                color: #050947;
            }
            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                background: #E6CDB4;
                color: #050947;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 18px;
                border-left-width: 1px;
                border-left-color: #050947;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(/path/to/your/down-arrow-icon.png); /* İkon dosya yolunu kendi ikon yolunuzla değiştirin */
            }
            QComboBox::down-arrow:on {
                top: 1px;
                left: 1px;
            }
        """)




        # ComboBox ekleme
        self.comboBox_baud = QComboBox(self)
         # Profesyonel görünüm için stil ayarları
        self.comboBox_baud.setStyleSheet("""
            QComboBox {
                border: 1px solid #050947;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
                background-color: #E6CDB4;
                color: #050947;
            }
            QComboBox:editable {
                background: #E6CDB4;
                color: #050947;
            }
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: #E6CDB4;
                color: #050947;
            }
            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                background: #E6CDB4;
                color: #050947;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 18px;
                border-left-width: 1px;
                border-left-color: #050947;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(/path/to/your/down-arrow-icon.png); /* İkon dosya yolunu kendi ikon yolunuzla değiştirin */
            }
            QComboBox::down-arrow:on {
                top: 1px;
                left: 1px;
            }
        """)
        
        temperature_icon = QLabel(self)
        temperature_icon.setGeometry(60, 10, 60, 60)
        temperature_icon.setPixmap(QPixmap("./img/menu/temperature.png"))
        self.temperature_status_label = QLabel("-", self)
        self.temperature_status_label.setGeometry(130, 10, 100, 60)

        self.add_divider(230)

        self.wifi_icon = QLabel(self)
        self.wifi_icon.setGeometry(240, 10, 60, 60)
        self.wifi_icon.setPixmap(QPixmap("./img/menu/wifi.png"))

        self.firtina = QLabel(self)
        self.firtina.setGeometry(630, 955, 80, 80)
        self.firtina.setPixmap(QPixmap("./img/arkaplan/icon1.png"))

        self.wifi_status_label = QLabel("Bağli Değil", self)
        self.wifi_status_label.setGeometry(310, 10, 200, 60)

        self.add_divider(410)

        self.battery_icon = QLabel(self)
        self.battery_icon.setGeometry(420, 10, 60, 60)
        self.battery_icon.setPixmap(QPixmap("./img/menu/battery.png"))
        self.battery_status_label = QLabel("0%", self)
        self.battery_status_label.setGeometry(490, 10, 100, 60)

        self.add_divider(580)

        weather_icon = QLabel(self)
        weather_icon.setGeometry(590, 10, 60, 60)
        self.weather_icon = weather_icon
        self.weather_status_label = QLabel("-", self)
        self.weather_status_label.setGeometry(660, 10, 200, 60)

        self.add_divider(760)

        wind_icon = QLabel(self)
        wind_icon.setGeometry(770, 10, 60, 60)
        wind_icon.setPixmap(QPixmap("./img/menu/wind.png"))
        self.wind_status_label = QLabel("-", self)
        self.wind_status_label.setGeometry(840, 10, 200, 60)



        self.connecting_label = QLabel('Bağlanıyor...', self)
        self.notconnecting_label = QLabel('Bağlantı kesiliyor...', self)
        
        self.connecting_label.setAlignment(Qt.AlignCenter)
        self.connecting_label.setStyleSheet("font-size: 24px; color: white; background-color: black;")

        self.notconnecting_label.setAlignment(Qt.AlignCenter)
        self.notconnecting_label.setStyleSheet("font-size: 24px; color: white; background-color: black;")

        self.ucur = QPushButton("Uçur", self)
        self.ucur.setGeometry(1430, 10, 140, 60)
        self.ucur.clicked.connect(self.parent.ucur)
        self.ucur.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(232, 205, 179, 180), stop:1 rgba(7, 9, 68, 180));
                color: white;
                font: bold 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(232, 205, 179, 255), stop:1 rgba(7, 9, 68, 255));
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(232, 205, 179, 200), stop:1 rgba(7, 9, 68, 200));
            }
        """)
    def add_divider(self, x_pos):
        line = QFrame(self)
        line.setGeometry(x_pos, 10, 2, 60)
        line.setStyleSheet("background-color: #E8CDB3;")   
        
    def update_weather_data(self):
    # OpenWeatherMap API key ve istek URL'si
        api_key = "3a4f58f1c915b6b4d06541083a240453"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Change the city name to "Bartın"
        city_name = "Bartın"
        complete_url = f"{base_url}q={city_name}&appid={api_key}&lang=tr&units=metric"

    # API'den istek yapma
        response = requests.get(complete_url)
        data = response.json()

    # Hava durumu ve rüzgar bilgilerini al
        if data["cod"] != "404":
            weather_desc = data["weather"][0]["description"].capitalize()
            wind_speed = data["wind"]["speed"]
            temperature = data["main"]["temp"]

        # Hava durumu, rüzgar ve sıcaklık bilgisini güncelle
            self.weather_status_label.setText(weather_desc)
            self.wind_status_label.setText(f"{wind_speed} m/s")
            self.temperature_status_label.setText(f"{temperature} °C")

        # Hava durumuna göre ikonu ayarla
            weather_code = data["weather"][0]["icon"]
            self.set_weather_icon(weather_code)
        else:
           print("Şehir bulunamadı!")
    


    def set_weather_icon(self, weather_code):
        # Hava durumu koduna göre uygun ikonu ayarla
        if weather_code == "01d":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/gunes.png"))
        elif weather_code == "01n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/gece.png"))
        elif weather_code == "02d":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/parcalibulut.png"))
        elif weather_code == "02n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/gece.png"))
        elif weather_code == "03d" or weather_code == "03n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/parcalibulut.png"))
        elif weather_code == "04d" or weather_code == "04n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/bulutlu.png"))
        elif weather_code == "09d" or weather_code == "09n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/yagmur.png"))
        elif weather_code == "10d":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/yagmur.png"))
        elif weather_code == "10n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/yagmur.png"))
        elif weather_code == "11d" or weather_code == "11n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/firtina.png"))
        elif weather_code == "13d" or weather_code == "13n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/karli.png"))
        elif weather_code == "50d" or weather_code == "50n":
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/sisli.png"))
        else:
            self.weather_icon.setPixmap(QPixmap("./img/havadurumu/other.png"))  # Diğer durumlar için genel bir ikon

    def update_satellite_status(self):
        # Pixhawk'tan uydu sinyali bilgisini al
        if self.parent.baglanti.vehicle:
            satellite_count = self.parent.baglanti.vehicle.gps_0.satellites_visible
            if satellite_count is not None:
                self.satellite_status_label.setText(f"{satellite_count} Uydu")
            else:
                self.satellite_status_label.setText("Sinyal Yok")
        else:
            self.satellite_status_label.setText("Sinyal Yok")
