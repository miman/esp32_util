## MqttTask
This task will do a number of tasks, all of them configured in the config file under the ***mqtt*** block
* Route any message from a list pf topics from the eventbus to the offboard MQTT broker onto a topic name defined in the same config block.
* Subscribe to a list of topics from the offboard MQTT broker & route these to the eventbus
  * after removing the thing-name in the first place in the topic
* Move one location in the topic to the device_id parameter & remove this from the topic
  * This to make the eventbus logic simpler
* Write the content of a message to the console for msgs posted to the topic ***txt/write***

## Pins
The MQTT task does not use any PIN's

## Eventbus messages
### txt/write
Write the content of a message to the console for msgs posted to the topic ***txt/write***

### Payload format
The payload for ***txt/write*** is:

```
{
    "content": "Msg to write to console :-)"
}
```

## Configuration format
The MQTT configuration is  configured in the ***mqtt*** block.
Here you can configure:
* if you are to connect to a normal MQTT server with username/password or AWS IoT using certificates
* The hostname for a normal MQTT broker
* The AWS region & the file paths for the AWS certificates
* which topics on the internal event bus that should automatically be routed to an external MQTT broker
* which topics that the device should subscribe to from the external MQTT broker, these will automaically be sent to the eventbus (after the thing name has been removed)

```
"mqtt": {
        "active": False,  # If this module should be active or not
        "mqtt_type": "AWS",  # AWS or Normal
        "normal": {
            "mqtt_host": "192.168.68.121"
        },
        "aws": {
            "aws_region": "eu-west-1",
            "keyfile_path": "/certs/thing-private.pem.key",
            "certfile_path": "/certs/thing-certificate.pem.crt"
        },
        "mqtt_routing": {
            "topics_to_route_externally": [  # - which topics that should be routed to offboard MQTT server
                {
                    "internal": "btn/state",
                    "external": "btn/state"
                },
                {
                    "internal": "file/content",
                    "external": "file/content"
                },
                {
                    "internal": "rfid",
                    "external": "rfid"
                }                
            ],
            "topics_to_subscribe_to": [  # - Which topics we should subscribe to from the offboard MQTT server
                "txt/#",
                "led/#",
                "file/write",
                "file/read",
                "file/remove"
            ],
            "topics_to_extract_device_id": [  # - Which topics we should extract the last item in the topic & place in device_id field
                {
                    "topic": "led",
                    "location": 2
                }
            ]
        }
    },
```
