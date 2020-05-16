import functools as ft


class HeuristicFunction:

    def __init__(self, strategies):
        self.strategies = strategies

    def _eval_strategies(self, state, player):
        # Multiplying every value for its weight and summing to the accumulated value
        value = ft.reduce(lambda acc, n: acc + next[0].eval(state, player)*n[1], self.strategies, initial=0)

        return value

    def eval(self, state, player):
        return self._eval_strategies(state, player)
