import ujson as json

# This class is the base class for MQTT connections
class MqttConnectionBase:
    def __init__(self):
        self.mqtt = None
    
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

