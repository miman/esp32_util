import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection
from config import mqtt_settings
from libs.global_props import GlobalProperties
from libs.task_base import Task

# This is a MQTT Connection class which creates an MQTT connection to a normal Basic auth MQTT broker
# It also listens to 2 topics
# - '/txt/write' -> the string in field content is written to the console
# - '/btn/set' -> the blue led is turned on/off based on the value in the field "state" (can be "on" or "off")

class NormalMqttTest(Task):
    def __init__(self):
        super().__init__()
        self.mqtt_username=mqtt_settings.username
        self.mqtt_password=mqtt_settings.password
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.HTTP_HEADERS = {'Content-Type': 'application/json'}
        self.UPDATE_INTERVAL_ms = 30000 # in ms time unit
        self.last_update = time.ticks_ms()
        self.led.off()
        self.CLIENT_ID = None
        self.MQTT_ENDPOINT = mqtt_settings.mqtt_host
        self.TOPIC_SUB = b"#"

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

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.CLIENT_ID = self.global_props.get_thing_id()
        # Connect to MQTT broker.
        self.mqtt = MqttConnection()
        self.mqtt.connect_to_mqtt( host_endpoint=self.MQTT_ENDPOINT, client_id=self.CLIENT_ID,
                                   username=self.mqtt_username, password=self.mqtt_password, sub_callback=self.sub_callback )
        self.mqtt.subscribe(self.TOPIC_SUB)
        global_props.set_mqtt_connection(self.mqtt)

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        if time.ticks_ms() - self.last_update >= self.UPDATE_INTERVAL_ms:
            #self.mqtt.wait_msg() #blocking  
            self.mqtt.check_msg() #non-blocking  
