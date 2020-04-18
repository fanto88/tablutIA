class Bitboard:
    @staticmethod
    def set(bits, index):
        """Set the bit of the sequence, corresponding to the index value, to the value 1."""
        return bits | (1 << index)

    @staticmethod
    def unset(bits, index):
        """Set the bit of the sequence, corresponding to the index value, to the value 0."""
        return bits & ~(1 << index)

    @staticmethod
    def print_bitboard(bitboard):
        """Print the bitboard."""
        for value in bitboard:
            print(format(value, '09b'))

    @staticmethod
    def get_bit(bits, index):
        """Get the value of the index-th bit of the sequence."""
        return bits >> index & 1
