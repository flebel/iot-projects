#!/usr/bin/env python

"""
https://gist.github.com/tcyrus/d32f4aba0b6ef9a961d3
https://gist.github.com/eob/d2d1eec8fad32e8bcb6e
"""

from scapy.all import ARP, sniff

import argparse
import subprocess
import time


parser = argparse.ArgumentParser('Runs executable when an ARP probe is performed by a given MAC.')
parser.add_argument('mac', type=str, help='MAC address performing the ARP probe')
parser.add_argument('executable', type=str, help='path to executable program to run when ARP probe is detected')


class ARPListener(object):
    def __init__(self, mac, callback=None, executable=None):
        assert mac, 'MAC address is required.'
        assert not all((callback, executable,)), 'One of callback or path to executable program is required.'
        self.callback = callback
        self.executable = executable
        self.mac = mac.lower()

    def _arp_callback(self, packet):
        pkt = packet[ARP]
        if pkt.op == 1 and pkt.psrc == '0.0.0.0' and pkt.hwsrc == self.mac:
            self._run()

    def _run(self):
        if self.callback:
            self.callback()
        elif self.executable:
            executable_atoms = filter(None, self.executable.split(' '))
            subprocess.Popen(['nohup'] + executable_atoms)

    def listen(self, pause_duration=1):
        arp_callback = lambda pkt: self._arp_callback(pkt)
        while True:
            sniff(prn=arp_callback, filter='arp', store=0, count=10)
            time.sleep(pause_duration)


if __name__ == '__main__':
    args = parser.parse_args()
    listener = ARPListener(args.mac, executable=args.executable)
    listener.listen()

