import machine
import time
import ujson as json
from libs.global_props import GlobalProperties
from libs.task_base import Task
from libs.event_bus import EventBus

class ButtonTask(Task):
    def __init__(self):
        super().__init__()
        self.btns = {}

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        for config in self.global_props.config["button"]["buttons"]:
            print("Adding Button unit: " + config["id"])
            b = machine.Pin(config["pin"], machine.Pin.IN)
            self.btns[config["pin"]] = {
                "id": config["id"],
                "btn": b,
                "last_state": 0
                }

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        for key in self.btns.keys():
            obj = self.btns[key]
            if (obj["btn"].value() != obj["last_state"]):
                # Btn state changed -> inform about this
                obj["last_state"] = obj["btn"].value()
                msg = {
                    "state": "on" if (obj["last_state"] == 0) else "off"
                    }
                self.event_bus.post(msg=msg, topic="btn/state", device_id=obj["id"])
