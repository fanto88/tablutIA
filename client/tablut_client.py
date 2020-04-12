from utils.connection_handler import ConnectionHandler
import utils.config as config


class Client(ConnectionHandler):
    def __init__(self, port, host, role):
        super().__init__(port, host)
        self.__player_name = config.PLAYER_NAME
        self.__role = role

    def player_name(self, player_name=None):
        if player_name is None:
            return self.__player_name
        self.__player_name = player_name
        return self

    def role(self, role=None):
        if role is None:
            return self.__role
        self.__role = role

    def run(self):
        self.connect()  # Connecting to the server
        self.send_string(self.__player_name)  # Sending the name

        initial_state = self.read_string()  # Reading the initial state of the game
        print(initial_state["board"])
        print("\n", initial_state["turn"])

        # TODO : fare la gestione delle mosse

        return self
