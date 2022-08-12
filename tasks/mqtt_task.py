import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.mqtt_aws_connection import MqttAwsConnection
from libs.wifi_connection import WifiConnection
from libs.global_props import GlobalProperties
from libs.mqtt_routing import MqttRoutingTask

# This is a MQTT class which creates an MQTT connection to an AWS IoT MQTT broker
# It also listens to 2 topics
# - '/txt/write' -> the string in field content is written to the console
# - '/btn/set' -> the blue led is turned on/off based on the value in the field "state" (can be "on" or "off")
class MqttTask(MqttRoutingTask):
    def __init__(self):
        super().__init__()
        self.timer = None
        self.CLIENT_ID = None
        self.last_update = time.ticks_ms()
        self.mqtt = None

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.CLIENT_ID = self.global_props.get_thing_id()
        # Activate timer callback if possible
        timer_no = self.global_props.get_and_use_next_timer_no()
        print("AwsMqttTest using timer: " + str(timer_no))
        if (timer_no is not None):
            self.timer = machine.Timer(timer_no)
            # We poll for new MQTT msgs every 500 ms
            self.timer.init(period=500, mode=machine.Timer.PERIODIC, callback=self.timer_callback)
        # Connect to MQTT broker.
        if (self.global_props.config["mqtt"]["mqtt_type"] == "AWS"):
            print("Starting MQTT type: " + self.global_props.config["mqtt"]["mqtt_type"])
            self.mqtt = MqttAwsConnection(self.global_props)
            self.mqtt.connect_to_mqtt_srv( client_id=self.CLIENT_ID, sub_callback=self.handle_mqtt_sub )
        elif (self.global_props.config["mqtt"]["mqtt_type"] == "Normal"):
            print("Starting MQTT type: " + self.global_props.config["mqtt"]["mqtt_type"])
            self.mqtt = MqttConnection()
            self.mqtt.connect_to_mqtt_srv( client_id=self.CLIENT_ID, sub_callback=self.handle_mqtt_sub, global_props=self.global_props )
        else:
            print("Unknown MQTT type: " + self.global_props.config["mqtt"]["mqtt_type"])
            
        global_props.set_mqtt_connection(self.mqtt)
        self.activate_subscriptions(self.mqtt)
        self.enable_observations(self.eventbus_callback)

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        pass  # Do nothing

    def handle_mqtt_msg(self, topic, msg):
        # print("> MQTT msg on [" + topic + "]: " + msg)
        items = topic.split("/")
        if (items[0] != self.global_props.config["thing_id"]):
            # The message was not for this device
            print("> MQTT received msg for other device on [" + topic + "]: " + msg)
            return
        
        del items[0]  # Remove thing address
        local_topic = '/'.join(items)
        dev_id: str = None
        for t in self.global_props.config["mqtt"]["mqtt_routing"]["topics_to_extract_device_id"]:
            if (t["topic"] in local_topic):
                dev_id = items[len(items)-t["location"]]
                del items[len(items)-t["location"]]  # Remove device id from topic
                local_topic = '/'.join(items)
        
        print("MQTT -> eventbus,  local_topic: [" + local_topic + "], dev_id: " + ("None" if (dev_id is None) else dev_id))
        
        if (local_topic == "txt/write"):
            obj = json.loads(msg)
            print("msg content: " + obj["content"])
        else:
            obj=json.loads(msg)  # str -> object
            self.event_bus.post(msg=obj, topic=local_topic, device_id=dev_id)

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

    # If the topic we get here is in the route externally list we send it to the
    # external topic with the device id added at the end
    def eventbus_callback(self, msg, topic: str, device_id: str):
        if (topic in self.topics_to_route_externally):
            ext_topic = self.global_props.config["thing_id"] + "/" + self.topics_to_route_externally[topic]
            if (device_id is not None):
                ext_topic = ext_topic + "/" + device_id
            self.mqtt.send_mqtt_obj(msg, ext_topic)
            