from machine import reset
import utime
from wifi import load_config, connect_wifi
from access_point import web_config_server
from mqtt import init_mqtt


def main():
    config = load_config()
    
    if config and connect_wifi(config["ssid"], config["password"]):
        init_mqtt()   # Start MQTT (placeholder)
        return
    
    # Fallback to AP mode if no config/connection fails
    print("Starting configuration mode...")
    if web_config_server():
        utime.sleep(2)
        reset()  # Reboot after saving config


if __name__ == "__main__":
    main()