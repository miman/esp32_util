from libs.mfrc522 import MFRC522
from machine import SPI
from libs.global_props import GlobalProperties

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
class RfidTest:
    def __init__(self):
        self.spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
        # *************************
        # To use SoftSPI,
        # from machine import SOftSPI
        # spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
        self.spi.init()
        self.rdr = MFRC522(spi=self.spi, gpioRst=4, gpioCs=5)
        self.mqtt = None

    def init(self, global_props: GlobalProperties):
        self.global_props = global_props
        self.mqtt = self.global_props.get_mqtt_connection()
        print("Place card")

    def inform_about_read_tag(self, rfid_no: str):
        if (self.mqtt is not None):
            obj = {
                "rfid_no": rfid_no
            }
            self.mqtt.send_mqtt_obj(obj_to_send=obj, topic="rfid/1")

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
