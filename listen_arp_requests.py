#!/usr/bin/env python

"""
https://gist.github.com/tcyrus/d32f4aba0b6ef9a961d3
https://gist.github.com/eob/d2d1eec8fad32e8bcb6e
"""

from scapy.all import ARP, sniff

import time


arp = {'10:ae:60:0e:62:47': 'bedroom'}

def arp_display(pkt):
    if pkt[ARP].op == 1: # who-has (request)
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            if pkt[ARP].hwsrc in arp:
                print 'Pushed %s (%s)' % (arp[pkt[ARP].hwsrc], pkt[ARP].hwsrc,)
            else:
                print 'ARP probe from unknown device: %s' % (pkt[ARP].hwsrc,)

while True:
    sniff(prn=arp_display, filter='arp', store=0, count=10)
    time.sleep(1)

