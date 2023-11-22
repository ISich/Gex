class Table():
    def __init__(self, size: int):
        '''
        Make table of hexagons where (x, y, player)
        '''
        self.size = size
        self.table = self.__create_table(size)

    def __create_table(self, size: int):
        table = []
        for i in range(1, size * 2):
            table.append([[(0, 0), 0] for i in range(min(i, size * 2 - i))])
        return table