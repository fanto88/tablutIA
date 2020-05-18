class Position:
    """Class that rappresent a Position on the board, formed by row and column."""

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        if self.row == other.row and self.column == other.column:
            return True
        return False

    def __repr__(self):
        return "RIGA:{:d} COLONNA:{:d}".format(self.row, self.column)


class Action:
    """Class that represent an Action on the board."""

    def __init__(self, start: Position, end: Position, role):
        self.start = start
        self.end = end
        self.role = role

    def to_server_format(self):
        """Return the action in the format required by the server."""
        column_number_start = self.start.row + 1
        column_number_end = self.end.row + 1
        row_letter_start = chr(73 - self.start.column)
        row_letter_end = chr(73 - self.end.column)
        return {
            'from': str(row_letter_start) + str(column_number_start),
            'to': str(row_letter_end) + str(column_number_end)
        }

    def __repr__(self):
        column_number_start = self.start.row + 1
        column_number_end = self.end.row + 1
        row_letter_start = chr(73 - self.start.column)
        row_letter_end = chr(73 - self.end.column)
        return "Action: {:s}-{:s}".format(str(row_letter_start) + str(column_number_start),
                                          str(row_letter_end) + str(column_number_end))
