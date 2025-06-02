from umqttsimple import MQTTClient
import machine
import ubinascii
import time
from custom_logic import init_custom_logic


MESSAGE_INTERVAL = 5

client_id = ubinascii.hexlify(machine.unique_id())


def restart_and_reconnect():
    time.sleep(10)
    machine.reset()


def init_mqtt(mqtt_broker, mqtt_user, mqtt_pass, topics):
    try:
        client = MQTTClient(client_id, mqtt_broker, user=mqtt_user, password=mqtt_pass)
        init_custom_logic(client)
        client.connect()
        print("Connected to %s MQTT broker" % (mqtt_broker))

        for topic in topics:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")

    except OSError as e:
        print(e)
        print("Failed to connect to MQTT broker. Reconnecting...")
        restart_and_reconnect()

    while True:
        try:
            client.check_msg()
            time.sleep(MESSAGE_INTERVAL)
        except OSError:
            restart_and_reconnect()
