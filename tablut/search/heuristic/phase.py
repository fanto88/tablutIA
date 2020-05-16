START = 3
MIDDLE = 7
LATE = 10


def get_phase(turn):
    return START if turn <= START else (MIDDLE if turn <= MIDDLE else LATE)
