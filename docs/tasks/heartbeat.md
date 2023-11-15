# HeartbeatTask
This task will send heartbeat events on the eventbus based on the configuration that has been set or recieved

## Pins
The button only requires 1 input pin & ground

## Eventbus messages
### heartbeat
At regurlar time intervalls a message will be sent on the ***heartbeat*** topic to the eventbus for other systems to know that the device is operational


#### Payload format - heartbeat
The payload for ***heartbeat*** is:

```
{
    "time": 4561237,
    "content": "heartbeat",
    "freeMem": 47
}
```

## Configuration format
How often a heartbeat should be sent to the external MQT broker configured in the ***heartbeat*** block

```
"heartbeat": {
        "active": True,  # If this module should be active or not
        # How often shall the heartbeat service send a heartbeat over MQTT
        "heartbeat_timeout_ms": 600000  # Every 10 mins
    },
```
