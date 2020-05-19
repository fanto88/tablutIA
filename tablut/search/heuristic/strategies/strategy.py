class HeuristicStrategy:
    """Basic interface for a Strategy."""

    def __init__(self):
        pass

    max = 1
    min = -1

    def eval(self, state, player):
        raise NotImplementedError()
