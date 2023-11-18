## LedTask
This task will poll the buttons defined in the config file regurlarly and send information if a button is pressed or released to the eventbus

## Pins
The LED requires the following pins
- GPIO output pin
- power (3.3V)
- ground

## Eventbus messages
### led/+/set
When message is received on topic ***led/+/set*** from the eventbus this task will turn the led with the given name on or off.
The + is the location of the name of the led.

If the received status is ***on***, we will turn the led on
If the received status is ***off***, we will turn the led off

#### Payload format
The payload for ***led/+/set*** is:

```
{
    "state": "on"
}
```

## Configuration format
Which LED's that shall be activated & what PIN each is connected to is configured in the ***led*** block

```
"led": {
        "active": True,  # If this module should be active or not
        "leds": [  # List of LED's connected to the device
            {
                "id": "red",
                "pin": 14,
                "in_out": "OUT"
            },
            {
                "id": "internal_blue",
                "pin": 2,
                "in_out": "OUT"
            },
        ]
    },
```