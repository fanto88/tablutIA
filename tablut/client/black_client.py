from tablut.client.tablut_client import Client
import tablut.utils.config as config


def main():
    Client(config.BLACK_SERVER_PORT, config.SERVER_IP, config.BLACK).run()


if __name__ == "__main__":
    main()
