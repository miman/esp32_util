from libs.global_props import GlobalProperties
from libs.task_base import Task
import machine

class ServoUnit:
    def __init__(self, servo, min_value, max_value):
        self.servo = servo
        self.min_value = min_value
        self.max_value = max_value
        
# A class managing a servo
# It handles the following events from the event_bus
# - set angle
# An example of the configuration needed in the config file can be found at the end of this file
class ServoTask(Task):
    def __init__(self):
        super().__init__()
        self.servos = {}
        # Mapping from pin no -> id
        # self.led_dict = {}

    def enable_observations(self):
        self.event_bus.observe(topic="servo/set", callback=self.set_eventbus_callback)

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.enable_observations()
        for config in self.global_props.config["servo"]["servos"]:
            # set the default PWM frequency as 50Hz
            # the frequency must be between 1Hz and 1kHz.
            freq = 50
            try:
                freq = config["freq"]
            except KeyError:
                pass
            start_value = 50
            try:
                start_value = config["start_value"]
            except KeyError:
                pass
            # set machine GPIO2
            servo_pin = machine.Pin(config["ctrl_pin"])
            # configure PWM
            print("Adding Servo unit: " + config["id"] + " [ctrl_pin: " + str(config["ctrl_pin"])
                  + ", start_value: " + str(start_value) + ", freq: " + str(freq)
                  + ", min_value: " + str(config["min_value"]) + ", max_value: " + str(config["max_value"]) + "]")
            servo = machine.PWM(servo_pin, freq = freq, duty = start_value)
            servo.freq(freq)
            self.servos[config["id"]] = ServoUnit(servo, config["min_value"], config["max_value"])

    # Handles events from the topic: servo/set
    # expects the following members in the JSON payload object:
    # "angle": 0-360
    def set_eventbus_callback(self, msg, topic: str, device_id: str):
        print("servo/set received for: " + device_id)
        if (self.servos[device_id]):
            dev = self.servos[device_id]
            print("servo/set to: " + str(msg["angle"]))
            angle = msg["angle"]
            if (angle < dev.min_value):
                angle = dev.min_value
            if (angle > dev.max_value):
                angle = dev.max_value
            dev.servo.duty(angle)

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        pass

# Config example
#    "servo": {
#        "active": True,
#        "servos": [  # List of servos connected to the device
#            {
#                "id": "servo_1",
#                "ctrl_pin": 15,
#                "start_value": 50,
#                "min_value": 40,
#                "max_value": 115,
#                "freq": 50
#            }
#        ]
