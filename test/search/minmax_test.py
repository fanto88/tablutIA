from tablut.search import parallel_search as s


class Problem:
    def actions(self, state):   # TODO: implement
        return [x for x in range(1, 3)]

    def goal_test(self, state):  # TODO: implement
        return False

    def value(self, state, lol):  # TODO: implement
        return state

    def process_action(self, state, action):
        return state - action

    def turn_player(self, state):
        return 0


if __name__ == '__main__':
    search = s.ParallelMinMax(2, 2, 20)
    action = search.make_decision(8, Problem())
    nodes_expanded = search.node_expanded
    print(action, search.max_depth)
    #print(nodes_expanded)
