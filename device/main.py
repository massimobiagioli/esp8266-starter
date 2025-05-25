from machine import reset
import utime
from settings import load_config
from wifi import connect_wifi
from access_point import web_config_server
from mqtt import init_mqtt


def main():
    config = load_config()

    if config and connect_wifi(config.wifi_ssid, config.wifi_password):
        init_mqtt()
        return

    # Fallback to AP mode if no config/connection fails
    print("Starting configuration mode...")
    if web_config_server():
        utime.sleep(2)
        reset()


if __name__ == "__main__":
    main()
