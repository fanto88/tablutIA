import numpy as np
from search.tree import Node
from collections.abc import Iterable


# TODO: aggiungi un timer per far finire la ricerca
class MinMaxAgent:

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.node_expanded = 0

    def choose_action(self, state, problem):
        self.node_expanded = 0
        eval_score, selected_action = self._minimax(state, problem, True, float('-inf'), float('inf'))

        return selected_action

    def _minimax(self, node, problem, max_turn, alpha, beta):
        if node.depth == self.max_depth or terminal_test(node.state, problem):
            return utility(node.state, problem), node.action

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

        return value, best_action

    def _minimax2(self, node, problem, max_turn, alpha, beta):
        if node.depth == self.max_depth or terminal_test(node.state, problem):
            return utility(node.state, problem), node.action

        self.node_expanded += 1
        value = float('-inf') if max_turn else float('inf')
        best_action = ''

        list_actions = possible_actions(node.state, problem)

        return tuple(map(lambda action: self._tovectorize_minimax(action, value, best_action, node, problem, max_turn, alpha, beta), list_actions))

    def _tovectorize_minimax(self, action, value, best_action, node, problem, max_turn, alpha, beta):
        new_state = resulting_state(node.state, action, problem)
        new_node = Node(new_state, node, action, node.path_cost + 1)
        child_value, child_action = self._minimax2(new_node, problem, not max_turn, alpha, beta)
        #child_value = max(child_value) if isinstance(child_value, Iterable) else child_value  # TODO: Vedi assolutamente come fare
        print(node, child_value, child_action)
        if max_turn and value < child_value:
            value = child_value
            best_action = action
            local_alpha = max(alpha, value)
            if beta <= local_alpha:
                return (float('-inf'), None) if max_turn else (float('inf'), None)

        elif (not max_turn) and value > child_value:
            value = child_value
            best_action = action
            local_beta = min(beta, value)
            if local_beta <= alpha:
                return (float('-inf'), None) if max_turn else (float('inf'), None)
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