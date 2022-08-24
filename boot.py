# This file is executed on every boot (including wake-boot from deepsleep)

from libs.wifi_connection import WifiConnection
from rest_call_test import RestCaller
from tasks.mqtt_task import MqttTask
from tasks.rfid_task import RfidTask
from tasks.heartbeat_task import HeartbeatTask
from tasks.led_task import LedTask
from tasks.btn_task import ButtonTask
from tasks.file_mgr_task import FileMgrTask
from tasks.hc_sr04_distance_sensor_task import HcSr04Task
from tasks.motor_task import MotorTask
from tasks.lcd_char_task import LcdCharTask
from tasks.servo_task import ServoTask
from libs.global_props import GlobalProperties
from flow import Flow

# Creates & returns the correct Task object based on task name
def startActiveTasks(config, tasks):
    if (config["mqtt"]["active"]):
        tasks.append( MqttTask() )
    if (config["rest_caller"]["active"]):
        tasks.append( RestCaller() )
    if (config["heartbeat"]["active"]):
        tasks.append( HeartbeatTask() )
    if (config["rfid_reader"]["active"]):
        tasks.append( RfidTask() )
    if (config["led"]["active"]):
        tasks.append( LedTask() )
    if (config["button"]["active"]):
        tasks.append( ButtonTask() )
    if (config["file"]["active"]):
        tasks.append( FileMgrTask() )
    if (config["hcsr04"]["active"]):
        tasks.append( HcSr04Task() )
    if (config["motor"]["active"]):
        tasks.append( MotorTask() )
    if (config["lcd"]["active"]):
        tasks.append( LcdCharTask() )
    if (config["servo"]["active"]):
        tasks.append( ServoTask() )
        
try:
    global_props = GlobalProperties();
    global_props.set_thing_id(global_props.config["thing_id"])
    
    flow: Flow = Flow(global_props)
    
    # **************************************
    # Connect to Internet over Wifi
    if (global_props.config["wifi"]["active"]):
        wifi = WifiConnection()
        wifi.connect(global_props.secrets)
    else:
        print("Wifi set not be activated in config/tasks_settings.py")
        
    tasks = []
    startActiveTasks(global_props.config, tasks)
    
    for task in tasks:
        print ("Initiating: " + type(task).__name__)
        task.init(global_props)
        
    while True: 
        for task in tasks:
            task.process()

except KeyboardInterrupt:
    print('Application interrupted by CTRL-c')
except OSError as error :
    print("OSError: " + error)
    print("Rebooting...")
    machine.reset()
finally:
    # Optional cleanup code
    print('Application ended')

#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()