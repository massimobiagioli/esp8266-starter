import ujson


CONFIG_FILE = "conf/settings.json"


class Settings:
    def __init__(
        self,
        wifi_ssid="",
        wifi_password="",
        mqtt_broker="",
        mqtt_user="",
        mqtt_password="",
    ):
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.mqtt_broker = mqtt_broker
        self.mqtt_user = mqtt_user
        self.mqtt_password = mqtt_password

    @classmethod
    def from_dict(cls, data):
        return cls(
            wifi_ssid=data.get("wifi_ssid", ""),
            wifi_password=data.get("wifi_password", ""),
            mqtt_broker=data.get("mqtt_broker", ""),
            mqtt_user=data.get("mqtt_user", ""),
            mqtt_password=data.get("mqtt_password", ""),
        )

    def to_dict(self):
        return {
            "wifi_ssid": self.wifi_ssid,
            "wifi_password": self.wifi_password,
            "mqtt_broker": self.mqtt_broker,
            "mqtt_user": self.mqtt_user,
            "mqtt_password": self.mqtt_password,
        }


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return Settings.from_dict(ujson.load(f))
    except (OSError, ValueError):
        print("No configuration file found or invalid format.")
        return None


def save_config(settings):
    with open(CONFIG_FILE, "w") as f:
        ujson.dump(settings.to_dict(), f)
