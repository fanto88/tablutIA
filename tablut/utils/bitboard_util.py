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


def count_piece(bitboard):
    """Count the pawn inside a bitboard."""
    count = 0
    for row in range(9):
        for column in range(9):
            if get_bit(bitboard, row, column) == 1:
                count += 1
    return count


def count_adjacent(position, obstacle_bitboard):
    """Count the obstacle with around the position. Obstacle_bitboard are the pawn that you have to
    consider as obstacle."""
    count = 0
    if get_bit(obstacle_bitboard, position.row - 1, position.column) == 1:
        count += 1
    if get_bit(obstacle_bitboard, position.row + 1, position.column) == 1:
        count += 1
    if get_bit(obstacle_bitboard, position.row, position.column - 1) == 1:
        count += 1
    if get_bit(obstacle_bitboard, position.row, position.column + 1) == 1:
        count += 1
    return count


def eat(bitboard, obstacle_bitboard, position):
    """Check if you can eat a normal Pawn and return the bitboard without the pawn ate."""
    result = False
    if position.row - 2 >= 0:
        if get_bit(obstacle_bitboard, position.row - 2, position.column) == 1:
            if get_bit(bitboard, position.row - 1, position.column) == 1:
                bitboard = unset(bitboard, position.row - 1, position.column)
                result = True
    if position.column - 2 >= 0:
        if get_bit(obstacle_bitboard, position.row, position.column - 2) == 1:
            if get_bit(bitboard, position.row, position.column - 1) == 1:
                bitboard = unset(bitboard, position.row, position.column - 1)
                result = True
    if position.row + 2 <= 8:
        if get_bit(obstacle_bitboard, position.row + 2, position.column) == 1:
            if get_bit(bitboard, position.row + 1, position.column) == 1:
                bitboard = unset(bitboard, position.row + 1, position.column)
                result = True
    if position.column + 2 <= 8:
        if get_bit(obstacle_bitboard, position.row, position.column + 2) == 1:
            if get_bit(bitboard, position.row, position.column + 1) == 1:
                bitboard = unset(bitboard, position.row, position.column + 1)
                result = True
    return bitboard, result
