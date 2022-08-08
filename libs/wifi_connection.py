import network 
from config import wifi_credentials 

# This class activates a Wifi connection based on the ssid & password defined
# in a separate file called wifi_credentials.py
class WifiConnection:
    def __init__(self):
        self.sta = network.WLAN(network.STA_IF)

    # **************************************
    # Configure the ESP32 wifi as STAtion
    def connect(self):
        if not self.sta.isconnected(): 
          print('connecting to network...') 
          self.sta.active(True) 
          self.sta.connect(wifi_credentials.ssid, wifi_credentials.password) 
          while not self.sta.isconnected(): 
            pass 
        print('network config:', self.sta.ifconfig())
