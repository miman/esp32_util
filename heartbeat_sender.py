import machine
import time
from libs.global_props import GlobalProperties
from config import tasks_settings

# This is a test class which sends a message to the AWS IoT topic '/heartbeat' Onece every X milliseconds
class HeartbeatSender:
    def __init__(self):
        self.timer = None
        self.UPDATE_INTERVAL_ms = tasks_settings.heartbeat_timeout_ms # in ms time unit
        self.last_update = time.ticks_ms()
        self.global_props = None
        self.mqtt = None

    def init(self, global_props: GlobalProperties):
        self.global_props = global_props
        # Activate timer callback if possible
        timer_no = self.global_props.get_and_use_next_timer_no()
        print("HeartbeatSender using timer: " + str(timer_no))
        if (timer_no is not None):
            self.timer = machine.Timer(timer_no)
            # We poll for new MQTT msgs every 500 ms
            self.timer.init(period=self.UPDATE_INTERVAL_ms, mode=machine.Timer.PERIODIC, callback=self.timer_callback)
        # Connect to MQTT broker.
        self.mqtt = self.global_props.get_mqtt_connection()

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        if (self.timer is None):
            # We use the polling process as backup
            if time.ticks_ms() - self.last_update >= self.UPDATE_INTERVAL_ms:
                self.timer_callback("")
                # print('Timeout occured...')


    # The timer callback where we poll for any new MQTT msgs
    def timer_callback(self, pin):
        # print('Timeout occured...')
        self.last_update = time.ticks_ms()
        obj = {
            "time": self.last_update,
            "content": "Heatbeat"
        }
        self.mqtt.send_mqtt_obj(obj_to_send=obj, topic='/heartbeat/')

