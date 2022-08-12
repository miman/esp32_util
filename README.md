# esp32_util
Utility classes &amp; code for Programming MicroPython on an ESP32

This project contains a framework for programming with an eventbus concept in an ESP32 module using MicroPython.

The mindset is to have a number of Task modules integrating with different hardware & sending and/or receiving events on the event bus and then place all logic into the ***Flows*** component.

The FileTask also enables remote software upload with the option for reboot (for example when adding new logic in the flows file)

Supported Hardware:
* LED
* Buttons
* RFID reader

Supported communication;
* Normal MQTT broker
* AWS IoT MQTT broker

# Overview

## Interaction overview
Here is an overview of how the classes & config files refer to each other:

![UML Page flow](https://www.plantuml.com/plantuml/png/TLBDRhCm4BpxAIoEd-HBfE-AygEchTH8ROAKimCBjMAyn5x2eSgxju0i79CSTsOzCpkmT2GjjRLcETOD6Z34ruWKZ5kDNJ2-QZn9_Mcn0KiAN42zNC7GkdMCzH9SfEFRSMWRaSuVnm3_9pIK90AjHkPdMG5FCkdEBk4_ZFF9ymEA7h_3rYqHcXdy1jBI2IJDc7sfvYgx2yqtjqh3hh83_aUCfudKnmWWdo92un2U63D4c8_0Gp2CS8lhuGHr4tUq1qSRgJNOK6T2Uvb2aZn91pn7KwfgcXta5iYnHv_AgkgRX7_oT67I2DhTxZV_5mjst_S6ZO6S59g8M7Nk8NTKfGe8vbiSBlGUlO078vkOYvt6jePVCfsPvHhR8kewMHqF_1spX4l7PUSK4hizMTrzPHa_WBs27TRh2v6prtv_baGKs1cHUidxAxXdlS8IJD7M-XS0)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/TLBDRhCm4BpxAIoEd-HBfE-AygEchTH8ROAKimCBjMAyn5x2eSgxju0i79CSTsOzCpkmT2GjjRLcETOD6Z34ruWKZ5kDNJ2-QZn9_Mcn0KiAN42zNC7GkdMCzH9SfEFRSMWRaSuVnm3_9pIK90AjHkPdMG5FCkdEBk4_ZFF9ymEA7h_3rYqHcXdy1jBI2IJDc7sfvYgx2yqtjqh3hh83_aUCfudKnmWWdo92un2U63D4c8_0Gp2CS8lhuGHr4tUq1qSRgJNOK6T2Uvb2aZn91pn7KwfgcXta5iYnHv_AgkgRX7_oT67I2DhTxZV_5mjst_S6ZO6S59g8M7Nk8NTKfGe8vbiSBlGUlO078vkOYvt6jePVCfsPvHhR8kewMHqF_1spX4l7PUSK4hizMTrzPHa_WBs27TRh2v6prtv_baGKs1cHUidxAxXdlS8IJD7M-XS0)

## Tasks
Here is an overview of the children of the Task class

The Task class is an abstract class defining the interface the other Tasks needs to implement

A Init function & a process function

The Init function will be called after all active components have been created

The process function will be called in each main loop run

![UML Page flow](https://www.plantuml.com/plantuml/png/POyn3i8m34NtdC8Nw0qOAf0G0rqgBX2egI8I1vAVZSDNwkAeNf-_lzuVAtn1Iz6zSlfcOG4zVFqu8WLtNWmxDo2BmJVs1K_sC9Vv7MpBz0DiaYikFaOk9ZldXY2hURc6oDDQTkveNq2d_p1qwifwTSL6NI-ghl2eGuwEI7EsiP-ek9yniYmjnGq0)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/POyn3i8m34NtdC8Nw0qOAf0G0rqgBX2egI8I1vAVZSDNwkAeNf-_lzuVAtn1Iz6zSlfcOG4zVFqu8WLtNWmxDo2BmJVs1K_sC9Vv7MpBz0DiaYikFaOk9ZldXY2hURc6oDDQTkveNq2d_p1qwifwTSL6NI-ghl2eGuwEI7EsiP-ek9yniYmjnGq0)

## Event bus
Here is an overview of who uses the event bus

The eventbus is created by the GlobalProperties & can be used by anyuone with access to this

![UML Page flow](https://www.plantuml.com/plantuml/png/POz1JiCm44NtFeNNY2ZxBb1LYRAX4a9Sm6scnSAP2UFlvleaXU0wtetVdx7UtqOuHUg3EKa_21F3xeECnjeCNe8SNNXJ6KZXAHRXyvKOkrJ2L-e-NFmgs2u1mXK-V0CLV3_x-eEz3tIuw8sRjPDjr5y-qVpxRAoC7CrSnZRDqnr_CCjy2-QD6MQ_rVuHt4OuK76tTDpOG5qR2MQHBgzrecOfMPdaJbEMXY8zJrbx4WOnLihvwczjL0zw_9sLUhdcX-lCbhXBVVW1)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/POz1JiCm44NtFeNNY2ZxBb1LYRAX4a9Sm6scnSAP2UFlvleaXU0wtetVdx7UtqOuHUg3EKa_21F3xeECnjeCNe8SNNXJ6KZXAHRXyvKOkrJ2L-e-NFmgs2u1mXK-V0CLV3_x-eEz3tIuw8sRjPDjr5y-qVpxRAoC7CrSnZRDqnr_CCjy2-QD6MQ_rVuHt4OuK76tTDpOG5qR2MQHBgzrecOfMPdaJbEMXY8zJrbx4WOnLihvwczjL0zw_9sLUhdcX-lCbhXBVVW1)

## Configuration file usage
Here is an overview of how the classes use the config file:

The config file contains the entire configuration for the application

![UML Page flow](https://www.plantuml.com/plantuml/png/ROxFIiGm48VlUOfXZqBs4MHTyS_11H71ysmxhM7JIKqcUX3VNIg4D5EltpVCxpiamIXvygOBqnoOME31XpFwvnXcYk8ehTJT9x4SSp8z2fun4NI11pUkJauV8hU1cJfnWPMu-Kh_kZStk9KmEW6kR7JZkzYoLq9WxscG_NNXxJfOsvWwhsJTryRCs5rm9DYzOhga7NmRW1h-HFt26tRC8e4t-94mofbGDkPbSDilI-y2eQ7tpjDfZ7_N1ieys3pNPAW5sfGfpSkQvasqbZL6gnzp8Expv7y1)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/ROxFIiGm48VlUOfXZqBs4MHTyS_11H71ysmxhM7JIKqcUX3VNIg4D5EltpVCxpiamIXvygOBqnoOME31XpFwvnXcYk8ehTJT9x4SSp8z2fun4NI11pUkJauV8hU1cJfnWPMu-Kh_kZStk9KmEW6kR7JZkzYoLq9WxscG_NNXxJfOsvWwhsJTryRCs5rm9DYzOhga7NmRW1h-HFt26tRC8e4t-94mofbGDkPbSDilI-y2eQ7tpjDfZ7_N1ieys3pNPAW5sfGfpSkQvasqbZL6gnzp8Expv7y1)

# Components
Information of the purpose with each component can be found in this sub-page:
[Components](docs/components.md)

# Configuration
Information of the content & purpose for the config files can be found in this sub-page:
[Configuration](docs/configuration.md)


# Misc

## Micropython library aggregation site
https://awesome-micropython.com/
