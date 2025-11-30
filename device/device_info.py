import json


DEVCE_TYPE_ESP8266 = "esp8266"


class DeviceInfo:
    def __init__(self, device_id, device_name, device_type=DEVCE_TYPE_ESP8266):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type

    def __repr__(self):
        return f"DeviceInfo(device_id={self.device_id}, device_name={self.device_name}, device_type={self.device_type})"

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "device_type": self.device_type,
        }
