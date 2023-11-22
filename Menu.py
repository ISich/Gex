# -*- coding: cp1251 -*-
from tkinter import *
from Game import Game


class Menu():
    def __init__(self, size):
        self.size = size
        self.window = Tk()
        self.start_menu(self.window)
        self.mainloop(self.window)

    def start_menu(self, window):
        window.resizable(False, False)
        window.geometry("350x250")
        window.title("Gex")
        window.grab_set()

        text = "GEX"
        label = Label(window, text=text, font=("Roboto", 20, "bold"))
        label.pack(side=TOP, pady=10)

        player1_button = Button(window, text="1 игрок", font=("Roboto", 14), width=16,
                               command=lambda: self.start_game(window, self.size))
        player1_button.pack(side=TOP, pady=10)

        player2_button = Button(window, text="2 игрока", font=("Roboto", 14), width=16,
                                command=lambda: self.close_window(window))
        player2_button.pack(side=TOP, pady=10)

        result_button = Button(window, text="Таблица рекордов", font=("Roboto", 14), width=16,
                               command=lambda: self.__show_result())
        result_button.pack(side=TOP, pady=10)

    def start_game(self, window, size):
        self.close_window(window)
        game = Game(size)

    def __show_result(self):
        scores = []
        with open("scores.txt") as f:
            record = f.readlines()
            for i in range(len(record)):
                scores.append(record[i][:-1])

        record_table = Toplevel(self.window)
        record_table.resizable(False, False)
        record_table.geometry("300x200")
        record_table.grab_set()

        main_label = Label(record_table, text="Таблица рекордов", font=("Roboto", 20, "bold"))
        first_lvl_label = Label(record_table, text="Уровень 1", font=("Roboto", 14))
        second_lvl_label = Label(record_table, text="Уровень 2", font=("Roboto", 14))
        third_lvl_label = Label(record_table, text="Уровень 3", font=("Roboto", 14))
        first_lvl_record = Label(record_table, text=f"{scores[0]}", font=("Roboto", 14))
        second_lvl_record = Label(record_table, text=f"{scores[1]}", font=("Roboto", 14))
        third_lvl_record = Label(record_table, text=f"{scores[2]}", font=("Roboto", 14))

        main_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20)
        first_lvl_label.grid(row=1, column=0, padx=5, pady=5)
        second_lvl_label.grid(row=2, column=0, padx=5, pady=5)
        third_lvl_label.grid(row=3, column=0, padx=5, pady=5)
        first_lvl_record.grid(row=1, column=1, padx=5, pady=5)
        second_lvl_record.grid(row=2, column=1, padx=5, pady=5)
        third_lvl_record.grid(row=3, column=1, padx=5, pady=5)

    def mainloop(self, window):
        window.mainloop()

    def close_window(self, window):
        window.destroy()