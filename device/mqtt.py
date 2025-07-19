from umqttsimple import MQTTClient
import machine
import ubinascii
import time
from custom_logic import init_custom_logic
from device_info import DeviceInfo

client_id = ubinascii.hexlify(machine.unique_id())

device_info = DeviceInfo(
    device_id=client_id.decode("utf-8"), device_name="tester", device_type="esp32"
)

MESSAGE_INTERVAL = 5
OUTBOUND_TOPIC = b"from_device"
DEVICE_STATUS_TOPIC = b"device_status"
EVENT_CONNECTED = "connected"
EVENT_DISCONNECTED = "disconnected"


def restart_and_reconnect():
    time.sleep(10)
    machine.reset()


def notify_event(client, topic, event_type, payload=None, retain=True, qos=1):
    event = {
        "event_type": event_type,
        "timestamp": time.time(),
        "payload": payload if payload is not None else {},
    }
    client.publish(topic, str(event).encode("utf-8"), retain=retain, qos=qos)


def set_on_disconnect(client, payload=None):
    last_will_message = {
        "event_type": EVENT_DISCONNECTED,
        "timestamp": time.time(),
        "payload": payload if payload is not None else {},
    }
    client.set_last_will(
        DEVICE_STATUS_TOPIC, str(last_will_message).encode("utf-8"), retain=True, qos=1
    )


def connect_to_broker(client):
    try:
        set_on_disconnect(client, device_info.to_dict())
        client.connect()
        notify_event(
            client, DEVICE_STATUS_TOPIC, EVENT_CONNECTED, device_info.to_dict()
        )
    except OSError as e:
        print(e)
        print("Failed to connect to MQTT broker. Reconnecting...")
        restart_and_reconnect()


def init_mqtt(mqtt_broker, mqtt_user, mqtt_pass, topics):
    client = MQTTClient(
        client_id, mqtt_broker, user=mqtt_user, password=mqtt_pass, keepalive=60
    )
    init_custom_logic(client)
    connect_to_broker(client)
    print("Connected to MQTT broker: %s" % (mqtt_broker))

    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")

    while True:
        try:
            client.check_msg()
            time.sleep(MESSAGE_INTERVAL)
        except OSError:
            restart_and_reconnect()
