# This file contains the application settings for the tasks

# The id of this device
thing_id="ESP32_A"

# If the Wifi should be activated or not (pre-req for MQTT for example)
activate_wifi=True

# How often shall the heartbeat service send a heartbeat over MQTT
heartbeat_timeout_ms=300000# Every 5 mins

# If an MQTT task is added it MUST be added first in the array
# This is the list of Tasks that shall be started
active_tasks = [ "AwsMqttTest", "RestCaller", "HeartbeatSender", "RfidTest"]

# This is the list of possible Tasks
sleeping_tasks = [ "RestCaller",
                   "AwsMqttTest",
                   "NormalMqttTest",
                   "GpioTest",
                   "RfidTest",
                   "HeartbeatSender"]
