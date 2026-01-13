import sys
import socket
from datetime import datetime
# USAGE: python3 port_scanner.py IP_ADDRESS

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Add target ip address or hostname")

print("Scan Target: " + target)
print("Scanning started: " + str(datetime.now()))

try:
    for port in range(1,65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = s.connect_ex((target,port))
        if result ==0:
            print("Port Number {} is open".format(port))
        s.close()
except KeyboardInterrupt:
    print("\n Scan stopped by user")
    sys.exit()