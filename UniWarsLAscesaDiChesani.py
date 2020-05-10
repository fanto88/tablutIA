import argparse
import sys

from tablut.client.tablut_client import Client
from tablut.utils import config


argv = sys.argv[1:]
argl = len(argv)
color = config.WHITE
timeout = 60
server_ip = "localhost"
server_port = config.WHITE_SERVER_PORT


# Check the color
if argl >= 1:
    color = config.WHITE if argv[0].lower() == 'white' else config.BLACK
    server_port = config.WHITE_SERVER_PORT if argv[0].lower() == 'white' else config.BLACK_SERVER_PORT

# Check timeout
if argl >= 2:
    timeout = int(argv[1])

# Check server address
if argl >= 3:
    server_complete_address = argv[2].split(':')
    server_ip = server_complete_address[0]
    server_port = int(server_complete_address[1])

# Start the client
Client(server_port, server_ip, color).run()

