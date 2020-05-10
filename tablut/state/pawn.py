import enum


class Pawn(enum.Enum):
    Empty = 0b000
    White = 0b001
    Black = 0b010
    Castle = 0b011
    Camps = 0b100
    Escapes = 0b101
    King = 0b110
