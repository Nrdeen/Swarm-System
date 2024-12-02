from dronekit import connect, Command, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import serial.tools.list_ports
class Baglan:
    
    def __init__(self):
        self.vehicle = None  # Aracı temsil eden nesne
       

    def connect_drone_iha(self, udp_endpoint, baud):
        print(f"UDP uç noktasında {udp_endpoint} ve baud hızı {baud} ile drone'a bağlanılıyor...")
        
        # UDP kullanarak araca bağlan
        self.vehicle = connect(udp_endpoint, wait_ready=True, baud=baud)

        # Bağlantıyı kontrol etmek için araç versiyonunu yazdır
        print("Araca bağlandı: %s" % self.vehicle.version)

        # Bağlantı başarılı olduğunda True döndür
        return True

    

    def get_ground_speed(self):
        if self.vehicle:
            return self.vehicle.groundspeed
        else:
            return None
        
    def get_airspeed(self):
        if self.vehicle:
            return self.vehicle.velocity
        else:
            return None
        
    def get_vertical_speed_status(self):
        if self.vehicle:
            return self.vehicle.velocity[2]  # Dikey hız (Z ekseni)
        else:
            return None
        
    def yukseklik(self):
        if self.vehicle:
            return self.vehicle.location.global_relative_frame.alt
        else:
            return None
    
    def Konum(self):
        if self.vehicle:
            if self.vehicle and self.vehicle.location.global_relative_frame:
                latitude = self.vehicle.location.global_relative_frame.lat
                longitude = self.vehicle.location.global_relative_frame.lon
                return f"{latitude},{longitude}"
        else:
            return None
        
    def get_attitude(self):
        if self.vehicle:
            return {
                "roll": self.vehicle.attitude.roll,
                "pitch": self.vehicle.attitude.pitch,
                "yaw": self.vehicle.attitude.yaw
            }
        else:
            return None
        
    def get_battery_status(self):
        if self.vehicle:
            batarya = self.vehicle.battery
            print(f"Battery status: {batarya}")
            return {
                "voltaj": batarya.voltage,
                "akim": batarya.current,
                "seviye": batarya.level
            }
        else:
            return None

        
    def disconnect(self):
        if self.vehicle:
            self.vehicle.close()
            self.vehicle = None
    


    def takeoff(self, irtifa):
        iha = self.vehicle
        try:
            while not iha.is_armable:
                print("İHA arm edilebilir durumda değil.")
                time.sleep(1)

            print("İHA arm edilebilir.")
            
            iha.mode = VehicleMode("GUIDED")
            iha.armed = True

            while not iha.armed:
                print("İHA arm ediliyor...")
                time.sleep(0.5)

            print("İHA arm edildi.")
            iha.simple_takeoff(irtifa)
                
            while iha.location.global_relative_frame.alt < irtifa * 0.05:
                print("İHA hedefe yükseliyor.")
                time.sleep(1)
            
            print("Kalkış tamamlandı, görevler ekleniyor...")

            komut = iha.commands
            komut.clear()
            time.sleep(1)

            # TAKEOFF
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

            # WAYPOINT
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.362430, 149.165134, 40))
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.362406, 149.165601, 15))
            
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.363130, 149.165718, 10))

            # RTL
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                            mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                
            # DOĞRULAMA
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                            mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0))

            komut.upload()
            print("Komutlar yüklendi.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    
    


