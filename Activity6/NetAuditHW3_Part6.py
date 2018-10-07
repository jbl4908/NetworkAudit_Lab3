#!/usr/bin/python

from scapy.all import *

#packets = sr(ARP(op="who-has", psrc="1.1.1.1"))

#packets = arping("10.0.0.*")
#packets2 = arping("192.168.1.*")

def main():
    print("Enter the type of scan that you would like to perform")
    print("1. ARP Scan")
    print("2. SYN Scan")
    print("3. Connect Scan")
    print("4. FIN Scan")
    print("5. XMAS Scan")
    print("6. ACK Scan")
    print("7. UDP Scan")
    scan = raw_input("Enter the scan you would like to perform: ")
    ips = raw_input("Enter IP address range(Ex. x or x,x or x-x): ")
    ports = raw_input("Enter port range(Ex. x or x,x or x-x): ")

    destination_ip=[]
    if ',' in ips:
        ip = ips.split(',')
        for i in ip:
            destination_ip.append(i)
    elif '-' in ips:
        ip = ips.split('-')
        for i in range(ip[0], ip[1]):
            
def arp_scan(subnet):
    packets = arping("10.0.0.*")

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
                print("Port: " + str(port) + " is open")
            else:
                print("Port: " + str(port) + " is closed")
            packet = send(IP(dst=ip)/TCP(flags="R", dport=port))

def fin_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="F", dport=port))

def xmas_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="FPU", dport=port))
            if packet == None:
                print("Port: " + str(port) + " is open")
            elif packet[TCP].flags == "R":
                print("Port: " + str(port) + " is closed")

def ack_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="A", dport=port, seq=12345))

def udp_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr(IP(dst=ip)/UDP(dport=port), retry=2, timeout=10)
main()
#fin_scan("10.0.0.25", [912])
#packet = TCP(raw(packet))
#print(packet[TCP].flags)
#hexdump(packet)
#print(packets.summary())
