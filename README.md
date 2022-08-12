# esp32_util
Utility classes &amp; code for Programming MicroPython on an ESP32

This project contains a framework for programming with an eventbus concept in an ESP32 module using MicroPython.

The mindset is to have a number of Task modules integrating with different hardware & sending and/or receiving events on the event bus and then place all logic into the ***Flows*** component.

# Overview

## Interaction overview
Here is an overview of how the classes & config files refer to each other:

![UML Page flow](https://www.plantuml.com/plantuml/png/TPBDRi8m48JlVWehnqgv8FKQyQFILYfI2v4ucsH3BHnlQc_8eUBTQqX3bvXUa7PcFH-pojIJSjJMHXHODsZ1afmZ4XkN1ZisFXlSAVFki0576ZopdexXTzvw8SuHCitwj_tGDc6E7ey5-P0Qg2XbMOqg3ceFCicLF_X4VWif_vXlK9xr6stU4g6Dv1S8LNUWA7BMbOvJLbzqsPGYo7s7D1juN68ufd8QDpXiq1ZhD2ui2Ufct7eDdXRA670yXQaXfbIaTif3U6OhlHVtRktq_fFIwmOhlrml7YSJSNkE1LeB1Mcq8sFM-RlULbUQ6MBetfV-PLpB1t646NaHwLAz_sAo25OORClHuPBPTYDVCK-ayb9rNYE9qp-hguyybnjmHt2NzJhWlJkUzwD_afROsJGR8czRoC4T4gPWoxOsFm00)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/TPBDRi8m48JlVWehnqgv8FKQyQFILYfI2v4ucsH3BHnlQc_8eUBTQqX3bvXUa7PcFH-pojIJSjJMHXHODsZ1afmZ4XkN1ZisFXlSAVFki0576ZopdexXTzvw8SuHCitwj_tGDc6E7ey5-P0Qg2XbMOqg3ceFCicLF_X4VWif_vXlK9xr6stU4g6Dv1S8LNUWA7BMbOvJLbzqsPGYo7s7D1juN68ufd8QDpXiq1ZhD2ui2Ufct7eDdXRA670yXQaXfbIaTif3U6OhlHVtRktq_fFIwmOhlrml7YSJSNkE1LeB1Mcq8sFM-RlULbUQ6MBetfV-PLpB1t646NaHwLAz_sAo25OORClHuPBPTYDVCK-ayb9rNYE9qp-hguyybnjmHt2NzJhWlJkUzwD_afROsJGR8czRoC4T4gPWoxOsFm00)

## Tasks
Here is an overview of the children of the Task class

The Task class is an abstract class defining the interface the other Tasks needs to implement

A Init function & a process function

The Init function will be called after all active components have been created

The process function will be called in each main loop run

![UML Page flow](https://www.plantuml.com/plantuml/png/POyn3i8m40Hxl-8-a1zGHD1GG1Fn0KCE566VmLvtF1ufpIgvTdQzdXiROaNFAJnA_XHJWznYUmSHWelEZXqxKCpXiyQAkqQuP7ekVkNw1NnJ6qun9QskEvMEnLxhao2hgHn-mq15CYfkC1LTGaN2_RSIP8_OyuiyPLIRUqv_)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/POyn3i8m40Hxl-8-a1zGHD1GG1Fn0KCE566VmLvtF1ufpIgvTdQzdXiROaNFAJnA_XHJWznYUmSHWelEZXqxKCpXiyQAkqQuP7ekVkNw1NnJ6qun9QskEvMEnLxhao2hgHn-mq15CYfkC1LTGaN2_RSIP8_OyuiyPLIRUqv_)

## Event bus
Here is an overview of who uses the event bus

The eventbus is created by the GlobalProperties & can be used by anyuone with access to this

![UML Page flow](https://www.plantuml.com/plantuml/png/RO_12i8m38RlVOgUXTBx3Z86waL1P2_GhL67MJFRrBs-JgZQpLlv_ZJv_ZAmyHnx55Asr0_amB7S8eqPs24r1e-U1l3SGSZ2pGCSLp67Ux2r2RUCLP6Pt08VximBU3ftjeR0GinlI-MxovNLvsuXQNH1JD9IgVKFNudqVWVJn0I_7hDvZTGQr0qx7TWmPDzJfK8YM1s0HNBylyM_Kf6wBSHAS3Rs-0G0)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/RO_12i8m38RlVOgUXTBx3Z86waL1P2_GhL67MJFRrBs-JgZQpLlv_ZJv_ZAmyHnx55Asr0_amB7S8eqPs24r1e-U1l3SGSZ2pGCSLp67Ux2r2RUCLP6Pt08VximBU3ftjeR0GinlI-MxovNLvsuXQNH1JD9IgVKFNudqVWVJn0I_7hDvZTGQr0qx7TWmPDzJfK8YM1s0HNBylyM_Kf6wBSHAS3Rs-0G0)

## Configuration file usage
Here is an overview of how the classes use the config file:

The config file contains the entire configuration for the application

![UML Page flow](https://www.plantuml.com/plantuml/png/ROx1IiGm48RlUOfXZqBs4MHT4JqeY0YUf-sqXaqdCPdeGNntwM5eq-pr-uRvlrCMJ59cR_emny340ey-TEXVKuYKn57Ug8TlOZcNR0OKx30Jz857DsrENhv4xWCpzU82xyJTJxxgFjpeDiBi4-369ZTzYjKz3O6Zfr6EjyhhTR2sCZhVIDrlZOdONt0YEBnZlkG3_1g0DVoPXeLNx5n40ZVuYJ19HoYDUHjT-sNfNI0O0pe3jiGr3NIfDVgouVfrpwkuMlwP4_5GPlyF)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/ROx1IiGm48RlUOfXZqBs4MHT4JqeY0YUf-sqXaqdCPdeGNntwM5eq-pr-uRvlrCMJ59cR_emny340ey-TEXVKuYKn57Ug8TlOZcNR0OKx30Jz857DsrENhv4xWCpzU82xyJTJxxgFjpeDiBi4-369ZTzYjKz3O6Zfr6EjyhhTR2sCZhVIDrlZOdONt0YEBnZlkG3_1g0DVoPXeLNx5n40ZVuYJ19HoYDUHjT-sNfNI0O0pe3jiGr3NIfDVgouVfrpwkuMlwP4_5GPlyF)
# Configuration

## Active Tasks
Which Task modules that shall be activated is configured in teh  ***config/tasks_settings.py***
In this file we also configure the name of the thing and some common settings

## Buttons
Which buttons that shall be activated & what PIN each is connected to is configured in the ***config/btn_config.py***

## LED
Which LED's that shall be activated & what PIN each is connected to is configured in the ***config/led_config.py***

## RFID
Which RFID reader that shall be activated & which PINs it is connected to is configured in the ***config/rfid_config.py***, for now only one is supported

# Flow
The mindset is that all interaction logic between the modules is done the the flows.py component

# Micropython library aggregation site
https://awesome-micropython.com/
