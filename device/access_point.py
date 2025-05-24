import network
import usocket
import ujson
from wifi import save_config

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

def web_config_server():
    ap = start_ap()
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    
    print(f"Web server running. Connect to {ACCESS_POINT_ADDRESS} to configure WiFi.")
    
    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = handle_request(conn)
        
        if "POST /configure" in request:
            body = request.split("\r\n\r\n")[1]
            params = body.split("&")
            ssid = params[0].split("=")[1].replace("%20", " ")
            password = params[1].split("=")[1].replace("%20", " ")
            
            save_config(ssid, password)
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            conn.send("<h1>Configuration saved! Rebooting...</h1>")
            conn.close()
            return True
        
        else:
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>WiFi Setup</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <h1>WiFi Configuration</h1>
                <form method="post" action="/configure">
                    <label>SSID:</label><br>
                    <input type="text" name="ssid" required><br><br>
                    <label>Password:</label><br>
                    <input type="password" name="password" required><br><br>
                    <button type="submit">Save & Reboot</button>
                </form>
            </body>
            </html>
            """
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            conn.send(html)
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

    return request_raw.decode('utf-8')