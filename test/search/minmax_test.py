from tablut.search import parallel_search as s
from tablut.search import search as single_process
import tablut.search.parallel_search2 as s2


class Problem:
    def actions(self, state):   # TODO: implement
        return [x for x in range(1, 20)]

    def goal_test(self, state):  # TODO: implement
        return False

    def value(self, state, lol):  # TODO: implement
        return state

    def process_action(self, state, action):
        return state - action

    def turn_player(self, state):
        return 0


if __name__ == '__main__':
    """search = single_process.SearchAgent(3, 20)
    action = search.choose_action(8, Problem())
    nodes_expanded = search.node_expanded"""
    print(s2.choose_action(state=8, process_no=4, problem=Problem(), max_depth=3, max_time=60))
    #print(nodes_expanded)
