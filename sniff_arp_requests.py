#!/usr/bin/env python

"""
https://gist.github.com/eob/a8b5632f23e75b311df2
"""

from scapy.all import *


def arp_display(pkt):
    if pkt[ARP].op == 1: # who-has (request)
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            print 'ARP Probe from: ' + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter='arp', store=0, count=10)

