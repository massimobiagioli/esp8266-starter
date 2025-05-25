from umqttsimple import MQTTClient
import machine
import ubinascii
import time


MQTT_SERVER = b"raspberrypi.homenet.telecomitalia.it"
MQTT_PORT = 1883
MQTT_USER = "mosquitto"
MQTT_PASS = "mosquitto"

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC_SUB = b"notification"
TOPIC_PUB = b"hello"

MESSAGE_INTERVAL = 5


def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b"notification":
        print(f"Message received: {msg}")


def connect_and_subscribe():
    client = MQTTClient(CLIENT_ID, MQTT_SERVER, user=MQTT_USER, password=MQTT_PASS)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(TOPIC_SUB)
    print(
        "Connected to %s MQTT broker, subscribed to %s topic" % (MQTT_SERVER, TOPIC_SUB)
    )
    return client


def restart_and_reconnect():
    print("Failed to connect to MQTT broker. Reconnecting...")
    time.sleep(10)
    machine.reset()


def init_mqtt():
    try:
        client = connect_and_subscribe()
    except OSError as e:
        print(e)
        restart_and_reconnect()

    # last_message = 0
    # counter = 0

    while True:
        try:
            client.check_msg()
            # if (time.time() - last_message) > MESSAGE_INTERVAL:
            #     msg = b'Hello #%d' % counter
            #     client.publish(TOPIC_PUB, msg)
            #     last_message = time.time()
            #     counter += 1
        except OSError:
            restart_and_reconnect()
