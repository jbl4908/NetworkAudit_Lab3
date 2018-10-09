You will need to install the following libraries for this script to work
	1. pip install scapy
	2. pip install ipaddress

If you want the connect scan to work correctly you must enter the following IP
table rule to make sure the host does not automatically send an RST when the
client responds.

iptables -t raw -A PREROUTING -p tcp --dport <source port I use for scapy traffic> -j DROP
