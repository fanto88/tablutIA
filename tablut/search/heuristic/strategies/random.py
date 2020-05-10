import secrets
from tablut.search.heuristic.strategies.strategy import HeuristicStrategy


class RandomStrategy(HeuristicStrategy):
    min = 0
    max = 10

    def eval(self, state, player):
        return secrets.randbelow(self.max+1)
