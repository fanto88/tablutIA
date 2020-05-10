class HeuristicStrategy:
    max = 1
    min = -1

    def eval(self, state, player):
        raise NotImplementedError()
