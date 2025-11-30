from umqttsimple import MQTTClient
import machine
import json
import time


MESSAGE_INTERVAL = 5
OUTBOUND_TOPIC = b"from_device"
DEVICE_STATUS_TOPIC = b"device_status"
EVENT_CONNECTED = "connected"
EVENT_DISCONNECTED = "disconnected"
KEEP_ALIVE_INTERVAL = 300


def restart_and_reconnect():
    time.sleep(10)
    machine.reset()


def send_message(client, topic, event_type, payload=None, retain=True, qos=1):
    event = {
        "event_type": event_type,
        "timestamp": time.time(),
        "payload": payload if payload is not None else {},
    }
    client.publish(topic, json.dumps(event).encode("utf-8"), retain=retain, qos=qos)


def set_on_disconnect(client, payload=None):
    last_will_message = {
        "event_type": EVENT_DISCONNECTED,
        "timestamp": time.time(),
        "payload": payload if payload is not None else {},
    }
    client.set_last_will(
        DEVICE_STATUS_TOPIC,
        json.dumps(last_will_message).encode("utf-8"),
        retain=True,
        qos=1,
    )


def connect_to_broker(client, device_info):
    try:
        set_on_disconnect(client, device_info.to_dict())
        client.connect()
        send_message(
            client, DEVICE_STATUS_TOPIC, EVENT_CONNECTED, device_info.to_dict()
        )
    except OSError as e:
        print(e)
        print("Failed to connect to MQTT broker. Reconnecting...")
        restart_and_reconnect()


def init_mqtt(settings, device_info, topics=[], cb=None):
    client = MQTTClient(
        device_info.device_id,
        settings.mqtt_broker,
        user=settings.mqtt_user,
        password=settings.mqtt_password,
        keepalive=KEEP_ALIVE_INTERVAL,
    )

    connect_to_broker(client, device_info)
    print("Connected to MQTT broker: %s" % (settings.mqtt_broker))

    if cb:
        client.set_callback(cb)

    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")

    return client
