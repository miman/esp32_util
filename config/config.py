# This file contains the configuration for the ESP32
config = {
    "thing_id": "ESP32_A",  # The id of this device
    "wifi": {
        "active": True  # If the Wifi should be active or not (pre-req for MQTT for example)
    },
    "mqtt": {
        "active": True,  # If this module should be active or not
        "mqtt_type": "AWS",  # AWS or Normal
        "normal": {
            "mqtt_host": "192.168.68.121"
        },
        "aws": {
            "aws_region": "eu-west-1",
            "keyfile_path": "/certs/thing-private.pem.key",
            "certfile_path": "/certs/thing-certificate.pem.crt"
        },
        "mqtt_routing": {
            "topics_to_route_externally": [  # - which topics that should be routed to offboard MQTT server
                {
                    "internal": "btn/state",
                    "external": "btn/state"
                },
                {
                    "internal": "file/content",
                    "external": "file/content"
                },
                {
                    "internal": "rfid",
                    "external": "rfid"
                }                
            ],
            "topics_to_subscribe_to": [  # - Which topics we should subscribe to from the offboard MQTT server
                "txt/#",
                "led/#",
                "file/write",
                "file/read",
                "file/remove"
            ],
            "topics_to_extract_device_id": [  # - Which topics we should extract the last item in the topic & place in device_id field
                {
                    "topic": "led",
                    "location": 2
                }
            ]
        }
    },
    "led": {
        "active": True,  # If this module should be active or not
        "leds": [  # List of RFID readers connected to the device
            {
                "id": "red",
                "pin": 14,
                "in_out": "OUT"
            },
            {
                "id": "internal_blue",
                "pin": 2,
                "in_out": "OUT"
            },
        ]
    },
    "button": {
        "active": True,  # If this module should be active or not
        "buttons": [  # List of buttons connected to the device
            {
                "id": "ext1",
                "pin": 15
            },
            {
                "id": "internal_boot",
                "pin": 0
            }
        ]        
    },
    "rfid_reader": {
        "active": True,  # If this module should be active or not
        "rfid_readers": [  # List of RFID readers connected to the device
            {
                "id": "1",
                "spi_port": 2,
                "gpio_rst": 4,
                "gpio_cs": 5
            }
        ]
    },
    "heartbeat": {
        "active": True,  # If this module should be active or not
        # How often shall the heartbeat service send a heartbeat over MQTT
        "heartbeat_timeout_ms": 600000  # Every 10 mins
    },
    "file": {
        "active": True
    },
    "rest_caller": {
        "active": False,  # If this module should be active or not
    }
}
