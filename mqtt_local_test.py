import machine
import time
import ujson as json
from libs.mqtt_connection import MqttConnection
from libs.wifi_connection import WifiConnection

mqtt_username="TBD"
mqtt_password="TBD"

led = machine.Pin(2, machine.Pin.OUT)
sw = machine.Pin(0, machine.Pin.IN)
# tim0 = machine.Timer(0)

# **************************************
# Constants and variables:
HTTP_HEADERS = {'Content-Type': 'application/json'}

UPDATE_INTERVAL_ms = 30000 # in ms time unit
last_update = time.ticks_ms()

def handle_callback(pin):
    global last_update
    # Ensure we are called directly
    last_update = time.ticks_ms() - UPDATE_INTERVAL_ms + 200
    # print('Button pressed')

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
    print("msg received @ '" + topic_str + "': " + msg_str)
    handle_mqtt_msg(topic_str, msg_str)

# **************************************
# Connect to Internet over Wifi
wifi = WifiConnection()
wifi.connect()

# Connect to MQTT broker.
CLIENT_ID = b'ESP32_1'  # Should be unique for each device connected.
MQTT_ENDPOINT = b'192.168.68.121'
TOPIC_SUB = b"#"
mqtt = MqttConnection()
mqtt.connect_to_mqtt( host_endpoint=MQTT_ENDPOINT, client_id=CLIENT_ID, username=mqtt_username, password=mqtt_password, sub_callback=sub_callback )
mqtt.subscribe(TOPIC_SUB)

# **************************************
# Main loop:
while True: 
    if time.ticks_ms() - last_update >= UPDATE_INTERVAL_ms:
        print('Requesting data...')
        last_update = time.ticks_ms()
        obj = {
            "time": last_update,
            "msg": "Howdey :-)"
        }
        json_str = json.dumps(obj)
        mqtt.send_mqtt_msg(json_str, 'test/esp32/hi')
    try:  
        #mqtt.wait_msg() #blocking  
        mqtt.check_msg() #non-blocking  
    except KeyboardInterrupt:  
        print('Ctrl-C pressed...exiting')  
        mqtt.disconnect()  
        sys.exit()
