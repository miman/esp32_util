from umqtt.simple import MQTTClient
from libs.mqtt_connection_base import MqttConnectionBase

# This class connects to an AWS IoT MQTT broker & sends messages to this
class MqttAwsConnection(MqttConnectionBase):
    def __init__(self, global_props):
        # AWS endpoint parameters.
        self.HOST: str = global_props.secrets["mqtt"]["aws"]["aws_host"]
        self.REGION: str = global_props.device_specific_config["mqtt"]["aws"]["aws_region"]
        self.AWS_ENDPOINT: str = '%s.iot.%s.amazonaws.com' % (self.HOST, self.REGION)

        keyfile: str = global_props.config["mqtt"]["aws"]["keyfile_path"]
        with open(keyfile, 'r') as f:
            key = f.read()

        certfile: str = global_props.config["mqtt"]["aws"]["certfile_path"]
        with open(certfile, 'r') as f:
            cert = f.read()

        self.SSL_PARAMS = {"key": key,"cert": cert}
        # print('MqttConnection initialized Ok')

    # This function connects to the AWS IoT MQTT broker.
    # The callback should look like this: def sub_callback(topic, msg):
    def connect_to_mqtt_srv(self, client_id: str, sub_callback):
        print('Connecting to MQTT...')
        self.mqtt = MQTTClient( client_id, self.AWS_ENDPOINT, port = 8883, keepalive = 10000, ssl = True, ssl_params = self.SSL_PARAMS )
        if sub_callback is not None:
            self.mqtt.set_callback(sub_callback)

        self.mqtt.connect()
        print('MQTT connected OK')
