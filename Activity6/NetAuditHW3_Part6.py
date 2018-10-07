#!/usr/bin/python

from scapy.all import *

#packets = sr(ARP(op="who-has", psrc="1.1.1.1"))

#packets = arping("10.0.0.*")
#packets2 = arping("192.168.1.*")

def tcp_scan(destination_ip, destination_ports):
    for port in destination_ports:
        packet = sr1(IP(dst=destination_ip)/TCP(flags="S", dport=port))
        if packet[TCP].flags == "SA":
            packet = send(IP(dst=destination_ip)/TCP(flags="A", dport=port))
            packet = send(IP(dst=destination_ip)/TCP(flags="RA", dport=port))
tcp_scan("10.0.0.25", [912])
#packet = TCP(raw(packet))
#print(packet[TCP].flags)
#hexdump(packet)
#print(packets.summary())
