# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from libs.wifi_connection import WifiConnection
#from rest_call_test import RestCaller
from mqtt_aws_libs import AwsMqttTest
from mqtt_local_test import NormalMqttTest
from gpio_tester import GpioTest

try:
    # **************************************
    # Connect to Internet over Wifi
    wifi = WifiConnection()
    wifi.connect()

    #runner = RestCaller()
    #runner = AwsMqttTest()
    # runner = NormalMqttTest()
    runner = GpioTest()
    runner.init()
    runner.process()
except KeyboardInterrupt:
    print('Application interrupted by CTRL-c')
finally:
    # Optional cleanup code
    print('Application ended')