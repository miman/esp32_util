## RfidTask
This task will poll the RFID reader defined in the config file regurlarly and send information if a RFID card is noticed in fromt of the reader, if so the RFID number of the card will be sent to the eventbus

## Pins
The RFID requires the SPI pins, ground & power (3.3V)

## Eventbus messages
### rfid
When a RFID card is noticed an event will be sent on the ***rfid*** topic to the eventbus
The payload will contain the RFID card number

### Payload format
The payload for ***rfid*** is:

```
{
    "rfid_no": "123456"
}
```

## Configuration format
Which RFID reader that shall be activated & which PINs it is connected to is configured in the ***rfid*** block, for now only one is supported

```
"rfid_reader": {
        "active": False,  # If this module should be active or not
        "rfid_readers": [  # List of RFID readers connected to the device
            {
                "id": "1",
                "spi_port": 2,
                "gpio_rst": 4,
                "gpio_cs": 5
            }
        ]
    },
```
