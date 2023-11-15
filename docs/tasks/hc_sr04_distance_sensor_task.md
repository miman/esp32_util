## HcSr04Task
This task will poll the HcSr04 Ultrasound distance sensor for how far away a thing is from the sensor & send this to the eventbus

## Pins
The distance sensor requires the following pins
* trigger_pin : input
* echo_pin : input
* ground
* power (3.3V)

## Eventbus messages

### distanceSensor/value
When the distance to the target has changed an event will be sent on the ***distanceSensor/value*** topic to the eventbus

### Payload format
The payload for ***distanceSensor/value*** is:

```
{
    "mm": 45,   # The distance in mm
    "timestamp_us": 2345632 # The timestamp in microseconds
}
```

## Configuration format
The payload block for ***Motor*** is:

```
"hcsr04": {
        "active": False,  # If this module should be active or not
        "sensors": [  # List of buttons connected to the device
            {
                "id": "dist_1",
                "trigger_pin": 27,
                "echo_pin": 26,
                "time_between_runs_us": 250000
            }
        ]        
    },
```