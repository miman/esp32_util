# esp32_util configuration
This page describes the configuration files and their content

# Configuration
All configuration for the application is in these files:
* ***config/config.py*** 
* ***config/secrets.py***

# config.py
## Active Tasks
Which Task modules that shall be activated is read from the ***active*** flags for each component

## Buttons
Which buttons that shall be activated & what PIN each is connected to is configured in the ***button*** block

## LED
Which LED's that shall be activated & what PIN each is connected to is configured in the ***led*** block

## RFID
Which RFID reader that shall be activated & which PINs it is connected to is configured in the ***rfid*** block, for now only one is supported

## Wifi
If this taks is active or not is configured in the ***wifi*** block

## MQTT / AWS IoT
The MQTT configuration is  configured in the ***mqtt*** block.
Here you can configure:
* if you are to connect to a normal MQTT server with username/password or AWS IoT using certificates
* The hostname for a normal MQTT broker
* The AWS region & the file paths for the AWS certificates
* which topics on the internal event bus that should automatically be routed to an external MQTT broker
* which topics that the device should subscribe to from the external MQTT broker, these will automaically be sent to the eventbus (after the thing name has been removed)

## Heartbeat
How often a heartbeat should be sent to the external MQT broker configured in the ***heartbeat*** block

## File
If this taks is active or not is configured in the ***file*** block

# secrets.py
## Wifi
The username/password for connecting to Wifi configured in the ***wifi*** block

## MQTT / AWS IoT
The MQTT configuration is  configured in the ***mqtt*** block.
Here you can configure:
* The username/password for a normal MQTT briker
* The AWS host
