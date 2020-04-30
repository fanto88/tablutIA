# TODO: Migliorare il print_bitboard dentro bitboard_util.py


def get_bit(bitboard, row, column):
    bits = bitboard[row]
    """Get the value of the index-th bit of the sequence."""
    return bits >> column & 1


def print_bitboard(bitboard):
    """Print the bitboard."""
    for value in bitboard:
        print(format(value, '09b'))


def unset(bitboard, row, column):
    """Set the bit of the sequence, corresponding to the index value, to the value 0."""
    bitboard[row] &= ~(1 << column)
    return bitboard


def set(bitboard, row, column):
    """Set the bit of the sequence, corresponding to the index value, to the value 1."""
    bitboard[row] = bitboard[row] | (1 << column)
    return bitboard
