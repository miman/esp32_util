from libs.global_props import GlobalProperties
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
        self.event_bus.observe(topic="btn/state", callback=self.btn_eventbus_callback)
        
    def send_mqtt(self, obj, topic):
        if (self.global_props.get_mqtt_connection() is not None):
            self.global_props.get_mqtt_connection().send_mqtt_obj(obj_to_send=obj, topic=topic)
            
    def btn_eventbus_callback(self, msg, topic: str, device_id: str):
        if (topic =="btn/state"):
            set_msg = {
                "state": msg["state"]
                }
            if (device_id == "ext1"):
                self.event_bus.post(msg=set_msg, topic="led/set", device_id="red")
            elif (device_id == "internal_boot"):
                self.event_bus.post(msg=set_msg, topic="led/set", device_id="internal_blue")
