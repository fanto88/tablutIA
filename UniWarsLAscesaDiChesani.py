import argparse

from tablut.client.tablut_client import Client
from tablut.utils import config

parser = argparse.ArgumentParser(description='Default Behaviour: Color = White | Timeout = 60s | Server = localhost |\
                                                Port = 5800')
parser.add_argument("-c", "--color", choices=['white', 'black'], type=str.lower, default='white',
                    help="Set the player color. Valid option: white/black")
parser.add_argument("-t", "--timeout", type=int, default=60, help="Change the timeout time")
parser.add_argument("-s", "--server", default='localhost', help="Change the host address. Format X.X.X.X")
parser.add_argument("-p", "--port", type=int, help="Change the server port.")

args = parser.parse_args()
color = config.WHITE if args.color.lower() == 'white' else config.BLACK
timeout = args.timeout
server_ip = args.server

if args.port is None:
    server_port = config.WHITE_SERVER_PORT if color == config.WHITE else config.BLACK_SERVER_PORT
else:
    server_port = args.port

Client(server_port, server_ip, color, timeout).run()
