from libs.mfrc522 import MFRC522
from machine import SPI
from libs.global_props import GlobalProperties
from libs.task_base import Task
from libs.event_bus import EventBus

# This is a test class which uses an RFID-RC522 reader connected as follows:
# When an RFID card is read it's number is written to the console
# 
# Using Hardware SPI pins:
#     sck=18   # yellow
#     mosi=23  # orange
#     miso=19  # blue
#     rst=4    # white
#     cs=5     # green, DS
# So from left to right connect:
# GPIO05, GPIO18, GPIO23, GPIO19, Nothing, GND, GPIO04, 3.3V
class RfidTask(Task):
    def __init__(self):
        super().__init__()
        self.event_bus = None

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.event_bus = global_props.get_event_bus()
        for config in self.global_props.config["rfid_reader"]["rfid_readers"]:
            print("Adding RFID unit: " + config["id"])
            self.spi = SPI(config["spi_port"], baudrate=2500000, polarity=0, phase=0)
            # *************************
            # To use SoftSPI,
            # from machine import SOftSPI
            # spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
            self.spi.init()
            self.rdr = MFRC522(spi=self.spi, gpioRst=config["gpio_rst"], gpioCs=config["gpio_cs"])
            self.id = config["id"]
        print("Place card")

    def inform_about_read_tag(self, rfid_no: str):
        if (self.event_bus is not None):
            obj = {
                "rfid_no": rfid_no
            }
            self.event_bus.post(msg=obj, topic="rfid", device_id=self.id)

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)
        if stat == self.rdr.OK:
            (stat, raw_uid) = self.rdr.anticoll()
            if stat == self.rdr.OK:
                card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                print("RFID no: " + card_id)
                self.inform_about_read_tag(rfid_no=card_id)
