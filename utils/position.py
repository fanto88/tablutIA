class Position:
    def __init__(self, row, column):
        self.__row = row
        self.__column = column

    def row(self):
        return self.__row

    def column(self):
        return self.__column
