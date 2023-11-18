# This file contains the configuration for the ESP32
config = {
    "wifi": {
        "active": True  # If the Wifi should be active or not (pre-req for MQTT for example)
    },
    "mqtt": {
        "active": False,  # If this module should be active or not
        "mqtt_type": "AWS",  # AWS or Normal
        "aws": {
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
                "pin": 5
            },
            {
                "id": "internal_boot",
                "pin": 0
            }
        ]        
    },
    "rfid_reader": {
        "active": False,  # If this module should be active or not
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
    "hcsr04": {
        "active": False,  # If this module should be active or not
        "sensors": [  # List of buttons connected to the device
            {
                "id": "dist_1",
                "trigger_pin": 27,
                "echo_pin": 26,
                "time_between_runs_us": 250000
            }
        ]        
    },
    "motor": {
        "active": False,
        "motors": [  # List of motors connected to the device
            {
                "id": "1",
                "motor_pin": 2,
                "reverse_ctrl_pin": 4,
                "forward_ctrl_pin": 5,
                "freq": 1000   # defaults to 1000
                # "speed": 512  # defaults to 0
            }
        ]
    },
    "lcd": {
        "active": False,
        "lcds": [  # List of motors connected to the device
            {
                "id": "lcd_1",
                "scl_pin": 22,
                "sda_pin": 21
                # "total_rows": 2,    # defaults to 2
                # "total_columns": 16, # defaults to 16
                # "i2c_addr": 0x27,      # defaults to 0x27
                # "freq": 10000,    # defaults to 10000
                # "speed": 512  # defaults to 0
            }
        ]
    },
    "servo": {
        "active": False,
        "servos": [  # List of servos connected to the device
            {
                "id": "servo_1",
                "ctrl_pin": 15,
                "start_value": 50,
                "min_value": 40,
                "max_value": 115,
                "freq": 50   # defaults to 50
            }
        ]
    },
    "rest_caller": {
        "active": False,  # If this module should be active or not
    }
}
