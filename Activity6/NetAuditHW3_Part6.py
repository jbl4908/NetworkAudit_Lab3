#!/usr/bin/python

from scapy.all import *
import ipaddress
import sys

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
        destination_ip=[]
        try:
            network = ipaddress.IPv4Network(unicode(subnet))
        except ValueError, e:
            print("illegal subnet")
            print("Exception: %s" % str(e))
            sys.exit(1)
        for ip in network:
            destination_ip.append(str(ip))
    elif int(scan)>=2 and int(scan)<=7:
        ips = raw_input("Enter IP address range(Ex. x or x,x or x-x or x/x): ")
        ports = raw_input("Enter port range(Ex. x or x,x or x-x): ")
        destination_ip, destination_ports = build_lists(ips, ports)
    else:
        print("Choice entered is invalid, aborting")
        sys.exit(1)

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
            is_valid_ip(i)
            destination_ip.append(i)
    elif '-' in ips:
        ip = ips.split('-')
        start = is_valid_ip(ip[0])
        end = is_valid_ip(ip[1])
        for x in range(start, end+1):
            try:
                cur_ip = ipaddress.IPv4Address(x)
            except ipaddress.AddressValueError, e:
                print("invalid IP address")
                print("Exception: %s" % str(e))
                sys.exit(1)
            print(str(cur_ip))
            destination_ip.append(str(cur_ip))
    elif '/' in ips:
        try:
            network = ipaddress.IPv4Network(unicode(ips))
        except ValueError, e:
            print("illegal subnet")
            print("Exception: %s" % str(e))
            sys.exit(1)
        for ip in network:
            destination_ip.append(str(ip))
    else:
        is_valid_ip(ips)
        destination_ip.append(ips)

    if ',' in ports:
        port = ports.split(',')
        for i in port:
            destination_ports.append(is_digit(i))
    elif '-' in ports:
        port = ports.split('-')
        start = is_digit(port[0])
        end = is_digit(port[1])
        while(start <= end):
            destination_ports.append(start)
            start+=1
    else:
        destination_ports.append(is_digit(ports))

    return (destination_ip, destination_ports)

def is_digit(digit):
    if digit.isdigit():
        return int(digit)
    else:
        print("invalid port entered, aborting")
        sys.exit(1)

def is_valid_ip(ip):
    try:
        ip = int(ipaddress.IPv4Address(unicode(ip)))
        return ip
    except ipaddress.AddressValueError, e:
        print("invalid IP address")
        print("Exception: %s" % str(e))
        sys.exit(1)

def arp_scan(subnet):
    packets = arping(subnet)

def connect_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="S", dport=port), retry=2, timeout=5)
            if packet != None:
                if packet[TCP].flags == "SA":
                    print("Port: " + str(port) + " is open")
                    packet = send(IP(dst=ip)/TCP(flags="A", dport=port),retry=2, timeout=5)
                    packet = send(IP(dst=ip)/TCP(flags="RA", dport=port),retry=2, timeout=5)
            else:
                print("Port: " + str(port) + " is closed")

def syn_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="S", dport=port), retry=2, timeout=5)
            if packet != None:
                if packet[TCP].flags == "SA":
                    packet = send(IP(dst=ip)/TCP(flags="R", dport=port), retry=2, timeout=5)
                    print("Port: " + str(port) + " is open")
            else:
                print("Port: " + str(port) + " is closed")


def fin_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="F", dport=port), retry=2, timeout=5)
            if packet != None:
                if packet[TCP].flags == "R":
                    print("Port: " + str(port) + " is closed or on a Windows device")
            elif packet == None:
                print("Port: " + str(port) + " is open")

def xmas_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="FPU", dport=port), retry=2, timeout=5)
            if packet == None:
                print("Port: " + str(port) + " is open")
            elif packet[TCP].flags == "R":
                print("Port: " + str(port) + " is closed or on a Windows device")

def ack_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/TCP(flags="A", dport=port, seq=12345), retry=2, timeout=5)
            if packet == None:
                print("Port: " + str(port) + " is filtered")
            elif packet[IP].proto == 6: # 6 corresponds to TCP
                if packet[TCP].flags == "R":
                    print("Port: " + str(port) + " is unfiltered")

def udp_scan(destination_ip, destination_ports):
    for ip in destination_ip:
        for port in destination_ports:
            packet = sr1(IP(dst=ip)/UDP(dport=port), retry=2, timeout=5)
            if packet == None:
                print("Port: " + str(port) + " is open/filtered")
            elif packet[IP].proto == 1: # 1 corresponds to ICMP
                print("Port: " + str(port) + " is closed")
            elif packet[IP].proto == 'udp':
                print("Port: " + str(port) + " is open")
main()
