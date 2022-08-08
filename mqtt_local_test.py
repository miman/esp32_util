import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection
from config import mqtt_settings

# This is a test class which sends a message to the AWS IoT topic '/txt/write' whenever you press the BOOT button.
# It also listens to 2 topics
# - '/txt/write' -> the string in field content is written to the console
# - '/btn/set' -> the blue led is turned on/off based on the value in the field "state" (can be "on" or "off")

class NormalMqttTest:
    def __init__(self):
        self.mqtt_username=mqtt_settings.username
        self.mqtt_password=mqtt_settings.password
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.sw = machine.Pin(0, machine.Pin.IN)
        # self.tim0 = machine.Timer(0)
        self.HTTP_HEADERS = {'Content-Type': 'application/json'}
        self.UPDATE_INTERVAL_ms = 30000 # in ms time unit
        self.last_update = time.ticks_ms()
        self.sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.handle_callback)
        self.led.off()
        self.CLIENT_ID = b'ESP32_1'  # Should be unique for each device connected.
        self.MQTT_ENDPOINT = mqtt_settings.mqtt_host
        self.TOPIC_SUB = b"#"

    def handle_callback(self, pin):
        # Ensure we are called directly
        self.last_update = time.ticks_ms() - self.UPDATE_INTERVAL_ms + 200
        # print('Button pressed')

    def handle_mqtt_msg(self, topic, msg):
        if (topic == "/btn/set"):
            obj = json.loads(msg)
            if (obj["state"] == "on"):
                self.led.on()
            else:
                self.led.off()
        elif (topic == "/txt/write"):
            obj = json.loads(msg)
            print("msg content: " + obj["content"])
    
    def sub_callback(self, topic, msg):
        msg_str = msg.decode()
        topic_str = topic.decode()
        print("msg received @ '" + topic_str + "': " + msg_str)
        self.handle_mqtt_msg(topic_str, msg_str)

    def init(self):
        # Connect to MQTT broker.
        self.mqtt = MqttConnection()
        self.mqtt.connect_to_mqtt( host_endpoint=self.MQTT_ENDPOINT, client_id=self.CLIENT_ID,
                                   username=self.mqtt_username, password=self.mqtt_password, sub_callback=self.sub_callback )
        self.mqtt.subscribe(self.TOPIC_SUB)

    # **************************************
    # Main loop:
    def process(self):
        while True: 
            if time.ticks_ms() - self.last_update >= self.UPDATE_INTERVAL_ms:
                print('Requesting data...')
                self.last_update = time.ticks_ms()
                obj = {
                    "time": self.last_update,
                    "msg": "Howdey :-)"
                }
                json_str = json.dumps(obj)
                self.mqtt.send_mqtt_msg(json_str, 'test/esp32/hi')
                #self.mqtt.wait_msg() #blocking  
                self.mqtt.check_msg() #non-blocking  
