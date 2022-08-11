from libs.global_props import GlobalProperties
from libs.task_base import Task

# This is a class which controls:
# - which topics that should be routed to offboard MQTT server
# - Which topics we should subscribe to from the offboard MQTT server
class MqttRoutingTask(Task):
    def __init__(self):
        super().__init__()
        # A Dictionary with the local topic name as key & the value is the topic name on the external server
        self.topics_to_route_externally = {}
        self.topics_to_subscribe_to = []

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        self.mqtt = global_props.get_mqtt_connection()
        for ttre in self.global_props.config["mqtt"]["mqtt_routing"]["topics_to_route_externally"]:
            print("Adding Topic to route externally: " + ttre["internal"] + " -> " + ttre["external"])
            self.topics_to_route_externally[ttre["internal"]] = ttre["external"]
        for ttst in self.global_props.config["mqtt"]["mqtt_routing"]["topics_to_subscribe_to"]:
            # We add the thing name first so we only subscribe to things addressed to this thing
            ext_topic = self.global_props.config["thing_id"] + "/" + ttst
            print("Adding Topic to subscribe to: " + ext_topic)
            self.topics_to_subscribe_to.append(ext_topic)

    # We subscribe to the internal topics on the event_bus so a callback is called
    # that will route the messages to an external MQTT topic
    def enable_observations(self, eventbus_callback):
        for t in self.topics_to_route_externally.keys():
            self.event_bus.observe(topic=t, callback=eventbus_callback)

    def activate_subscriptions(self, mqtt):
        for t in self.topics_to_subscribe_to:
            mqtt.subscribe(t)

    def process(self):
        pass
