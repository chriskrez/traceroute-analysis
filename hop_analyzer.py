from iptools import ipv4
import socket
import sys
from traceroute import Traceroute

ip = sys.argv[1] if ipv4.validate_ip(sys.argv[1]) else socket.gethostbyname(sys.argv[1])
print(ip)

traceroute = Traceroute(ip, country="LO")
hops = traceroute.traceroute()
print(hops)
