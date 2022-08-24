from machine import Pin, SoftI2C
# from libs.lcd.lcd_api import LcdApi
# from libs.lcd.i2c_lcd import I2cLcd
from libs.lcd.lcd_1602 import LCD
from libs.global_props import GlobalProperties
from libs.task_base import Task
from libs.event_bus import EventBus

class LcdUnit:
    def __init__(self, i2c, lcd):
        self.i2c = i2c
        self.lcd = lcd

# Used to write on a 1602 LCD character screen
# On ESP 32 use these PINS: scl = 22 & sda = 21
# On ESP 8622 use these PINS: scl = 5 & sda = 4
class LcdCharTask(Task):
    def __init__(self):
        super().__init__()
        self.leds = {}
        # Mapping from pin no -> id
        # self.led_dict = {}

    def enable_observations(self):
        self.event_bus.observe(topic="lcd/write", callback=self.write_eventbus_callback)
        self.event_bus.observe(topic="lcd/clear", callback=self.clear_eventbus_callback)

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.enable_observations()
        for config in self.global_props.config["lcd"]["lcds"]:
            I2C_ADDR = 0x27
            totalRows = 2
            totalColumns = 16
            freq = 10000
            try:
                freq = config["freq"]
            except KeyError:
                pass
            try:
                totalRows = config["total_rows"]
            except KeyError:
                pass
            try:
                totalColumns = config["total_columns"]
            except KeyError:
                pass
            try:
                I2C_ADDR = config["i2c_addr"]
            except KeyError:
                pass
            print("Adding LCD screen unit: " + config["id"] + " [scl: " + str(config["scl_pin"]) + ", sda: " + str(config["sda_pin"])
                  + ", freq: " + str(freq) + ", I2C_ADDR: " + str(I2C_ADDR)
                  + ", totalColumns: " + str(totalColumns) + ", totalRows: " + str(totalRows) + "]")
            i2c = SoftI2C(scl=Pin(config["scl_pin"]), sda=Pin(config["sda_pin"]), freq=freq)
            lcd = LCD(i2c)

            lcd_unit = LcdUnit(i2c, lcd)
            self.leds[config["id"]] = lcd_unit

    def write_eventbus_callback(self, msg, topic: str, device_id: str):
        print("lcd/write received for: " + device_id + ", with content: " + msg["content"])
        if (device_id in self.leds):
            lcd_unit = self.leds[device_id]
            print("Writing to lcd for: " + device_id + ", content: " + msg["content"])
            lcd_unit.lcd.puts(msg["content"])

    def clear_eventbus_callback(self, msg, topic: str, device_id: str):
        print("lcd/clear received for: " + device_id)
        if (device_id in self.leds):
            lcd_unit = self.leds[device_id]
            lcd_unit.lcd.clear()

    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        pass
