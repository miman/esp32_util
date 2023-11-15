## LcdCharTask
This task will write on a 1602 LCD character screen the text it receives from the eventbus

## Pins
The LCD task requires the following pins
* scl_pin
* sda_pin
* ground
* power (3.3V)

## Eventbus messages
### lcd/write
When a message is received on the ***lcd/write*** topic on the eventbus the given text will be displayed on the LCD display


### Payload format
The payload for ***lcd/write*** is:

```
{
    "content": "The text to display"
}
```

### lcd/clear
When a message is received on the ***lcd/clear*** topic on the eventbus the given text will be displayed on the LCD display


### Payload format
There in no  payload for ***lcd/clear***

## Configuration format
The payload block for ***LCD*** is:

```
"lcd": {
        "active": False,
        "lcds": [  # List of motors connected to the device
            {
                "id": "lcd_1",
                "scl_pin": 22,
                "sda_pin": 21
                # "total_rows": 2,    # defaults to 2
                # "total_columns": 16, # defaults to 16
                # "i2c_addr": 0x27,      # defaults to 0x27
                # "freq": 10000,    # defaults to 10000
                # "speed": 512  # defaults to 0
            }
        ]
    },
```