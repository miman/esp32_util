from umqtt.simple import MQTTClient
from config import aws_iot_settings
import ujson as json

# This class connects to an AWS IoT MQTT broker & sends messages to this
class MqttConnection:
    def __init__(self):
        # print('MqttConnection..')
        # AWS endpoint parameters.
        self.HOST: str = aws_iot_settings.aws_host
        self.REGION: str = aws_iot_settings.aws_region
        self.AWS_ENDPOINT: str = '%s.iot.%s.amazonaws.com' % (self.HOST, self.REGION)

        keyfile: str = aws_iot_settings.keyfile_path
        with open(keyfile, 'r') as f:
            key = f.read()

        certfile: str = aws_iot_settings.certfile_path
        with open(certfile, 'r') as f:
            cert = f.read()

        #aws_certfile = "/AmazonRootCA1.pem"
        #with open(aws_certfile, 'r') as f:
        #    aws_cert = f.read()

        self.SSL_PARAMS = {"key": key,"cert": cert}
        #self.SSL_PARAMS = {'key': key,'cert': cert, 'ca_certs': aws_cert}
        # print('MqttConnection initialized Ok')

    # This function connects to the AWS IoT MQTT broker.
    # The callback should look like this: def sub_callback(topic, msg):
    def connect_to_aws_mqtt(self, client_id: str, sub_callback):
        print('Connecting to MQTT...')
        self.mqtt = MQTTClient( client_id, self.AWS_ENDPOINT, port = 8883, keepalive = 10000, ssl = True, ssl_params = self.SSL_PARAMS )
        if sub_callback is not None:
            self.mqtt.set_callback(sub_callback)

        self.mqtt.connect()
        print('MQTT connected OK')

    # This function connects to a normal MQTT broker.
    # The callback should look like this: def sub_callback(topic, msg):
    def connect_to_mqtt(self, host_endpoint, client_id: str, username: str, password: str, sub_callback):
        print('Connecting to MQTT...')
        self.mqtt = MQTTClient( client_id, host_endpoint, user=username, password=password, keepalive = 10000, ssl = False )
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

    # This function is used to send a message string to a topic
    def send_mqtt_msg(self, msg_to_send: str, topic: str):
        # print('Sending msg to MQTT: ' + msg_to_send)
        self.mqtt.publish( topic = topic, msg = msg_to_send, qos = 0 )

    # This function is used to send an object as a JSON string to a topic
    def send_mqtt_obj(self, obj_to_send, topic: str):
        # print('Sending msg to MQTT: ' + msg_to_send)
        json_str = json.dumps(obj_to_send)
        self.mqtt.publish( topic = topic, msg = json_str, qos = 0 )

    # This function is used to subscribe to data from the given topic name
    # when data is received the sub_callback given in connect will be called
    def subscribe(self, topic_to_subscribe_to: str):
        self.mqtt.subscribe(topic_to_subscribe_to)

    # Will poll for new incoming message, in a blocking mode
    def wait_msg(self):
        self.mqtt.wait_msg()
        
    # Will poll for new incoming message, in an non-blocking mode
    def check_msg(self):
        self.mqtt.check_msg()

    # Disonnects the connection
    def disconnect(self):
        self.mqtt.disconnect()
