#!/usr/bin/python

from scapy.all import *
import ipaddress

def main():
    subnet = None
    ips = None
    ports = None
    print("Enter the type of scan that you would like to perform")
    print("1. ARP Scan")
    print("2. SYN Scan")
    print("3. Connect Scan")
    print("4. FIN Scan")
    print("5. XMAS Scan")
    print("6. ACK Scan")
    print("7. UDP Scan")
    scan = raw_input("Enter the scan you would like to perform: ")
    if scan == '1':
        subnet = raw_input("Enter subnet you would like to search: ")
    else:
        ips = raw_input("Enter IP address range(Ex. x or x,x or x-x or x/x): ")
        ports = raw_input("Enter port range(Ex. x or x,x or x-x): ")
        destination_ip, destination_ports = build_lists(ips, ports)

    if scan == '1':
        arp_scan(subnet)
    elif scan == '2':
        syn_scan(destination_ip, destination_ports)
    elif scan == '3':
        connect_scan(destination_ip, destination_ports)
    elif scan == '4':
        fin_scan(destination_ip, destination_ports)
    elif scan == '5':
        xmas_scan(destination_ip, destination_ports)
    elif scan == '6':
        ack_scan(destination_ip, destination_ports)
    elif scan == '7':
        udp_scan(destination_ip, destination_ports)


def build_lists(ips, ports):
    destination_ip=[]
    destination_ports=[]
    if ',' in ips:
        ip = ips.split(',')
        for i in ip:
            destination_ip.append(i)
    elif '-' in ips:
        ip = ips.split('-')
        start = int(ipaddress.IPv4Address(unicode(ip[0])))
        end = int(ipaddress.IPv4Address(unicode(ip[1])))
        for x in range(start, end+1):
            cur_ip = ipaddress.IPv4Address(x)
            print(str(cur_ip))
            destination_ip.append(str(cur_ip))
        #for i in range(ip[0], ip[1]):
    elif '/' in ips:
        for ip in ipaddress.IPv4Network(unicode(ips)):
            print(str(ip))
            destination_ip.append(str(ip))
    else:
        destination_ip.append(ips)

    if ',' in ports:
        port = ports.split(',')
        for i in port:
            destination_ports.append(int(i))
    elif '-' in ports:
        port = ports.split('-')
        start = int(port[0])
        end = int(port[1])
        while(start <= end):
            destination_ports.append(start)
            start+=1
    else:
        destination_ports.append(int(ports))

    return (destination_ip, destination_ports)

def arp_scan(subnet):
    packets = arping(subnet)

def connect_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="S", dport=port))
            if packet[TCP].flags == "SA":
                print("Port: " + str(port) + " is open")
                packet = send(IP(dst=ip)/TCP(flags="A", dport=port))
                packet = send(IP(dst=ip)/TCP(flags="RA", dport=port))
            else:
                print("Port: " + str(port) + " is closed")

def syn_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="S", dport=port))
            if packet[TCP].flags == "SA":
                packet = send(IP(dst=ip)/TCP(flags="R", dport=port))
                print("Port: " + str(port) + " is open")
            else:
                print("Port: " + str(port) + " is closed")


def fin_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="F", dport=port))
            if packet[TCP].flags == "R":
                print("Port: " + str(port) + " is closed or on a Windows device")
            elif packet == None:
                print("Port: " + str(port) + " is open")

def xmas_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="FPU", dport=port))
            if packet == None:
                print("Port: " + str(port) + " is open")
            elif packet[TCP].flags == "R":
                print("Port: " + str(port) + " is closed or on a Windows device")

def ack_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="A", dport=port, seq=12345), timeout=2)
            if packet == None:
                print("Port: " + str(port) + " is filtered")
            elif packet[IP].proto == 6: # 6 corresponds to TCP
                if packet[TCP].flags == "R":
                    print("Port: " + str(port) + " is unfiltered")

def udp_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/UDP(dport=port), retry=2, timeout=10)
            if packet == None:
                print("Port: " + str(port) + " is open/filtered")
            elif packet[IP].proto == 1: # 1 corresponds to ICMP
                print("Port: " + str(port) + " is closed")
            elif packet[IP].proto == 'udp':
                print("Port: " + str(port) + " is open")
            #packet.show()
main()
