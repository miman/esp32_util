# esp32_util
Utility classes &amp; code for Programming MicroPython on an ESP32

This project contains a framework for programming with an eventbus concept in an ESP32 module using MicroPython.

The mindset is to have a number of Task modules integrating with different hardware & sending and/or receiving events on the event bus and then place all logic into the ***Flows*** component.

# Overview

## Interaction overview
Here is an overview of how the classes & config files refer to each other:

![UML Page flow](https://www.plantuml.com/plantuml/png/PPF1RhCm48JlF8MLUowH_ckKFr7J7fggYYBrY1PO8Yl69lPI3bNVlH1QTh6F-yqodXs9NI3mr3KcArtJEekMrDuv4kFHk5wCpyOLODwzQz6JnY2afq-qjEz2beqMQhsTlfs6hXtcvECOgBN1cePDzcgXlC4LrUe2uHPMwYjJYjzynMha2xRlY9nDy0k2fmA14kLSw-g2WHRmVnzETwA4lpdVW9cbGPiEN6yv32EHXMaSXGLEmeo3I1pd-8wRKeHD6zTrna07C0Qzj68wsbH0K4101Nt8jQCy896sry1ASoU1cHkiyjBPMb-P-Lgdi22Ri5xNEYyzLcX9WnbyV_iSCqfhxdHKfDTVVGyk7-OE9oqvRMwJTw8ZkSJJyNpujzb8CgmUdBLOadPM21_3JK9O19nzed2HMnGjNNZyOFEF4xsu7EUjfEiTsgfhp0y0)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/PPF1RhCm48JlF8MLUowH_ckKFr7J7fggYYBrY1PO8Yl69lPI3bNVlH1QTh6F-yqodXs9NI3mr3KcArtJEekMrDuv4kFHk5wCpyOLODwzQz6JnY2afq-qjEz2beqMQhsTlfs6hXtcvECOgBN1cePDzcgXlC4LrUe2uHPMwYjJYjzynMha2xRlY9nDy0k2fmA14kLSw-g2WHRmVnzETwA4lpdVW9cbGPiEN6yv32EHXMaSXGLEmeo3I1pd-8wRKeHD6zTrna07C0Qzj68wsbH0K4101Nt8jQCy896sry1ASoU1cHkiyjBPMb-P-Lgdi22Ri5xNEYyzLcX9WnbyV_iSCqfhxdHKfDTVVGyk7-OE9oqvRMwJTw8ZkSJJyNpujzb8CgmUdBLOadPM21_3JK9O19nzed2HMnGjNNZyOFEF4xsu7EUjfEiTsgfhp0y0)

## Tasks
Here is an overview of the children of the Task class

![UML Page flow](https://www.plantuml.com/plantuml/png/PS-z3G8n3CNnFbDuWTk0ue260YZGBM0u8o6S198NqJ0y7mMMIVjxalNtMC45BMeWEkLuoqaIQE9w3KwsCd_GsQe1ENMy4Iuu2gDR3kVBF4c5m-MZxkv0v_jS8kjl2lIjeiLp6Ap6p6eSTpMsM8sXhp7_g_5VlM7DgbByUUCmIffRr1S0)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/PS-z3G8n3CNnFbDuWTk0ue260YZGBM0u8o6S198NqJ0y7mMMIVjxalNtMC45BMeWEkLuoqaIQE9w3KwsCd_GsQe1ENMy4Iuu2gDR3kVBF4c5m-MZxkv0v_jS8kjl2lIjeiLp6Ap6p6eSTpMsM8sXhp7_g_5VlM7DgbByUUCmIffRr1S0)

## Event bus
Here is an overview of who uses the event bus

![UML Page flow](https://www.plantuml.com/plantuml/png/ROz1Je0m44NtFKNN9attB0oIg1irnd21GaSbJZlOcShr1HAK0fkcUV-tURzcSKboGALrJs6a257q0z9KW4Uapk5heX6I3C15UFypdqqkuHFurl5NmPeiGl64xoP-_XPfWQNWBvI2mylexNtmArH7CstIyF4fvi-gqZH5LiiaRSpjZj-exRu6IsE1_vQ7laNg7TfEecLn0iNpRN2b4Rnb4BKvNl-IvbJjbf_SolMdMDKGVGxu2m00)

[PlantUML edit page for picture above](http://www.plantuml.com/plantuml/uml/ROz1Je0m44NtFKNN9attB0oIg1irnd21GaSbJZlOcShr1HAK0fkcUV-tURzcSKboGALrJs6a257q0z9KW4Uapk5heX6I3C15UFypdqqkuHFurl5NmPeiGl64xoP-_XPfWQNWBvI2mylexNtmArH7CstIyF4fvi-gqZH5LiiaRSpjZj-exRu6IsE1_vQ7laNg7TfEecLn0iNpRN2b4Rnb4BKvNl-IvbJjbf_SolMdMDKGVGxu2m00)

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
