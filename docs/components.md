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

## HeartbetTask
This task will send a heartbeat message at regular intevalls to the eventbus (which then can be routed to the offboard MQTT server

### heartbeat
Once every X ms an heartbeat message will be sent  on the ***heartbeat*** topic to the eventbus
The payload will contain the RFID card number
How often the heartbeat should be sent is configured in the config file.

### Payload format
The payload for ***heartbeat*** is:

```
{
   "time": 1234567,
    "content": "heartbeat",
    "freeMem": 123
}
```

## MqttTask
This task will do a number of tasks, all of them configured in the config file under the ***mqtt*** block
* Route any message from a list pf topics from the eventbus to the offboard MQTT broker onto a topic name defined in the same config block.
* Subscribe to a list of topics from the offboard MQTT broker & route these to the eventbus
  * after removing the thing-name in the first place in the topic
* Move one location in the topic to the device_id parameter & remove this from the topic
  * This to make the eventbus logic simpler
* Write the content of a message to the console for msgs posted to the topic ***txt/write***

### txt/write
Write the content of a message to the console for msgs posted to the topic ***txt/write***

### Payload format
The payload for ***txt/write*** is:

```
{
    "content": "Msg to write to console :-)"
}
```

## FileTask
This task will do a number of file operation tasks on the ESP 32
* Write the given file content to the given file path
* Read a file path with a given name & return the content on topic ***file/content***
* Delete the file with the given file path

### file/write
Write the given file content to the given file path msgs posted to the topic ***file/write***
If the reboot flag is present & set to true the device will be rebooted after the file has been written.
This could for example be used foe remote software updates.

### Payload format
The payload for ***file/write*** is:

```
{
    "path": "dir/filename.py",
    "content": "File content",
    "reboot": false
}
```

### file/read
Read a file path with a given name msgs posted to the topic ***file/read*** & return the content on topic ***file/content***

### Payload format
The payload for ***file/read*** is:

```
{
    "path": "dir/filename.py"
}
```

### file/remove
Write the given file content to the given file path msgs posted to the topic ***file/remove***

### Payload format
The payload for ***file/remove*** is:

```
{
    "path": "dir/filename.py",
    "content": "File content"
}
```

### file/content
When asked to read a file a message with the file content will be sent to this topic ***file/content***

### Payload format
The payload for ***file/content*** is:

```
{
    "path": "dir/filename.py",
    "content": "File content"
}
```
