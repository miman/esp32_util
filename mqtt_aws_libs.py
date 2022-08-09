import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection
from libs.global_props import GlobalProperties

# This is a MQTT class which creates an MQTT connection to an AWS IoT MQTT broker
# It also listens to 2 topics
# - '/txt/write' -> the string in field content is written to the console
# - '/btn/set' -> the blue led is turned on/off based on the value in the field "state" (can be "on" or "off")
class AwsMqttTest:
    def __init__(self):
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.timer = None
        self.CLIENTID = None
        self.TOPIC_SUB = b"#"
        self.last_update = time.ticks_ms()
        self.led.off()
        self.global_props = None
        self.i = 1

    def init(self, global_props: GlobalProperties):
        self.global_props = global_props
        self.CLIENTID = self.global_props.get_thing_id()
        # Activate timer callback if possible
        timer_no = self.global_props.get_and_use_next_timer_no()
        print("AwsMqttTest using timer: " + str(timer_no))
        if (timer_no is not None):
            self.timer = machine.Timer(timer_no)
            # We poll for new MQTT msgs every 500 ms
            self.timer.init(period=500, mode=machine.Timer.PERIODIC, callback=self.timer_callback)
        # Connect to MQTT broker.
        self.mqtt = MqttConnection()
        self.mqtt.connect_to_aws_mqtt( client_id=self.CLIENTID, sub_callback=self.handle_mqtt_sub )
        self.mqtt.subscribe(self.TOPIC_SUB)
        global_props.set_mqtt_connection(self.mqtt)

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        self.i = 0  # Do nothing

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

    def handle_mqtt_sub(self, topic, msg):
        if (type(msg) == str):
            msg_str = msg
        else:
            msg_str = msg.decode()

        if (type(topic) == str):
            topic_str = topic
        else:
            topic_str = topic.decode()
        # print("msg received @ '" + topic_str + "': " + msg_str)
        self.handle_mqtt_msg(topic_str, msg_str)

    # The timer callback where we poll for any new MQTT msgs
    def timer_callback(self, pin):
        self.mqtt.check_msg()
