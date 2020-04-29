import time

import numpy

import utils.config as config
from client.algorithm import Algorithm
from network.connection_handler import ConnectionHandler
from state.tablut_state import TablutState
from utils import bitboard_util


class Client(ConnectionHandler):
    """Class that define the client logic.
    Extend ConnectionHandler that handles the connection between client and server."""

    def __init__(self, port, host, role):
        super().__init__(port, host)
        self.__player_name = config.PLAYER_NAME
        self.__role = role
        self.__state = TablutState()
        self.__algorithm = Algorithm(self.__role)

    def player_name(self, player_name=None):
        """If called with no parameters return the player_name.
            Else assign a new player_name to the class."""
        if player_name is None:
            return self.__player_name
        self.__player_name = player_name
        return self

    def role(self, role=None):
        """If called with no parameters return the role.
            Else assign a new role to the class."""
        if role is None:
            return self.__role
        self.__role = role

    def run(self):
        """Implements the logic of the client."""
        try:
            self.connect()  # Connecting to the server
            self.send_string(self.__player_name)  # Sending the name
            self.__state.load_state_from_json(self.read_string())  # Read the initial state
            while True:  # Game loop
                all_moves = self.__state.all_available_moves(self.__state, self.__state.turn())
                for action in all_moves:
                    print(action.to_server_format())
                print("Mosse giocatore: ", self.__state.turn())
                print("------------------------------------------------------------------")
                time.sleep(1)
                if self.__role == self.__state.turn():  # check if our turn or not
                    move = self.__algorithm.get_move(self.__state)  # Algorithm return a move
                    if move is not None:
                        self.__state.move(move)  # Execute the move
                        self.send_string(move.to_server_format())  # send the move to the server
                self.__state.load_state_from_json(self.read_string())  # read the new state
        except:
            pass
        finally:
            print("Game Terminated - Closing Connection")
            self.disconnect()
