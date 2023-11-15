## MotorTask
This task will control the state, direction & speed of a motor based on events on the eventbus

## Pins
The motor requires the following pins
* motor_pin : output
* reverse_ctrl_pin : output
* forward_ctrl_pin : output
* ground
* power (5V)

## Eventbus messages
### motor/run
When a message is received on this channel this task will start the engine with the wanted speed


### Payload format
The payload for ***motor/run*** is:

```
{
    "speed": 12,
    "direction": "clockwise"    # clockwise OR counterclockwise
}
```

### motor/stop
When a message is received on this channel this task will stop the engine


### Payload format
There is no  payload for ***motor/stop***

### motor/speed
When a message is received on this channel this task will change to the wanted speed stil rotating the the previous direction

### Payload format
The payload for ***motor/speed*** is:

```
{
    "speed": 12,
}
```

## Configuration format
The payload block for ***Motor*** is:

```
"motor": {
        "active": False,
        "motors": [  # List of motors connected to the device
            {
                "id": "1",
                "motor_pin": 2,
                "reverse_ctrl_pin": 4,
                "forward_ctrl_pin": 5,
                "freq": 1000   # defaults to 1000
                # "speed": 512  # defaults to 0
            }
        ]
    },
```