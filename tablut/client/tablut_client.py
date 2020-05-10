import tablut.utils.config as config
from tablut.client.connection_handler import ConnectionHandler
from tablut.search import parallel_search as parallel_search
from tablut.search.game import TablutProblem
from tablut.state.tablut_state import TablutState


class Client(ConnectionHandler):
    """Class that define the client logic.
    Extend ConnectionHandler that handles the connection between client and server."""

    def __init__(self, port, host, role, timeout):
        super().__init__(port, host)
        self.__player_name = config.PLAYER_NAME
        self.__role = role
        self.__timeout = timeout
        self.__state = TablutState(self.__role)

    def run(self):
        """Implements the logic of the client."""
        try:
            self.connect()  # Connecting to the server
            self.send_string(self.__player_name)  # Sending the name
            self.__state.load_state_from_json(self.read_string())  # Read the initial state
            while True:  # Game loop
                if self.__role == self.__state.turn:  # check if our turn or not
                    search = parallel_search.ParallelMinMax(2, 3, self.__timeout)
                    action = search.make_decision(self.__state, TablutProblem())
                    if action is not None:
                        self.__state.move(action)  # Execute the move
                        self.send_string(action.to_server_format())  # send the move to the server
                self.__state.load_state_from_json(self.read_string())  # read the new state
        except ConnectionResetError:
            pass
        finally:
            print("Game Terminated - Closing Connection")
