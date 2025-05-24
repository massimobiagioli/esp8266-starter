import network
import ujson
import utime


CONFIG_FILE = "conf/wifi.json"


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return ujson.load(f)
    except:
        return None


def save_config(ssid, password):
    config = {"ssid": ssid, "password": password}
    with open(CONFIG_FILE, "w") as f:
        ujson.dump(config, f)


def connect_wifi(ssid, password, timeout=10):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    
    print(f"Connecting to {ssid}...")
    for _ in range(timeout * 2):  # Timeout in seconds
        if sta_if.isconnected():
            print("WiFi connected!")
            print("IP:", sta_if.ifconfig()[0])
            return True
        utime.sleep(0.5)
    
    print("Error: Connection failed!")
    return False