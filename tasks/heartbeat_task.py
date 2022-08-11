import machine
import time
from libs.global_props import GlobalProperties
from libs.task_base import Task
import gc

# This is a test class which sends a message to the AWS IoT topic '/heartbeat' Onece every X milliseconds
class HeartbeatTask(Task):
    def __init__(self):
        super().__init__()
        self.timer = None
        self.UPDATE_INTERVAL_ms = None # in ms time unit
        self.last_update = time.ticks_ms()
        self.mqtt = None

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        # Activate timer callback if possible
        timer_no = self.global_props.get_and_use_next_timer_no()
        self.UPDATE_INTERVAL_ms = self.global_props.config["heartbeat"]["heartbeat_timeout_ms"]
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
        gc.collect()
        free_mem = gc.mem_free()        
        self.last_update = time.ticks_ms()
        obj = {
            "time": self.last_update,
            "content": "heartbeat",
            "freeMem": free_mem
        }
        self.mqtt.send_mqtt_obj(obj_to_send=obj, topic='/heartbeat/')

