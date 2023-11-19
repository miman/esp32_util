# This file contains the configuration specific for this specific device
device_specific_config = {
    "thing_id": "ESP32_Test",  # The id of this device
    "mqtt": {
        "normal": {
            "mqtt_host": "192.168.68.121"
        },
        "aws": {
            "aws_region": "eu-west-1",
        },
    }
}
