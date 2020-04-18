from client.tablut_client import Client
import utils.config as config


def main():
    Client(config.WHITE_SERVER_PORT, config.SERVER_IP, config.WHITE).run()


if __name__ == "__main__":
    main()
