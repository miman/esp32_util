import network 

# This class activates a Wifi connection based on the ssid & password defined
# in a separate file called wifi_credentials.py
class WifiConnection:
    def __init__(self):
        self.sta = network.WLAN(network.STA_IF)

    # **************************************
    # Configure the ESP32 wifi as STAtion
    def connect(self, secrets):
        if not self.sta.isconnected(): 
          print('connecting to network...') 
          self.sta.active(True) 
          self.sta.connect(secrets["wifi"]["ssid"], secrets["wifi"]["password"]) 
          while not self.sta.isconnected(): 
            pass 
        print('network config:', self.sta.ifconfig())
