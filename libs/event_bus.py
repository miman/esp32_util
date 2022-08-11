import time
import ujson as json

class Observer:
    def __init__(self):
        self.callbacks = []
        
    def get_callbacks(self):
        return self.callbacks
        
class Callback:
    def __init__(self):
        pass
    
    # This is the function that will be called
    def eventbus_callback(self, msg, topic: str):
        pass
    
# This is an event bus used to communicate between all the components in the application
class EventBus:
    def __init__(self):
        super().__init__()
        self.observers = {}

    # Posting a message on the eventbus
    # This will send this event to all observers that are subscribing to this topic
    def post(self, msg, topic: str, device_id: str):
        if (topic in self.observers):
            obs = self.observers[topic]
            for cb in obs.get_callbacks():
                cb(msg=msg, topic=topic, device_id=device_id)

    # Register the callback for a topic
    # The callback shoudl be defined as:
    # def eventbus_callback(self, msg, topic: str, device_id: str):
    def observe(self, topic: str, callback):
        if (topic in self.observers):
            self.observers[topic].get_callbacks().append(callback)
        else:
            self.observers[topic] = Observer()
            self.observers[topic].get_callbacks().append(callback)
            
