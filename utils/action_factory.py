from utils import config, bitboard_util
from utils.action import Position, Action


def get_available_actions_for_pawn(position, obstacle_bitboard, color):
    row_index = position.row()
    column_index = position.column()
    all_available_moves_for_pawn = []
    for row in range(row_index - 1, -1, -1):
        if bitboard_util.get_bit(obstacle_bitboard, row, column_index) != 1:
            action = Action(Position(row_index, column_index), Position(row, column_index), color)
            all_available_moves_for_pawn.append(action)
        else:
            break
    for col in range(column_index - 1, -1, -1):
        if bitboard_util.get_bit(obstacle_bitboard, row_index, col) != 1:
            action = Action(Position(row_index, column_index), Position(row_index, col), color)
            all_available_moves_for_pawn.append(action)
        else:
            break
    for row in range(row_index + 1, 9):
        if bitboard_util.get_bit(obstacle_bitboard, row, column_index) != 1:
            action = Action(Position(row_index, column_index), Position(row, column_index), color)
            all_available_moves_for_pawn.append(action)
        else:
            break
    for col in range(column_index + 1, 9):
        if bitboard_util.get_bit(obstacle_bitboard, row_index, col) != 1:
            action = Action(Position(row_index, column_index), Position(row_index, col), color)
            all_available_moves_for_pawn.append(action)
        else:
            break
    return all_available_moves_for_pawn


def all_available_actions(state):
    actions = []
    if state.turn == config.WHITE:
        obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
        for row_index in range(0, 9):
            for column_index in range(0, 9):
                if bitboard_util.get_bit((state.white_bitboard | state.king_bitboard), row_index,
                                         column_index) == 1:
                    actions += get_available_actions_for_pawn(Position(row_index, column_index),
                                                              obstacle_bitboard, config.WHITE)
    else:
        obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard
        for row_index in range(0, 9):
            for column_index in range(0, 9):
                if bitboard_util.get_bit(state.black_bitboard, row_index, column_index):
                    new_obstacle_bitboard = obstacle_bitboard.copy()
                    if (row_index == 8 or row_index == 0) & (column_index == 3 or column_index == 5):
                        row = 8 - row_index
                        new_obstacle_bitboard = bitboard_util.set(new_obstacle_bitboard, row, column_index)

                    elif (row_index == 3 or row_index == 5) & (column_index == 3 or column_index == 8):
                        column = 8 - column_index
                        new_obstacle_bitboard = bitboard_util.set(new_obstacle_bitboard, row_index, column)

                    else:
                        new_obstacle_bitboard |= state.camps_bitboard
                    actions += get_available_actions_for_pawn(Position(row_index, column_index),
                                                              new_obstacle_bitboard, config.BLACK)

    return actions
