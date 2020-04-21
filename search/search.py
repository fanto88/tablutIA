import numpy as np


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def expand(self, problem):  # TODO: restituisco array numpy anziché lista?
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.process_action(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


class MinMaxAgent:

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.node_expanded = 0

    def choose_action(self, state, problem):
        self.node_expanded = 0
        eval_score, selected_action = self._max_value(state, problem, 0, float('-inf'), float('inf'))

        return selected_action

    def _max_value(self, state, problem, depth, alpha, beta):
        if depth == self.max_depth or terminal_test(state, problem):
            return utility(state, problem)

        self.node_expanded += 1
        value = float('-inf')
        best_action = ''

        list_actions = possible_actions(state, problem)
        for action in list_actions:  # TODO: vettorizza il codice
            new_state = resulting_state(state, action, problem)
            min_value, min_action = self._min_value(new_state, problem, depth+1, alpha, beta)
            value = max(value, min_value)
            if value >= alpha:
                best_action = min_action
                return value, action
            alpha = max(alpha, value)

        return value, best_action

    def _min_value(self, state, problem, depth, alpha, beta):
        if depth == self.max_depth or terminal_test(state, problem):
            return utility(state, problem)

        self.node_expanded += 1
        value = float('inf')
        best_action = ''

        list_actions = possible_actions(state, problem)
        for action in list_actions:  # TODO: vettorizza il codice
            new_state = resulting_state(state, action, problem)
            max_value, max_action = self._max_value(new_state, problem, depth + 1, alpha, beta)
            value = min(value, max_value)
            if value <= beta:
                best_action = max_action
                return value, action
            beta = min(beta, value)

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


class Problem:

    def actions(self, state):
        return list(range(1, 4))

    def value(self, state):
        return state

    def process_action(self, state, action):
        return state - action

    def goal_test(self, state):
        return False


if __name__ == '__main__':
    print(MinMaxAgent(2).choose_action(8, Problem()))
