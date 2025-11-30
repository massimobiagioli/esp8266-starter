from device_info import DeviceInfo
import utime
import ubinascii
from machine import reset, unique_id
from settings import load_settings
from wifi import connect_wifi
from access_point import web_config_server
from mqtt import init_mqtt, restart_and_reconnect


LOOP_INTERVAL = 1

STATUS_CONFIG = "status_config"
STATUS_READY = "status_ready"


# Define MQTT topics to subscribe to
MQTT_TOPICS = [
    b"notification",
]


def main():
    print("Starting main application...")

    settings = load_settings()
    device_id = ubinascii.hexlify(unique_id()).decode("utf-8")

    status = STATUS_CONFIG
    if settings:
        status = STATUS_READY

    if settings and connect_wifi(settings.wifi_ssid, settings.wifi_password):
        status = STATUS_READY

    if status == STATUS_CONFIG:
        print("Starting device in configuration mode.")
        if web_config_server():
            utime.sleep(2)
            reset()

    elif status == STATUS_READY:
        if not connect_wifi(ssid=settings.wifi_ssid, password=settings.wifi_password):
            print("Failed to connect to WiFi, resetting device.")
            reset()

        device_info = DeviceInfo(
            device_id=device_id,
            device_name=settings.device_alias or device_id,
        )

        print("Starting MQTT client...")

        def on_message(topic, msg):
            print((topic, msg))
            if topic == b"notification":
                print(f"Message received: {msg}")

        mqtt_client = init_mqtt(
            settings=settings,
            device_info=device_info,
            topics=MQTT_TOPICS,
            cb=on_message,
        )

        print("Entering main loop...")
        while True:
            try:
                mqtt_client.check_msg()
                handle_loop()
                utime.sleep(LOOP_INTERVAL)
            except OSError as e:
                print(e)
                restart_and_reconnect()

    else:
        print("Unknown status, resetting device.")
        reset()


def handle_loop():
    print("Running main loop...")


if __name__ == "__main__":
    main()
