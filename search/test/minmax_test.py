from search import search as s
import time

class Problem:
    def actions(self, state):   # TODO: implement
        return [x for x in range(1, 3)]

    def goal_test(self, state):  # TODO: implement
        return False

    def value(self, state):  # TODO: implement
        return state

    def process_action(self, state, action):
        return state - action


if __name__ == '__main__':
    search = s.ParallelMinMax(2, 3, 20)
    action = search.choose_action(8, Problem())
    nodes_expanded = search.node_expanded
    print(action)
    print(nodes_expanded)
