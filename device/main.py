from machine import reset
import utime
from settings import load_config
from wifi import connect_wifi
from access_point import web_config_server
from mqtt import init_mqtt

(STATUS_CONFIG, STATUS_READY) = range(2)


def main():
    print("Starting main application...")

    config = load_config()

    status = STATUS_CONFIG
    if config:
        status = STATUS_READY

    if config and connect_wifi(config.wifi_ssid, config.wifi_password):
        status = STATUS_READY

    if status == STATUS_CONFIG:
        print("Starting device in configuration mode.")
        if web_config_server():
            utime.sleep(2)
            reset()

    elif status == STATUS_READY:
        if not connect_wifi(config.wifi_ssid, config.wifi_password):
            print("Failed to connect to WiFi, resetting device.")
            reset()
        init_mqtt()
        
    else:
        print("Unknown status, resetting device.")
        reset()


if __name__ == "__main__":
    main()
