## ServoTask
This task will send control values to the servo to turn it to the desired location

## Pins
The servo requires the following pins
* ctrl_pin : output
* ground
* power

## Eventbus messages
### servo/set
When a message is received on this channel this task will turn the servo to the desired angle


### Payload format
The payload for ***servo/set*** is:

```
{
    "angle": 45
}
```

## Configuration format
The payload block for ***Motor*** is:

```
"servo": {
        "active": False,
        "servos": [  # List of servos connected to the device
            {
                "id": "servo_1",
                "ctrl_pin": 15,
                "start_value": 50,
                "min_value": 40,
                "max_value": 115,
                "freq": 50   # defaults to 50
            }
        ]
    },
```
