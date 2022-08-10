from umqtt.simple import MQTTClient
from config import aws_iot_settings
from libs.event_bus import EventBus

# This class connects to an AWS IoT MQTT broker & sends messages to this
class GlobalProperties:
    def __init__(self):
        self.mqtt = None
        self.next_timer_no: int = -1
        self.thing_id: str = None
        self.event_bus = EventBus()

    # Returns the thing_id global property
    def get_event_bus(self) -> EventBus:
        return self.event_bus

# Returns the MQTT connection global property
    def get_mqtt_connection(self):
        return self.mqtt

    # Sets the MQTT connection global property
    def set_mqtt_connection(self, mqtt_connection):
        self.mqtt = mqtt_connection

    # Returns the thing_id global property
    def get_thing_id(self) -> str:
        return self.thing_id

    # Sets the thing_id global property
    def set_thing_id(self, thing_id):
        self.thing_id = thing_id
        print("thing_id: " + self.thing_id)

    # Returns and allocates the next timer number.
    # Returns None if no id is available
    def get_and_use_next_timer_no(self) -> int:
        if (self.next_timer_no < 3):# There only exists 4 timers
            self.next_timer_no = self.next_timer_no + 1
            return self.next_timer_no