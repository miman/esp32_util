from libs.mfrc522 import MFRC522
from machine import SPI
from libs.global_props import GlobalProperties

# This is base class for all tasks, defining which methods interface they have
class Task:
    def __init__(self):
        self.global_props: GlobalProperties = None
        self.event_bus = None

    # The init function where all initialization takes place
    # The global props is supplier
    def init(self, global_props: GlobalProperties):
        self.global_props = global_props
        self.event_bus = self.global_props.get_event_bus()

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        pass
