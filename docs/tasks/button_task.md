# ButtonTask
This task will poll the buttons defined in the config file regurlarly and send information if a button is pressed or released to the eventbus

## Pins
The button only requires 1 input pin & ground

## Eventbus messages
### btn/state
When a button is pressed or released an event will be sent on the ***btn/state*** topic to the eventbus

If the button is pressed the status will be ***on***
If the button is pressed the status will be ***off***


#### Payload format - btn/state
The payload for ***btn/state*** is:

```
{
    "state": "on"
}
```

## Configuration format
Which buttons that shall be activated & what PIN each is connected to is configured in the ***button*** block

```
"button": {
        "active": True,  # If this module should be active or not
        "buttons": [  # List of buttons connected to the device
            {
                "id": "ext1",
                "pin": 5
            },
            {
                "id": "internal_boot",
                "pin": 0
            }
        ]        
    },
```
