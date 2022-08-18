from libs.global_props import GlobalProperties
from libs.task_base import Task
from libs.l298_motor import L298Motor

# A class managing a L298 motor
# It handles the following events from the event_bus
# - set speed
# - start with direction
# - stop
class MotorTask(Task):
    def __init__(self):
        super().__init__()
        self.motors = {}
        # Mapping from pin no -> id
        # self.led_dict = {}

    def enable_observations(self):
        self.event_bus.observe(topic="motor/run", callback=self.run_eventbus_callback)
        self.event_bus.observe(topic="motor/stop", callback=self.stop_eventbus_callback)
        self.event_bus.observe(topic="motor/speed", callback=self.speed_eventbus_callback)

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.enable_observations()
        for config in self.global_props.config["motor"]["motors"]:
            print("Adding Motor unit: " + config["id"])
            motor = L298Motor(config["motor_pin"], config["reverse_ctrl_pin"], config["forward_ctrl_pin"], config["freq"])
            if (config["speed"]):
                motor.speed(msg["speed"])
            self.motors[config["id"]] = motor

    # Handles events from the topic: motor/run
    # expects the following members in the JSON payload object:
    # "direction": ["clockwise" or "counterclockwise"]
    # "speed": 0-1023 [is optional, if not set using existing speed]
    def run_eventbus_callback(self, msg, topic: str, device_id: str):
        # print("motor/run received for: " + device_id)
        if (self.motors[device_id]):
            motor = self.motors[device_id]
            if (msg["speed"]):
                motor.speed(msg["speed"])

            if (msg["direction"] == "clockwise"):
                motor.clockwise()
            else:
                motor.counterclockwise()

    # Handles events from the topic: motor/stop
    # expects nothing in the JSON payload object:
    def stop_eventbus_callback(self, msg, topic: str, device_id: str):
        # print("motor/stop received for: " + device_id)
        if (self.motors[device_id]):
            motor = self.motors[device_id]
            motor.stop()

    # Handles events from the topic: motor/speed
    # expects the following members in the JSON payload object:
    # "speed": 0-1023 [is optional, if not set using existing speed]
    def speed_eventbus_callback(self, msg, topic: str, device_id: str):
        # print("motor/speed received for: " + device_id)
        if (self.motors[device_id]):
            motor = self.motors[device_id]
            if (msg["speed"]):
                motor.speed(msg["speed"])

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        pass
