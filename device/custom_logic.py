topics = [
    b"notification",
]


def init_custom_logic(client):
    def sub_cb(topic, msg):
        print((topic, msg))
        if topic == b"notification":
            print(f"Message received: {msg}")

    client.set_callback(sub_cb)
