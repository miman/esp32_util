from umqtt.simple import MQTTClient
import ujson as json
from libs.mqtt_connection_base import MqttConnectionBase

# This class connects to a normal MQTT broker & sends messages to this
class MqttConnection(MqttConnectionBase):
    def __init__(self):
        pass

    # This function connects to a normal MQTT broker.
    # The callback should look like this: def sub_callback(topic, msg):
    def connect_to_mqtt_srv(self, client_id: str, sub_callback, global_props):
        print('Connecting to MQTT...')
        self.mqtt = MQTTClient( client_id, global_props.config["mqtt"]["normal"]["mqtt_host"],
                                user=global_props.config["mqtt"]["normal"]["username"],
                                password=global_props.config["mqtt"]["normal"]["password"],
                                keepalive = 10000, ssl = False )
        if sub_callback is not None:
            self.mqtt.set_callback(sub_callback)

        self.mqtt.connect()
        print('MQTT connected OK')

    # This function connects to a normal MQTT broker.
    # The callback should look like this: def sub_callback(topic, msg):
    def connect_to_mqtt_with_ssl(self, host_endpoint, client_id: str, username: str, password: str, sub_callback, ssl_params):
        print('Connecting to MQTT...')
        self.mqtt = MQTTClient( client_id, host_endpoint, user=username, password=password, keepalive = 10000, ssl = True, ssl_params = ssl_params )
        if sub_callback is not None:
            self.mqtt.set_callback(sub_callback)

        self.mqtt.connect()
        print('MQTT connected OK')
