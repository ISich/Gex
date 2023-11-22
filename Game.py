# -*- coding: cp1251 -*-
from tkinter import *
import pygame, math
from Table import Table


class Game():
    def __init__(self, table_size: int):
        pygame.init()
        self.size = 500
        self.window = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Gex")

        self.table_size = table_size
        self.hexagon_size = 30
        self.hexagon0_center = (self.size//2, self.hexagon_size + 20)
        self.table = Table(table_size)
        self.table.table = self.create_hex_field(self.table.table, self.hexagon0_center, self.hexagon_size)

        self.start_game()

    def start_game(self):
        run = True
        turn = 1
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    res = self.is_inside_hexagons(x, y, self.table.table)
                    if res != [-1, -1]:
                        if not self.table.table[res[0]][res[1]][1]:
                            self.table.table[res[0]][res[1]][1] = turn
                            l = self.table.size
                            win = self.check_win(self.table.table, turn,
                                                 [[i, 0] for i in range(l)],
                                                 [[i + l - 1, l - 1 - i] for i in range(l)])
                            if win:
                                print("Win", turn)
                                run = False
                            turn *= -1
                            print(res)

            self.window.fill((255, 255, 255))
            self.draw_hexagons(self.window, self.table.table)
            pygame.display.flip()
        #pygame.quit()

    def draw_hexagons(self, surface, hexagons):
        for line in hexagons:
            for i in line:
                cur_color = (0, 0, 0)
                if i[1] == 1:
                    cur_color = (0, 0, 255)
                elif i[1] == -1:
                    cur_color = (255, 0, 0)
                self.draw_hexagon(surface, cur_color, i[0], self.hexagon_size)

    def draw_hexagon(self, surface, color, center, size):
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            x = center[0] + size * math.cos(angle_rad)
            y = center[1] + size * math.sin(angle_rad)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)


    def is_inside_hexagons(self, x, y, hexagons):
        for i in range(len(hexagons)):
            for q in range(len(hexagons[i])):
                hexagon = hexagons[i][q]
                if self.is_point_inside_hexagon(x, y, hexagon[0], self.hexagon_size):
                    return [i, q]
        return [-1, -1]

    def is_point_inside_hexagon(self, x, y, center, size):
        # Эта функция проверяет, находится ли точка (x, y) внутри шестиугольника.
        # Для упрощения, предполагаем, что шестиугольник регулярный.
        # В реальном приложении логика может быть более сложной.
        dx = x - center[0]
        dy = y - center[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < size

    def create_hex_field(self, table, hexagon0_center, hexagon_size):
        for i in range(len(table)):
            ind = 1 - len(table[i])
            for q in range(len(table[i])):
                table[i][q][0] = (hexagon0_center[0] + ind * hexagon_size * (math.sqrt(3) + 0.2)//2,
                                  hexagon0_center[1] + i * hexagon_size * (math.sqrt(3) + 1.6)//2)
                ind += 2
        return table


    def check_win(self, table, user, start_points, end_points):
        table_cur = [[0 for q in line] for line in table]
        for point in start_points:
            table_cur = self.dfs(table_cur, table, point, user)
        res = False
        for point in end_points:
            res = res or table_cur[point[0]][point[1]] == 1
        return res


    def dfs(self, table_cur, table, start, user):
        stack = [start]
        while len(stack) != 0:
            point = stack[-1]
            del stack[-1]
            if table[point[0]][point[1]][1] == user and table_cur[point[0]][point[1]] == 0:
                table_cur[point[0]][point[1]] = 1
                for i in self.get_neibor(table, point[0], point[1]):
                    stack.append(i)
        return table_cur

    def get_neibor(self, table, x, y):
        res = []
        res.append([x, y - 1])
        res.append([x, y + 1])
        if y <= len(table) // 2:
            res.append([x - 1, y - 1])
            res.append([x - 1, y])
        else:
            res.append([x - 1, y])
            res.append([x - 1, y + 1])

        if y < len(table) // 2:
            res.append([x + 1, y])
            res.append([x + 1, y + 1])
        else:
            res.append([x + 1, y - 1])
            res.append([x + 1, y])
        res1 = []
        for i in res:
            if 0 <= i[0] <= len(table) - 1:
                if 0 <= i[1] <= len(table[i[0]]) - 1:
                    res1.append(i)
        return res1
