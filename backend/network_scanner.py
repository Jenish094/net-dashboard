from scapy.all import ARP, Ether, srp
import sys
import ipaddress

def networkscanner(target_ip):
    # Accept user input like "192.168.1" or full CIDR"
    if not target_ip.endswith(('/24', '/25', '/26', '/27', '/28', '/29', '/30', '/31', '/32')):
        target_ip = target_ip.rstrip('.') + ".0/24"

    print(f"[network_scanner] Scanning network: {target_ip}")

    try:
        ipaddress.ip_network(target_ip, strict=False)
    except ValueError:
        print(f"[network_scanner] Invalid network: {target_ip}")
        return []
    
    # create packets
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # send packets
    result = srp(packet, timeout=3, verbose=True)[0]

    # empty list
    clients = []

    # add clients to clients[] dict
    for sent, recieved in result:
        clients.append({'ip': recieved.psrc, 'mac': recieved.hwsrc})

    print(f"[network_scanner] Found {len(clients)} client(s)")
    for c in clients:
        print(f"[network_scanner] - {c.get('ip')} {c.get('mac')}")



    #print clients
    # print("Devices on network")
    # print("IP"+ " "*18+"MAC")
    # for client in clients:
    #     print("{:16} {}".format(client['ip'], client['mac']))

    # clientip = client['ip']
    return clients