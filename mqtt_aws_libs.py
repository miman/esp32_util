import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection

# This is a test class which sends a message to the AWS IoT topic '/txt/write' whenever you press the BOOT button.
# It also listens to 2 topics
# - '/txt/write' -> the string in field content is written to the console
# - '/btn/set' -> the blue led is turned on/off based on the value in the field "state" (can be "on" or "off")
class AwsMqttTest:
    def __init__(self):
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.sw = machine.Pin(0, machine.Pin.IN)
        self.tim0 = machine.Timer(0)
        self.CLIENTID = 'esp32_t2'  # Should be unique for each device connected.
        self.TOPIC_SUB = b"#"
        self.UPDATE_INTERVAL_ms = 20000 # in ms time unit
        self.last_update = time.ticks_ms()
        self.sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.handle_callback)
        self.led.off()

    def init(self):
        # Connect to MQTT broker.
        self.mqtt = MqttConnection()
        self.mqtt.connect_to_aws_mqtt( client_id=self.CLIENTID, sub_callback=self.handle_mqtt_sub )
        self.mqtt.subscribe(self.TOPIC_SUB)
        # We poll for new MQTT msgs every 500 ms
        self.tim0.init(period=500, mode=machine.Timer.PERIODIC, callback=self.timer_callback)

    # **************************************
    # Main loop:
    def process(self):
        while True: 
            if time.ticks_ms() - self.last_update >= self.UPDATE_INTERVAL_ms:
                # print('Timeout occured...')
                self.last_update = time.ticks_ms()
                obj = {
                    "time": self.last_update,
                    "content": "Howdey :-)"
                }
                json_str = json.dumps(obj)
                self.mqtt.send_mqtt_msg(msg_to_send=json_str, topic='/txt/write')

    def handle_callback(self, pin):
        # Ensure we are called directly
        self.last_update = time.ticks_ms() - self.UPDATE_INTERVAL_ms + 200

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
