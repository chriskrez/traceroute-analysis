#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from traceroute import Traceroute


ip=socket.gethostbyname()
print(ip)
traceroute = Traceroute(,country="LO")
hops=traceroute.traceroute()
print(hops)