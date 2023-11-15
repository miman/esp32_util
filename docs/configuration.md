# esp32_util configuration
This page describes the configuration files and their content

# Configuration
All configuration for the application is in these files:
* ***config/config.py*** 
* ***config/secrets.py***

# config.py
## Active Tasks
Which Task modules that shall be activated is read from the ***active*** flags for each component

## Wifi
If this taks is active or not is configured in the ***wifi*** block

## Task configuration
The configuration for each task type can be found in the task description page here: [Tasks](tasks/tasks-main.md)

# secrets.py
This file contains the secrets that is used in the config file, to keep this separate

## Wifi
The username/password for connecting to Wifi configured in the ***wifi*** block

## MQTT / AWS IoT
The MQTT configuration is  configured in the ***mqtt*** block.
Here you can configure:
* The username/password for a normal MQTT briker
* The AWS host
