# esp32_util componentes
This page describes what the different components do

# Tasks
Here are the tasks

## ButtonTask
This task will poll the buttons defined in the config file regurlarly and send information if a button is pressed or released to the eventbus

### btn/state
When a button is pressed or released an event will be sent on the ***btn/state*** topic to the eventbus

If the button is pressed the status will be ***on***
If the button is pressed the status will be ***off***


### Payload format
The payload for ***btn/state*** is:

```
{
    "state": "on"
}
```

## LedTask
This task will poll the buttons defined in the config file regurlarly and send information if a button is pressed or released to the eventbus

### led/+/set
When message is received on topic ***led/+/set*** from the eventbus this task will turn the led with the given name on or off.
The + is the location of the name of the led.

If the received status is ***on***, we will turn the led on
If the received status is ***off***, we will turn the led off

### Payload format
The payload for ***led/+/set*** is:

```
{
    "state": "on"
}
```

## RfidTask
This task will poll the RFID reader defined in the config file regurlarly and send information if a RFID card is noticed in fromt of the reader, if so the RFID number of the card will be sent to the eventbus

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