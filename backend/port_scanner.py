import sys
import socket
from datetime import datetime
import requests
import network_scanner
# USAGE: python3 port_scanner.py IP_ADDRESS

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Add target ip address or hostname")

print("Scan Target: " + target)
print("Scanning started: " + str(datetime.now()))

open_ports = []

try:
    for port in range(1,65536):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = s.connect_ex((target,port))
        if result ==0:
            print("Port Number {} is open".format(port))
            open_ports.append(port)
        s.close()
except KeyboardInterrupt:
    print("\n Scan stopped by user")
    sys.exit()


clientip = network_scanner.clientip
print(f"client ip: " + clientip)

#check if a website is hosted on the port
def check_website():
    ok = []
    deny = []
    for p in open_ports:
        url = f"http://{clientip}:{p}"
        print(f"{url}")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(f"Status Code: {response.status_code}")
            if 200 <= response.status_code <= 299:
                ok.append(response.status_code)
                print("WEBSERVER")
            else:
                deny.append(p, response.status_code)
                print("NO WEBSERVER")
        except requests.exceptions.Timeout:
            print("Timed out")
            deny.append((p, "timeout"))
        except requests.exceptions.ConnectionError:
            print("Connection error")
            deny.append((p, "connection_error"))
        except requests.exceptions.RequestException as e:
            print(f"Error {e}")
            deny.append((p, str(e)))
    print(f"ok list: {ok}, deny list: {deny}")
    #make a request to the website

check_website()

