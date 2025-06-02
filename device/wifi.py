import network
import utime


DEFAULT_TIMEOUT = 10


def connect_wifi(ssid, password, timeout=DEFAULT_TIMEOUT):
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
