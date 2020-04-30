import numpy


class State:
    """Class that contain the all the States bitboard and their initialization."""

    def __init__(self, color):
        self.white_bitboard = numpy.zeros(shape=9, dtype=int)
        self.king_bitboard = numpy.zeros(shape=9, dtype=int)
        self.black_bitboard = numpy.zeros(shape=9, dtype=int)
        self.escape_bitboard = numpy.empty(shape=9, dtype=int)
        self.camps_bitboard = numpy.empty(shape=9, dtype=int)
        self.throne_bitboard = numpy.empty(shape=9, dtype=int)
        self.turn = color

        # Initialize Escape Bitboard
        self.escape_bitboard[0] = 0b011000110
        self.escape_bitboard[1] = 0b100000001
        self.escape_bitboard[2] = 0b100000001
        self.escape_bitboard[3] = 0b000000000
        self.escape_bitboard[4] = 0b000000000
        self.escape_bitboard[5] = 0b000000000
        self.escape_bitboard[6] = 0b100000001
        self.escape_bitboard[7] = 0b100000001
        self.escape_bitboard[8] = 0b011000110

        # Initialize Camps Bitboard
        self.camps_bitboard[0] = 0b000111000
        self.camps_bitboard[1] = 0b000010000
        self.camps_bitboard[2] = 0b000000000
        self.camps_bitboard[3] = 0b100000001
        self.camps_bitboard[4] = 0b110000011
        self.camps_bitboard[5] = 0b100000001
        self.camps_bitboard[6] = 0b000000000
        self.camps_bitboard[7] = 0b000010000
        self.camps_bitboard[8] = 0b000111000

        # Initialize Throne Bitboard
        self.throne_bitboard[0] = 0b000000000
        self.throne_bitboard[1] = 0b000000000
        self.throne_bitboard[2] = 0b000000000
        self.throne_bitboard[3] = 0b000000000
        self.throne_bitboard[4] = 0b000010000
        self.throne_bitboard[5] = 0b000000000
        self.throne_bitboard[6] = 0b000000000
        self.throne_bitboard[7] = 0b000000000
        self.throne_bitboard[8] = 0b000000000
