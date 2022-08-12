from libs.global_props import GlobalProperties
from libs.task_base import Task
import os

# The file manager task will read/write/remove a file based on eventbus commands
# topic "file/write"
# topic "file/read"
# topic "file/remove"
# The read command will send back the file contebt on topic "file/content"
# File info from: https://docs.micropython.org/en/latest/esp8266/tutorial/filesystem.html
class FileMgrTask(Task):
    def __init__(self):
        super().__init__()
        self.leds = {}

    def enable_observations(self):
        self.event_bus.observe(topic="file/write", callback=self.eventbus_callback)
        self.event_bus.observe(topic="file/read", callback=self.eventbus_callback)
        self.event_bus.observe(topic="file/remove", callback=self.eventbus_callback)

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.enable_observations()

    # Writes the given file content to a file on the given path
    def write_file(self, msg):
        print("write_file: path: '" + msg["path"] + "', content: " + msg["content"])
        file = open (msg["path"], "w") # TextIOWrapper
        chars_written = file.write(msg["content"])
        print("write_file: chars_written: '" + str(chars_written) + "'")
        file.close()

    # Reads the given file content to a file on the given path & writes back the file on the topic "file/content"
    def read_file(self, msg):
        print("read_file: path: '" + msg["path"] + "'")
        file = open (msg["path"]) # TextIOWrapper
        content = file.read()
        file.close()
        reply = {
            "path": msg["path"],
            "content": content
        }
        self.event_bus.post(msg=reply, topic="file/content", device_id=None)

    # Removes the given file content to a file on the given path
    def remove_file(self, msg):
        print("remove_file: path: '" + msg["path"]  + "'")
        file = open (msg["path"]) # TextIOWrapper
        os.remove(file)

    def eventbus_callback(self, msg, topic: str, device_id: str):
        print("FileMgrTask: event received on topic: '" + topic + "'")
        if (topic == "file/write"):
            self.write_file(msg)
        if (topic == "file/read"):
            self.read_file(msg)
        if (topic == "file/remove"):
            self.remove_file(msg)

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        pass

#             led = machine.Pin(config["pin"], machine.Pin.OUT if (config["in_out"] == "OUT") else machine.Pin.IN)
