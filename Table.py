import random


class Table():
    def __init__(self, size: int):
        '''
        Make table of hexagons where (x, y, player)
        '''
        self.size = size
        self.table = self.__create_table(size, random.randint(0, size))

    def __create_table(self, size: int, own_fields: int):
        table = []
        for i in range(1, size * 2):
            table.append([[(0, 0), 0] for i in range(min(i, size * 2 - i))])
        while own_fields != 0:
            x = random.randint(0, len(table) - 1)
            y = random.randint(0, len(table[x]) - 1)
            if table[x][y][1] == 0:
                table[x][y][1] = 2
                own_fields -= 1
        return table