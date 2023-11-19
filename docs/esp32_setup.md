# How to setup the ESP 32 for development

# On Raspberry PI

On the Raspberry PI we use the development tool Thonny

## Configure Thonny

Go to the menu item: **Tools / Manage Plug-ins**

Search for **esptool**

Click on it & install

The select **Tools/Options** & select the interpreter **MicroPython (ES32)**.
The auto detect for the port usually works fine.

Then click on the **Install or update firmware** link on the same page to install the MicroPyton binary on the ESP 32 (see below on how to etch the .bin file)

## ESP32 Micropython driver

For the Freenove device get the driver from here:

https://micropython.org/download/ESP32_GENERIC/

Use the one under the header: Firmware (Support for SPIRAM / WROVER)

