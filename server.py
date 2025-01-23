#!/usr/bin/env python3

"""
Modbus/TCP server
~~~~~~~~~~~~~~~~~

Run this as root to listen on TCP privileged ports (<= 1024).

Add "--host 0.0.0.0" to listen on all available IPv4 addresses of the host.
$ sudo ./server.py --host 0.0.0.0
"""

import argparse
import logging

from pyModbusTCP.server import ModbusServer

# init logging
logging.basicConfig()
# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', type=str, default='192.168.1.201', help='Host (default: 192.168.1.201)')
parser.add_argument('-p', '--port', type=int, default=5020, help='TCP port (default: 5020)')
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()
# logging setup
if args.debug:
    logging.getLogger('pyModbusTCP.server').setLevel(logging.DEBUG)
# start modbus server
server = ModbusServer(host=args.host, port=args.port)
print("Start modbus server..")
print("Host: " + str('192.168.1.201')+"  PortNo: "+str(5020))
server.start()
