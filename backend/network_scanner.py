from scapy.all import ARP, Ether, srp
import sys

def networkscanner():
    #create packets
    target_ip = sys.argv[1]
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    #send packets
    result = srp(packet, timeout=3)[0]

    #empty list
    clients = []

    # add clients to clients[] list
    for sent, recieved in result:
        clients.append({'ip': recieved.psrc, 'mac': recieved.hwsrc})



    #print clients
    print("Devices on network")
    print("IP"+ " "*18+"MAC")
    for client in clients:
        print("{:16} {}".format(client['ip'], client['mac']))

    clientip = client['ip']
    return clients

networkscanner()