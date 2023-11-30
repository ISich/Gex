# -*- coding: cp1251 -*-
from tkinter import *
import pygame, math, random
from Table import Table
import Menu as My_menu


class Game():
    def __init__(self, table_size, players, bot):
        pygame.init()
        table_size = int(table_size)
        self.bot = bot
        self.players = players
        self.x_size = 500
        self.y_size = 700
        self.table_size = table_size
        self.hexagon_size = max(30 - int(max(table_size - 7, 0) * 2.5), 6)
        self.window = pygame.display.set_mode((self.x_size, self.y_size), pygame.RESIZABLE)
        self.time = 5000
        pygame.display.set_caption("Gex")

        self.table_size = table_size
        self.hexagon0_center = (self.x_size//2, self.hexagon_size + 20)
        self.table = Table(table_size)
        self.table.table = self.create_hex_field(self.table.table, self.hexagon0_center, self.hexagon_size)
        self.score = 0

        self.start_game()

    def start_game(self):
        run = True
        turn = 1
        turn_time = pygame.time.get_ticks()
        winner = "Никто не"
        user = 1
        while run:
            for event in pygame.event.get():
                res = [-1, -1]
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1:
                    x, y = event.pos
                    res = self.is_inside_hexagons(x, y, self.table.table)
                elif event.type == pygame.MOUSEBUTTONDOWN and turn == -1 and not self.bot:
                    x, y = event.pos
                    res = self.is_inside_hexagons(x, y, self.table.table)
                elif turn == -1 and self.bot:
                    res = self.bot_choose(self.table.table)
                if res != [-1, -1]:
                    if not self.table.table[res[0]][res[1]][1]:
                        self.table.table[res[0]][res[1]][1] = turn
                        self.score += 1
                        l = self.table.size
                        if turn == 1:
                            start, end = [[i, 0] for i in range(l)], [[i + l - 1, l - 1 - i] for i in range(l)]
                        else:
                            start, end = [[i + l - 1, 0] for i in range(l)], [[i, i] for i in range(l)]
                        win = self.check_win(self.table.table, turn, start, end)
                        if win:
                            winner = "1 игрок"
                            if turn == -1:
                                winner ="2 игрок"
                                if self.bot:
                                    winner = "Бот"
                            self.update_scores(turn, self.bot)
                            run = False
                        turn *= -1
                        user += 1
                        if user == self.players and self.players % 2 == 1:
                            turn = -1
                        if user > self.players:
                            user = 1
                        turn_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - turn_time > self.time:
                if turn == 1:
                    winner = "2 игрок"
                else:
                    winner = "1 игрок"
                run = False

            self.window.fill((255, 255, 255))
            self.draw_hexagon(self.window, (255 * (turn == -1), 0, 255 * (turn == 1)), (50, 50), 40)

            font1 = pygame.font.SysFont('', 30)
            text1 = font1.render(str('{0:.2f}'.format(5 - ((pygame.time.get_ticks() - turn_time)//100)/10)), True, (0, 0, 0))
            textRect1 = text1.get_rect()
            textRect1.center = (50, 50)
            self.window.blit(text1, textRect1)

            font2 = pygame.font.SysFont('_', 30)
            text2 = font2.render(str(user) + " игрок", True, (0, 0, 0))
            textRect2 = text2.get_rect()
            textRect2.center = (50, 100)
            self.window.blit(text2, textRect2)

            self.draw_hexagons(self.window, self.table.table, self.hexagon_size+20)
            pygame.display.flip()
        pygame.quit()
        self.draw_res(winner)


    def update_scores(self, turn, bot):
        scores = []
        with open("scores.txt") as f:
            record = f.readlines()
            for i in range(len(record)):
                for i0 in record[i][:-1].split():
                    scores.append(i0)
        if turn == 1 and bot:
            scores[0] = str(int(scores[0]) + 1)
        elif turn == -1 and bot:
            scores[1] = str(int(scores[1]) + 1)
        if turn == 1 and not bot:
            scores[2] = str(int(scores[2]) + 1)
        if turn == -1 and not bot:
            scores[3] = str(int(scores[3]) + 1)
        with open("scores.txt", 'w') as f:
            f.truncate()
            f.write(scores[0] + " " + scores[1] + "\n")
            f.write(scores[2] + " " + scores[3] + "\n")

    def bot_choose(self, table):
        points = []
        for i in range(len(table)):
            for q in range(len(table[i])):
                if table[i][q][1] == 0:
                    points.append([i, q])
        res = random.choice(points)
        return res

    def draw_res(self, winner):
        window = Tk()
        window.resizable(False, False)
        window.geometry("350x150")
        window.title("Gex")
        window.grab_set()

        text = winner + " победил"
        result_label = Label(window, text=text, font=("Roboto", 20, "bold"))
        result_label.pack(side=TOP, pady=10)

        player1_button = Button(window, text="Вернуться", font=("Roboto", 14), width=16,
                                command=lambda: self.go_menu(window, self.table_size))
        player1_button.pack(side=TOP, pady=10)

    def go_menu(self, window, size):
        window.destroy()
        menu = My_menu.Menu()

    def draw_hexagons(self, surface, hexagons, side):
        for line in hexagons:
            for i in line:
                cur_color = (0, 0, 0)
                if i[1] == 1:
                    cur_color = (0, 0, 255)
                elif i[1] == -1:
                    cur_color = (255, 0, 0)
                elif i[1] == 2:
                    cur_color = (0, 255, 0)
                self.draw_hexagon(surface, cur_color, i[0], self.hexagon_size)
        width = 4
        up = [hexagons[0][0][0][0], hexagons[0][0][0][1] - side]
        down = [hexagons[-1][0][0][0], hexagons[-1][0][0][1] + side]
        left = [hexagons[len(hexagons)//2][0][0][0] - side, hexagons[len(hexagons)//2][0][0][1]]
        right = [hexagons[len(hexagons) // 2][-1][0][0] + side, hexagons[len(hexagons) // 2][-1][0][1]]
        pygame.draw.line(surface, (0, 0, 255), up, left, width)
        pygame.draw.line(surface, (0, 0, 255), down, right, width)
        pygame.draw.line(surface, (255, 0, 0), up, right, width)
        pygame.draw.line(surface, (255, 0, 0), down, left, width)

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
            if (table[point[0]][point[1]][1] == user or table[point[0]][point[1]][1] == 2) \
                    and table_cur[point[0]][point[1]] == 0:
                table_cur[point[0]][point[1]] = 1
                for i in self.get_neibor(table, point[0], point[1]):
                    stack.append(i)
        return table_cur

    def get_neibor(self, table, x, y):
        res = []
        res.append([x, y - 1])
        res.append([x, y + 1])
        if x <= len(table) // 2:
            res.append([x - 1, y - 1])
            res.append([x - 1, y])
        else:
            res.append([x - 1, y])
            res.append([x - 1, y + 1])

        if x < len(table) // 2:
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
