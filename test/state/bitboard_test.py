import time

import numpy

from tablut.state.tablut_state import TablutState
from tablut.utils import config, bitboard_util
from tablut.utils.action import Position


def main():
    state = TablutState(config.WHITE)

    adjacent_throne_bitboard = numpy.empty(shape=9, dtype=int)

    adjacent_throne_bitboard[0] = 0b000000000
    adjacent_throne_bitboard[1] = 0b000000000
    adjacent_throne_bitboard[2] = 0b000000000
    adjacent_throne_bitboard[3] = 0b000010000
    adjacent_throne_bitboard[4] = 0b000101000
    adjacent_throne_bitboard[5] = 0b000010000
    adjacent_throne_bitboard[6] = 0b000000000
    adjacent_throne_bitboard[7] = 0b000000000
    adjacent_throne_bitboard[8] = 0b000000000

    state.king_bitboard[0] = 0b000000000
    state.king_bitboard[1] = 0b000000000
    state.king_bitboard[2] = 0b000000000
    state.king_bitboard[3] = 0b000000000
    state.king_bitboard[4] = 0b000010000
    state.king_bitboard[5] = 0b000000000
    state.king_bitboard[6] = 0b000000000
    state.king_bitboard[7] = 0b000000000
    state.king_bitboard[8] = 0b000000000

    start_time = time.time()
    result = numpy.any(state.king_bitboard | state.throne_bitboard)
    end_time = time.time() - start_time

    result = False
    start_time = time.time()
    if state.king_position == Position(4, 4):
        result = True
    end_time_2 = time.time() - start_time

    start_time = time.time()
    result = bitboard_util.get_bit(state.king_bitboard & state.throne_bitboard, 4 , 4)
    end_time_3 = time.time() - start_time

    print(end_time)
    print(end_time_2)
    print(end_time_3)

    print(end_time_2 < end_time_3)


if __name__ == '__main__':
    main()