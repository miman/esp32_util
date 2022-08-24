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
        self.angle = 50

    def enable_observations(self):
        self.event_bus.observe(topic="btn/state", callback=self.btn_eventbus_callback)
        self.event_bus.observe(topic="distanceSensor/value", callback=self.dist_eventbus_callback)
        
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
                if (msg["state"] == "on"):
                    writeText = {
                        "content": "Red button"
                    }
                    self.event_bus.post(msg=writeText, topic="lcd/write", device_id="lcd_1")
                    self.angle = self.angle + 5
                    if (self.angle > 180):
                        self.angle = 180
                    servoMsg = {
                        "angle": self.angle
                    }
                    self.event_bus.post(msg=servoMsg, topic="servo/set", device_id="servo_1")
#                else:
#                    self.event_bus.post(msg=None, topic="lcd/clear", device_id="lcd_1")
            elif (device_id == "internal_boot"):
                self.event_bus.post(msg=set_msg, topic="led/set", device_id="internal_blue")
                if (msg["state"] == "on"):
                    writeText = {
                        "content": "Blue button"
                    }
                    self.event_bus.post(msg=writeText, topic="lcd/write", device_id="lcd_1")
                    self.angle = self.angle - 5
                    if (self.angle < 0):
                        self.angle = 0
                    servoMsg = {
                        "angle": self.angle
                    }
                    self.event_bus.post(msg=servoMsg, topic="servo/set", device_id="servo_1")
#                else:
#                    self.event_bus.post(msg=None, topic="lcd/clear", device_id="lcd_1")
                
    def dist_eventbus_callback(self, msg, topic: str, device_id: str):
        if (topic == "distanceSensor/value"):
            # print("HC-SR04 distance: " + str(mm) )
            set_msg = {
                "state": "on"
            }
            if (msg["mm"] > 80):
                if (msg["mm"] > 240):
                    self.event_bus.post(msg=set_msg, topic="led/set", device_id="red")
                    set_msg["state"] = "off"
                    self.event_bus.post(msg=set_msg, topic="led/set", device_id="internal_blue")
                else:
                    self.event_bus.post(msg=set_msg, topic="led/set", device_id="internal_blue")
                    set_msg["state"] = "off"
                    self.event_bus.post(msg=set_msg, topic="led/set", device_id="red")
            else:
                set_msg["state"] = "off"
                self.event_bus.post(msg=set_msg, topic="led/set", device_id="red")
                self.event_bus.post(msg=set_msg, topic="led/set", device_id="internal_blue")
