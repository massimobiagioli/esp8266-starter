import network
import usocket
from settings import Settings, save_config


ACCESS_POINT_SSID = "NodeMCU-Config"
ACCESS_POINT_PASSWORD = "config123"
ACCESS_POINT_ADDRESS = "http://192.168.4.1"

CONNECTION_TIMEOUT = 2.0
CHUNK_SIZE = 512


def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ACCESS_POINT_SSID, password=ACCESS_POINT_PASSWORD)
    return ap


def web_page():
    try:
        with open('templates/index.html', 'r') as file:
            html = file.read()
    except:
        html = """
        <!DOCTYPE html>
        <html>
            <head><title>Error</title></head>
            <body><h1>Error loading page</h1></body>
        </html>
        """
    return html


def web_config_server():
    _ = start_ap()
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.bind(("", 80))
    s.listen(5)

    print(f"Web server running. Connect to {ACCESS_POINT_ADDRESS} to configure WiFi.")

    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = handle_request(conn)

        if "POST /configure" in request:
            body = request.split("\r\n\r\n")[1]
            params = body.split("&")
            wifi_ssid = params[0].split("=")[1].replace("%20", " ")
            wifi_password = params[1].split("=")[1].replace("%20", " ")
            mqtt_broker = params[2].split("=")[1].replace("%20", " ")
            mqtt_user = params[3].split("=")[1].replace("%20", " ")
            mqtt_password = params[4].split("=")[1].replace("%20", " ")

            save_config(
                Settings(
                    wifi_ssid=wifi_ssid,
                    wifi_password=wifi_password,
                    mqtt_broker=mqtt_broker,
                    mqtt_user=mqtt_user,
                    mqtt_password=mqtt_password,
                )
            )
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            conn.send("<h1>Configuration saved! Rebooting...</h1>")
            conn.close()
            return True

        else:
            conn.send("HTTP/1.1 200 OK\n")
            conn.send("Content-Type: text/html\n")
            conn.send("Connection: close\n\n")
            conn.sendall(web_page())
            conn.close()


def handle_request(conn):
    conn.settimeout(CONNECTION_TIMEOUT)
    request_raw = b""
    try:
        while True:
            chunk = conn.recv(CHUNK_SIZE)
            if not chunk:
                break
            request_raw += chunk
    except OSError:
        pass

    return request_raw.decode("utf-8")
