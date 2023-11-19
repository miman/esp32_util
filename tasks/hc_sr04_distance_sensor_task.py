import machine
import time
import ujson as json
from libs.global_props import GlobalProperties
from libs.task_base import Task
from libs.event_bus import EventBus

# Measure the distance to a device
# Using HC-SR04 Ultrasonic distance sensor device
# Any 2 GPIO pins can be used
class HcSr04Task(Task):
    def __init__(self, echo_timeout_us=500*2*30):
        super().__init__()
        self.sensors = []
        self.echo_timeout_us = 500*2*30

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        for config in self.global_props.config["hcsr04"]["sensors"]:
            print("Adding HC-SR04 distance sensor unit: " + config["id"])
            trigger = machine.Pin(config["trigger_pin"], machine.Pin.OUT, pull=None)
            trigger.value(0)
            echo = machine.Pin(config["echo_pin"], machine.Pin.IN, pull=None)
            self.sensors.append( {
                "id": config["id"],
                "trigger": trigger,
                "echo": echo,
                "time_between_runs_us": config["time_between_runs_us"],
                "next_run": time.ticks_us() + config["time_between_runs_us"]
                } )

    """
    Get the distance in milimeters without floating point operations.
    """
    def distance_mm(self, sensor):
        try:
            pulse_time = self._send_pulse_and_wait(sensor)

            # To calculate the distance we get the pulse_time and divide it by 2 
            # (the pulse walk the distance twice) and by 29.1 becasue
            # the sound speed on air (343.2 m/s), that It's equivalent to
            # 0.34320 mm/us that is 1mm each 2.91us
            # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
            mm = pulse_time * 100 // 582
            return mm
        except OSError as ex:
            return -1

    def distance_cm(self, sensor):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait(sensor)

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        for sensor in self.sensors:
            if (sensor["next_run"] > time.ticks_us()):
                # We should poll this sensor
                sensor["next_run"] = time.ticks_us() + sensor["time_between_runs_us"]
                mm = self.distance_mm(sensor)
                if ( mm > -1 ):
                    msg = {
                        "mm": mm,
                        "timestamp_us": time.ticks_us()
                    }
                    print("HC-SR04 distance: " + str(mm))
                    self.event_bus.post(msg=msg, topic="distanceSensor/value", device_id=sensor["id"])

    # Send the pulse to trigger and listen on echo pin.
    # We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
    def _send_pulse_and_wait(self, sensor):
        sensor["trigger"].value(0) # Stabilize the sensor
        time.sleep_us(5)
        sensor["trigger"].value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        sensor["trigger"].value(0)
        try:
            pulse_time = machine.time_pulse_us(sensor["echo"], 1, self.echo_timeout_us)
            # time_pulse_us returns -2 if there was timeout waiting for condition; and -1 if there was timeout during the main measurement. It DOES NOT raise an exception
            # ...as of MicroPython 1.17: http://docs.micropython.org/en/v1.17/library/machine.html#machine.time_pulse_us
            if pulse_time < 0:
                MAX_RANGE_IN_CM = 500 # it's really ~400 but I've read people say they see it working up to ~460
                pulse_time = int(MAX_RANGE_IN_CM * 29.1) # 1cm each 29.1us
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex
