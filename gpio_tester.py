import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection

class GpioTest:
    def __init__(self):
        self.led = machine.Pin(14, machine.Pin.OUT)
        self.sw = machine.Pin(15, machine.Pin.IN)
        self.led.off()

    def init(self):
        # Connect to MQTT broker.
        print("init ok")
        
    # **************************************
    # Main loop:
    def process(self):
        while True:
            #print("sw: " + str(self.sw.value()))
            if self.sw.value() == 1:
                self.led.on()
            else:
                self.led.off()
            #time.sleep(0.5)
