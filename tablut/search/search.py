import time
import operator
from tablut.search.heuristic.strategies import random
from tablut.search.tree import Node
from tablut.search.game import Game
import tablut.search.heuristic as heuristic


class SearchAgent:

    def __init__(self, max_depth, max_time, checked_nodes=None):
        self.max_depth = max_depth
        self.max_time = max_time
        self.node_expanded = 0
        self.node_skipped = 0
        self.checked = dict()
        self.timer = 0.0
        self.phase = heuristic.phase.START

        if checked_nodes:
            self.checked = checked_nodes

        # TODO: DA ELIMINARE ASSOLUTAMENTE
        self.h = random.RandomStrategy()

    def _best(self, actions_values, maximize):
        """Returns the first "action" in the given list,
        ordered by "values" Ascendant or Descendant, depending on "maximize" var."""
        if not actions_values:
            return (None, float('inf')) if maximize else (None, float('-inf'))

        actions_values.sort(key=operator.itemgetter(1), reverse=maximize)

        if actions_values[0][1] in (float('inf'), float('-inf')):
            return (None, float('inf')) if maximize else (None, float('-inf'))

        return actions_values[0]

    def choose_action(self, state, problem: Game, maximize=True, max_depth=None, max_time=None,
                      start_depth=0, given_player=None, given_phase=None):
        self.timer = time.time()

        self.node_expanded = 0
        self.node_skipped = 0
        if max_depth:
            self.max_depth = max_depth

        if max_time:
            self.max_time = max_time

        if given_phase:
            self.phase = given_phase

        # All possible actions applicable in the given state
        actions = self.possible_actions(state, problem)

        # Child states of the given one
        states = [self.resulting_state(state, action, problem) for action in actions]

        # Turn player
        player = problem.turn_player(state)
        if given_player:
            player = given_player

        if self.terminal_test(state, problem) or start_depth >= self.max_depth:
            return "None", self.utility(state, problem, player, start_depth)

        # Utility value, for each state
        first = Node(state)
        first.depth = start_depth
        eval_scores = [self._minimax(Node(st, first), problem, not maximize, player, float('-inf'), float('inf')) for st in states]

        # Obtaining best action
        bestaction_bestvalue = self._best(list(filter(lambda x: x[1] not in (float('inf'), float('-inf')),
                                                                             zip(actions, eval_scores))), maximize)
        return bestaction_bestvalue

    def _already_checked(self, state):
        #print("(stato, stati_computati):{}".format(state, self.checked))
        return state in self.checked

    def _already_checked_result(self, state):
        return self.checked[state]

    def _mark_checked(self, state):
        self.checked[state] = 1    # values = (value of single state, action)

    # TODO: si può provare a ottimizzare l'algoritmo e non restituire per ogni stato (valore, azione) ma solo valore
    # TODO: se fai quanto detto sopra, potresti togliere i nodi
    # TODO: se trovi mossa vincente, esci subito
    def _minimax(self, node: Node, problem: Game, maximize, player, alpha, beta):
        # Ricerca termina se:
        #   -E' uno stato terminale
        #   -Il tempo è scaduto
        #   -Non voglio più espandere l'albero

        if node.depth >= self.max_depth \
                or self.terminal_test(node.state, problem) \
                or (time.time() - self.timer) >= self.max_time:
            values = self.utility(node.state, problem, player, node.depth)

            self._mark_checked(node.state)
            return values

        # TODO: sposta il controllo sopra alle condizioni
        # Controlla se lo stato corrente è già stato elaborato
        if self._already_checked(node.state):
            self.node_skipped += 1
            return float('-inf') if not maximize else float('inf')
        else:
            self._mark_checked(node.state)

        self.node_expanded += 1
        value = float('-inf') if maximize else float('inf')

        list_actions = self.possible_actions(node.state, problem)
        for action in list_actions:
            new_state = self.resulting_state(node.state, action, problem)
            new_node = Node(new_state, node, action, node.path_cost+1)
            child_value = self._minimax(new_node, problem, not maximize, player, alpha, beta)

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

            # Time control
            if (time.time() - self.timer) >= self.max_time:
                break

        return value

    # Utils
    def possible_actions(self, state, problem):
        return problem.actions(state)

    def resulting_state(self, state, action, problem):
        return problem.process_action(state, action)

    # TODO: modifica l'euristica che viene utilizzata
    # TODO: elimina par. depth
    def utility(self, state, problem, player, depth):
        phase = self.phase

        return problem.value(state, player) if problem.goal_test(state) \
            else heuristic.eval(state, player, phase)
            # else self.h.eval(state, player)

    def terminal_test(self, state, problem):
        return problem.goal_test(state)


def utility(state, problem):
    return problem.value(state, state.turn) if problem.goal_test(state) \
        else random.RandomStrategy().eval(state, problem.turn_player(state))
