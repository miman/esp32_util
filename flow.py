from config import aws_iot_settings
from libs.event_bus import EventBus
from libs.global_props import GlobalProperties
from config import tasks_settings
import ujson as json

# This class implements the actual logic flow based on receiving & sending events on the event bus
# For now it does the following:
# - Send all received RFID events to an external MQTT server
# - Listens to button changes and turn 2 different LED's oon/off based on button state
class Flow:
    def __init__(self, global_props: GlobalProperties):
        self.global_props = global_props
        self.event_bus = global_props.get_event_bus()
        self.enable_observations()

    def enable_observations(self):
        self.event_bus.observe(topic="/local/rfid", callback=self.eventbus_callback)
        self.event_bus.observe(topic="/local/btn/state", callback=self.btn_eventbus_callback)
        
    def send_mqtt(self, obj, topic):
        if (self.global_props.get_mqtt_connection() is not None):
            self.global_props.get_mqtt_connection().send_mqtt_obj(obj_to_send=obj, topic=topic)
            
    def eventbus_callback(self, msg, topic: str, device_id: str):
        if (topic =="/local/rfid"):
            # Send rfid value to MQTT
            self.send_mqtt(msg, "thing/" + tasks_settings.thing_id + "/rfid/" + device_id)
            
    def btn_eventbus_callback(self, msg, topic: str, device_id: str):
        if (topic =="/local/btn/state"):
            set_msg = {
                "state": msg["state"]
                }
            if (device_id == "ext1"):
                self.event_bus.post(msg=set_msg, topic="/local/led/set", device_id="red")
            elif (device_id == "internal_boot"):
                self.event_bus.post(msg=set_msg, topic="/local/led/set", device_id="internal_blue")
