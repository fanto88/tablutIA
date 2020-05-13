from tablut.search.tree import Node
import time
import os
from tablut.search.heuristic.strategies import random
import operator


class MinMaxAgent:

    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.node_expanded = 0
        self.max_time = max_time
        self.checked = dict()
        self.node_skipped = 0
        self.timer = 0.0

        # TODO: DA ELIMINARE ASSOLUTAMENTE
        self.h = random.RandomStrategy()

    def _best(self, actions_values, maximize):
        """Returns the first "action" in the given list,
        ordered by "values" Ascendant or Descendant, depending on "maximize" var."""

        actions_values.sort(key=operator.itemgetter(1), reverse=maximize)
        return actions_values[0] if actions_values else []

    def choose_action(self, state, problem, maximize=True, max_depth=None, start_depth=0):
        self.timer = time.time()
        if self.terminal_test(state, problem):
            return self.utility(state, problem)

        self.node_expanded = 0
        self.node_skipped = 0
        if max_depth:
            self.max_depth = max_depth

        # All possible actions applicable in the given state
        actions = self.possible_actions(state, problem)

        # Child states of the given one
        states = [self.resulting_state(state, action, problem) for action in actions]

        # Utility value, for each state
        first = Node(state)
        first.depth = start_depth
        eval_scores = [self._minimax(Node(st, first), problem, not maximize, float('-inf'), float('inf')) for st in states]

        # Obtaining best action
        best_action, best_value = self._best(list(zip(actions, eval_scores)), maximize)

        return best_action, best_value

    def _already_checked(self, state):
        #print("(stato, stati_computati):{}".format(state, self.checked))
        return state in self.checked

    def _already_checked_result(self, state):
        return self.checked[state]

    def _mark_checked(self, state):
        self.checked[state] = 1    # values = (value of single state, action)

    # TODO: si può provare a ottimizzare l'algoritmo e non restituire per ogni stato (valore, azione) ma solo valore
    # TODO: se fai quanto detto sopra, potresti togliere i nodi
    def _minimax(self, node, problem, maximize, alpha, beta):
        #print("(stato, profondità): ({}, {})".format(node.state, node.depth))
        # Ricerca termina se:
        #   -E' uno stato terminale
        #   -Il tempo è scaduto
        #   -Non voglio più espandere l'albero
        #print("Secondi passati:", time.time() - self.timer)
        print("(stato, depth)", node.state, node.depth)
        if node.depth >= self.max_depth \
                or self.terminal_test(node.state, problem) \
                or (time.time() - self.timer) >= self.max_time:
            values = self.utility(node.state, problem)

            self._mark_checked(node.state)
            return values

        # Controlla se lo stato corrente è già stato elaborato
        if self._already_checked(node.state):
            self.node_skipped += 1
            return float('-inf') if not maximize else float('inf')
        else:
            self._mark_checked(node.state)

        self.node_expanded += 1
        value = float('-inf') if maximize else float('inf')

        list_actions = self.possible_actions(node.state, problem)
        for action in list_actions:  # TODO: vettorizza il codice
            new_state = self.resulting_state(node.state, action, problem)
            new_node = Node(new_state, node, action, node.path_cost+1)
            child_value = self._minimax(new_node, problem, not maximize, alpha, beta)
            if maximize and value < child_value:
                value = child_value
                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            elif (not maximize) and value > child_value:
                value = child_value
                beta = min(beta, value)
                if beta <= alpha:
                    break

        return value

    # Utils
    def possible_actions(self, state, problem):
        return problem.actions(state)

    def resulting_state(self, state, action, problem):
        return problem.process_action(state, action)

    # TODO: modifica l'euristica che viene utilizzata
    def utility(self, state, problem):
        return problem.value(state, state.turn) if problem.goal_test(state) \
            else self.h.eval(state, problem.turn_player(state))

    def terminal_test(self, state, problem):
        return problem.goal_test(state)
