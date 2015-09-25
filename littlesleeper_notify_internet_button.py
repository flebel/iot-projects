#!/usr/bin/env python

import ConfigParser

import requests

parser = argparse.ArgumentParser(description='Lights up the first N LEDs on a Photon-based Internet Button device from Particle.')
parser.add_argument('number_leds', help='first N LEDs to light up', type=int)
parser.add_argument('--config', default='default.conf', dest='config_file', help='Configuration file', type=str)

def run(number_leds, config):
    device_id = config.get('particle', 'device_id')
    headers = {
        'access_token': config.get('particle', 'access_token'),
        'params': number_leds,
    }
    requests.post('https://api.spark.io/v1/devices/%s/leds_upto' % (device_id,), headers=headers)

if __name__ == '__main__':
    args = parser.parse_args()
    config = ConfigParser.SafeConfigParser()
    config.read(args.config_file)
    run(args.number_leds, config)

