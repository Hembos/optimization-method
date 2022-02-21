import PySimpleGUI as sg
from TaskConversion import conversion_to_standart
import TableSymplexMethod


class Interface:
    def __init__(self):
        self.c = None
        self.b = None
        self.A = None
        self.__default = True

        # self.__var_num = 6
        # self.__non_neg_rest_num = 1
        # self.__non_pos_rest_num = 2
        # self.__eq_rest_num = 3
        #
        # self.__positive_indexes = [0, 1, 2]
        # self.__func_coefs = [1, -9, 2, 6, 7, 6]
        # self.__non_neg_coefs = []
        # self.__non_pos_coefs = [[1, -2, -4, 0, 0, 1],
        #                         [2, 4, -3, 3, 9, 8],
        #                         [9, -1, -1, 2, 3, 1]
        #                         ]
        # self.__eq_coefs = [[0, -3, -2, 8, 8, 0],
        #                    [1, 10, -10, 6, 2, 8],
        #                    [0, 1, 3, 0, 2, 0]]
        # self.__rest_b = [2, 3, -4, 1, 4, 3]

        self.__var_num = 6
        self.__non_neg_rest_num = 3
        self.__non_pos_rest_num = 0
        self.__eq_rest_num = 3

        self.__positive_indexes = [0, 1, 2]
        self.__func_coefs = [3, -4, 2, 1, 4, 3]
        self.__non_neg_coefs = [[2, 9, 1, 0, 3, 0],
                                [4, -1, -2, -3, 10, 1],
                                [3, 1, 4, 2, 10, -3]]
        self.__non_pos_coefs = [
                                ]
        self.__eq_coefs = [[3, 2, 0, 8, 6, 0],
                           [9, 3, 0, 8, 2, 2],
                           [8, 1, 1, 0, 8, 0]]
        self.__rest_b = [1, -9, -2, 6, 7, 6]

        self.__entering_func_window = None
        self.__main_window = self.__create_main_window()

    def __create_main_window(self):
        layout = [
            [
                sg.Text("Количество переменных:"),
                sg.In(size=(25, 1), enable_events=True, key="var_num")
            ],
            [
                sg.Text("Количество ограничений >= 0:"),
                sg.In(size=(25, 1), enable_events=True, key="restrictions_num_>=")
            ],
            [
                sg.Text("Количество ограничений <= 0:"),
                sg.In(size=(25, 1), enable_events=True, key="restrictions_num_<=")
            ],
            [
                sg.Text("Количество ограничений = 0:"),
                sg.In(size=(25, 1), enable_events=True, key="restrictions_num_=")
            ],
            [
                sg.Text("Индексы переменных >= 0:"),
                sg.In(size=(25, 1), key="positive_var_num")
            ],
            [
                sg.Button("Ввести функцию и ограничения"),
                sg.Button("Решить"),
                sg.Button("Выйти")
            ]
        ]

        return sg.Window("Simplex method", layout, finalize=True)

    def __create_entering_func_window(self):
        layout = [
            [
                sg.Text("Введите коэффициенты целевой функции"),
                sg.In(size=(25, 1), key="func_coefs")
            ]
        ]

        for i in range(int(self.__non_neg_rest_num)):
            layout.append(
                [
                    sg.Text(f">={i} Введите коэффициенты ограничения через пробел:"),
                    sg.In(size=(25, 1)),
                ]
            )

        for i in range(int(self.__non_pos_rest_num)):
            layout.append(
                [
                    sg.Text(f"<={i} Введите коэффициенты ограничения через пробел:"),
                    sg.In(size=(25, 1)),
                ]
            )

        for i in range(int(self.__eq_rest_num)):
            layout.append(
                [
                    sg.Text(f"={i} Введите коэффициенты ограничения через пробел:"),
                    sg.In(size=(25, 1)),
                ]
            )

        layout.append(
            [
                sg.Text(f"Введите вектор b правой части ограничений:"),
                sg.In(size=(25, 1), key=f"rest_b"),
            ]
        )

        layout.append([sg.Button("Создать")])

        return sg.Window("Function and restricts", layout, finalize=True)

    def create_task(self, values):
        if self.__default is False:
            for i in range(self.__non_neg_rest_num):
                self.__non_neg_coefs.append([float(x) for x in values[i].split(' ')])

            for i in range(self.__non_neg_rest_num, self.__non_neg_rest_num + self.__non_pos_rest_num):
                self.__non_pos_coefs.append([float(x) for x in values[i].split(' ')])

            for i in range(self.__non_neg_rest_num + self.__non_pos_rest_num,
                           self.__non_neg_rest_num + self.__non_pos_rest_num + self.__eq_rest_num):
                self.__eq_coefs.append([float(x) for x in values[i].split(' ')])

            self.__func_coefs = [float(x) for x in values["func_coefs"].split(' ')]
            self.__positive_indexes = [int(x) for x in self.__positive_indexes]
            self.__rest_b = [float(x) for x in values["rest_b"].split(' ')]

    def main_loop(self):
        while True:
            window, event, values = sg.read_all_windows()
            if event == "Выйти" or event == sg.WIN_CLOSED:
                window.close()
                if window == self.__main_window:
                    break
                elif window == self.__entering_func_window:
                    self.__entering_func_window = None

            if event == "var_num":
                self.__default = False
                self.__var_num = int(values["var_num"])
            elif event == "restrictions_num_>=":
                self.__non_neg_rest_num = int(values["restrictions_num_>="])
            elif event == "restrictions_num_<=":
                self.__non_pos_rest_num = int(values["restrictions_num_<="])
            elif event == "restrictions_num_=":
                self.__eq_rest_num = int(values["restrictions_num_="])
            elif event == "positive_var_num":
                self.__positive_indexes = values["positive_var_num"].split(' ')
            elif event == "Ввести функцию и ограничения":
                self.__entering_func_window = self.__create_entering_func_window()
            elif event == "Создать":
                self.create_task(values)
                self.A, self.b, self.c = conversion_to_standart(self.__var_num, self.__positive_indexes,
                                                                self.__non_neg_coefs,
                                                                self.__non_pos_coefs, self.__eq_coefs,
                                                                self.__func_coefs,
                                                                self.__rest_b)
                window.close()
                self.__entering_func_window = None
            elif event == "Решить":
                solution = TableSymplexMethod.get_optimal_solution(self.A, list(self.b), [-x for x in self.c],
                                                                   self.__var_num,
                                                                   len(self.A))
                j = self.__var_num
                for i in list(filter(lambda x: x not in self.__positive_indexes, range(self.__var_num))):
                    solution[i] -= solution[j]
                    j += 1
                del solution[self.__var_num:]
                print(solution)
                print(sum(x * y for (x, y) in zip(solution, self.c)))
