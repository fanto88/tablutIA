class Position:
    def __init__(self, row, column):
        self.__row = row
        self.__column = column

    def row(self):
        return self.__row

    def column(self):
        return self.__column

    def __eq__(self, other):
        if self.__row == other.row() & self.__column == other.column():
            return True
        return False


class Action:
    def __init__(self, start: Position, end: Position, role):
        self.__start = start
        self.__end = end
        self.__role = role

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def role(self):
        return self.__role

    def to_server_format(self):
        column_number_start = self.__start.row() + 1
        column_number_end = self.__end.row() + 1
        row_letter_start = chr(73 - self.__start.column())
        row_letter_end = chr(73 - self.__end.column())
        return {
            'from': str(row_letter_start) + str(column_number_start),
            'to': str(row_letter_end) + str(column_number_end)
        }
