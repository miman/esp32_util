import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection
from libs.global_props import GlobalProperties
from libs.task_base import Task
from config import tasks_settings

# This is a MQTT class which creates an MQTT connection to an AWS IoT MQTT broker
# It also listens to 2 topics
# - '/txt/write' -> the string in field content is written to the console
# - '/btn/set' -> the blue led is turned on/off based on the value in the field "state" (can be "on" or "off")
class AwsMqttTest(Task):
    def __init__(self):
        super().__init__()
        self.timer = None
        self.CLIENTID = None
        self.TOPIC_SUB = b"#"
        self.last_update = time.ticks_ms()

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
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
        pass  # Do nothing

    def handle_mqtt_msg(self, topic, msg):
        print("> MQTT msg on [" + topic + "]: " + msg)
        items = topic.split("/")
        if (items[0] != tasks_settings.thing_id):
            # The message was not for this device
            print("> MQTT received msg for other device on [" + topic + "]: " + msg)
            return
        
        del items[0]  # Remove thing address
        local_topic = '/'.join(items)
        if ("led/set" in local_topic):
            obj=json.loads(msg)  # str -> object
            items = local_topic.split("/")
            dev_id = items[len(items)-1]
            del items[len(items)-1]  # Remove device id from topic
            local_topic = '/'.join(items)
            self.event_bus.post(msg=obj, topic=local_topic, device_id=dev_id)
        elif (local_topic == "txt/write"):
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
