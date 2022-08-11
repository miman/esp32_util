import machine
import time
import ujson as json
from libs.global_props import GlobalProperties
from libs.task_base import Task
from libs.event_bus import EventBus

class LedTask(Task):
    def __init__(self):
        super().__init__()
        self.leds = {}
        # Mapping from pin no -> id
        # self.led_dict = {}

    def enable_observations(self):
        self.event_bus.observe(topic="led/set", callback=self.eventbus_callback)

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.event_bus = self.global_props.get_event_bus()
        self.enable_observations()
        for config in self.global_props.config["led"]["leds"]:
            print("Adding LED unit: " + config["id"])
            led = machine.Pin(config["pin"], machine.Pin.OUT)
            led.off()
            self.leds[config["id"]] = led

    def eventbus_callback(self, msg, topic: str, device_id: str):
        if (topic == "led/set"):
            # print("/local/btn/set received for: " + device_id)
            if (device_id in self.leds):
                led = self.leds[device_id]
                # obj = json.loads(msg)
                if (msg["state"] == "on"):
                    led.on()
                else:
                    led.off()

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        pass

#             led = machine.Pin(config["pin"], machine.Pin.OUT if (config["in_out"] == "OUT") else machine.Pin.IN)
