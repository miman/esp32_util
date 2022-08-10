# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from libs.wifi_connection import WifiConnection
from rest_call_test import RestCaller
from mqtt_aws_libs import AwsMqttTest
from mqtt_local_test import NormalMqttTest
from gpio_tester import GpioTest
from rfid_test import RfidTest
from tasks.heartbeat_task import HeartbeatTask
from libs.event_bus import EventBus
from tasks.led_task import LedTask
from tasks.btn_task import ButtonTask
from config import tasks_settings
from libs.global_props import GlobalProperties
from flow import Flow

# Creates & returns the correct Task object based on task name
def createTaskFromString(task_name):
    if (task_name == "RestCaller"):
        return RestCaller()
    elif (task_name == "AwsMqttTest"):
        return AwsMqttTest()
    elif (task_name == "NormalMqttTest"):
        return NormalMqttTest()
    elif (task_name == "GpioTest"):
        return GpioTest()
    elif (task_name == "HeartbeatTask"):
        return HeartbeatTask()
    elif (task_name == "RfidTest"):
        return RfidTest()
    elif (task_name == "EventBus"):
        return EventBus()
    elif (task_name == "LedTask"):
        return LedTask()
    elif (task_name == "ButtonTask"):
        return ButtonTask()
    else:
        print("Unknown Task name '" + at + "'-> no object created")

try:
    global_props = GlobalProperties();
    global_props.set_thing_id(tasks_settings.thing_id)
    
    flow: Flow = Flow(global_props)
    
    # **************************************
    # Connect to Internet over Wifi
    if (tasks_settings.activate_wifi):
        wifi = WifiConnection()
        wifi.connect()
    else:
        print("Wifi set not be activated in config/tasks_settings.py")
        
    tasks = []
    for at in tasks_settings.active_tasks:
        tmp = createTaskFromString(at)
        if tmp is not None:
            tasks.append(tmp)
            print("Task created: " + at)
        else:
            print("Task unknown: " + at)
        
    for task in tasks:
        #print ("Initiating: " + type(task).__name__)
        task.init(global_props)
        
    while True: 
        for task in tasks:
            task.process()

except KeyboardInterrupt:
    print('Application interrupted by CTRL-c')
finally:
    # Optional cleanup code
    print('Application ended')