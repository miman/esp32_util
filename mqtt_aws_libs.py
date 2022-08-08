import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection

led = machine.Pin(2, machine.Pin.OUT)
sw = machine.Pin(0, machine.Pin.IN)
tim0 = machine.Timer(0)

CLIENTID = 'esp32_t2'  # Should be unique for each device connected.
TOPIC_SUB = b"#"

# **************************************
# Constants and variables:
UPDATE_INTERVAL_ms = 20000 # in ms time unit
last_update = time.ticks_ms()

def handle_callback(pin):
    global last_update
    # Ensure we are called directly
    last_update = time.ticks_ms() - UPDATE_INTERVAL_ms + 200

sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_callback)

led.off()

def handle_mqtt_msg(topic, msg):
    if (topic == "/btn/set"):
        obj = json.loads(msg)
        if (obj["state"] == "on"):
            led.on()
        else:
            led.off()
    elif (topic == "/txt/write"):
        obj = json.loads(msg)
        print("msg content: " + obj["content"])

def sub_callback(topic, msg):
    msg_str = msg.decode()
    topic_str = topic.decode()
    # print("msg received @ '" + topic_str + "': " + msg_str)
    handle_mqtt_msg(topic_str, msg_str)
    
# **************************************
# Connect to Internet over Wifi
wifi = WifiConnection()
wifi.connect()

#print('All setup, starting MQTT stuff')
# Connect to MQTT broker.
mqtt = MqttConnection()
mqtt.connect_to_aws_mqtt( client_id=CLIENTID, sub_callback=sub_callback )
mqtt.subscribe(TOPIC_SUB)

# The timer callback where we poll for any new MQTT msgs
def timer_callback(pin):
    mqtt.check_msg()

# We poll for new MQTT msgs every 500 ms
tim0.init(period=500, mode=machine.Timer.PERIODIC, callback=timer_callback)

# **************************************
# Main loop:
while True: 
    if time.ticks_ms() - last_update >= UPDATE_INTERVAL_ms:
        # print('Timeout occured...')
        last_update = time.ticks_ms()
        obj = {
            "time": last_update,
            "msg": "Howdey :-)"
        }
        json_str = json.dumps(obj)
        mqtt.send_mqtt_msg(msg_to_send=json_str, topic='test/esp32')
