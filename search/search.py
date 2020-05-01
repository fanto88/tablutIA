import numpy as np
from search.tree import Node
import time
import os


class MinMaxAgent:

    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.node_expanded = 0
        self.max_time = max_time
        self.checked = dict()
        self.node_skipped = 0
        self.timer = 0.0

    def choose_action(self, state, problem):
        self.node_expanded = 0
        self.node_skipped = 0
        self.timer = time.time()

        eval_score, selected_action = self._minimax(Node(state), problem, True, float('-inf'), float('inf'))
        print("<PID {}> nodi saltati {}".format(os.getpid(), self.node_skipped))
        return selected_action, eval_score

    def _already_checked(self, state):
        return state in self.checked

    def _already_checked_result(self, state):
        return self.checked[state]

    def _mark_checked(self, state, values):
        self.checked[state] = values    # values = (value of single state, action)
        print(os.getpid(), "stato {} elaborato".format(state))

    # TODO: si può provare a ottimizzare l'algoritmo e non restituire per ogni stato (valore, azione) ma solo valore /
        # alla fine (valore, azione) è contenuto nel dict checked
    # TODO: se fai quanto detto sopra, potresti togliere i nodi
    def _minimax(self, node, problem, max_turn, alpha, beta):

        # Controlla se lo stato corrente è già stato elaborato
        """if self._already_checked(node.state):
            print(os.getpid(),"Stato", node.state," già elaborato")
            self.node_skipped += 1
            return (float('-inf'), None) if max_turn else (float('inf'), None)
        else:
            self._mark_checked(node.state, (None, None))"""

        # Ricerca termina se:
        #   -E' uno stato terminale
        #   -Il tempo è scaduto
        #   -Non voglio più espandere l'albero
        if node.depth == self.max_depth \
                or terminal_test(node.state, problem) \
                or (time.time() - self.timer) >= self.max_time:
            values = utility(node.state, problem), node.action
            self._mark_checked(node.state, values)
            return values

        self.node_expanded += 1
        value = float('-inf') if max_turn else float('inf')
        best_action = ''

        list_actions = possible_actions(node.state, problem)
        for action in list_actions:  # TODO: vettorizza il codice
            new_state = resulting_state(node.state, action, problem)
            new_node = Node(new_state, node, action, node.path_cost+1)
            child_value, child_action = self._minimax(new_node, problem, not max_turn, alpha, beta)

            if max_turn and value < child_value:
                value = child_value
                best_action = action
                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            elif (not max_turn) and value > child_value:
                value = child_value
                best_action = action
                beta = min(beta, value)
                if beta <= alpha:
                    break

        self._mark_checked(node.state, best_action)
        return value, best_action


# Utils
def possible_actions(state, problem):   # TODO: vedi come implementare
    return problem.actions(state)


def resulting_state(state, action, problem):
    return problem.process_action(state, action)


def utility(state, problem):  # TODO: vedi come implementare
    return problem.value(state)


def terminal_test(state, problem):  #TODO: vedi come implementare
    problem.goal_test(state)
