import logging
import traceback

import PySimpleGUI as sg
from TaskConversion import conversion_to_standart
import TableSymplexMethod
from EnumerationSimplexMethod import converse_to_canonical
from EnumerationSimplexMethod import EnumMethod, convertToDual


class Interface:
    def __init__(self):
        self.c = None
        self.b = None
        self.A = None

        self.__var_num = None
        self.__non_neg_rest_num = None
        self.__non_pos_rest_num = None
        self.__eq_rest_num = None

        self.__positive_indexes = None
        self.__func_coefs = None
        self.__rest_coefs = None
        self.__rest_b = None

        self.__main_window = self.__create_main_window()
        self.__solution_window = None

    def __create_main_window(self):
        layout = [
            [
                sg.Text("Количество переменных:"),
                sg.In(size=(25, 1), key="var_num")
            ],
            [
                sg.Text("Количество ограничений >= 0:"),
                sg.In(size=(25, 1), key="restrictions_num_>=")
            ],
            [
                sg.Text("Количество ограничений <= 0:"),
                sg.In(size=(25, 1), key="restrictions_num_<=")
            ],
            [
                sg.Text("Количество ограничений = 0:"),
                sg.In(size=(25, 1), key="restrictions_num_=")
            ],
            [
                sg.Text("Индексы переменных >= 0:"),
                sg.In(size=(25, 1), key="positive_var")
            ],
            [
                sg.Text("Введите коэффициенты целевой функции"),
                sg.In(size=(25, 1), key="func_coefs")
            ],
            [
                sg.Text("Введите коэффициенты ограничения:"),
                sg.Multiline(size=(25, 10), key="rest_coefs"),
            ],
            [
                sg.Text(f"Введите вектор b правой части ограничений:"),
                sg.In(size=(25, 1), key="rest_b"),
            ],
            [
                sg.Button("Решить"),
                sg.Button("Решить задачу по умолчанию"),
                sg.Button("Выйти")
            ]
        ]

        return sg.Window("Simplex method", layout, finalize=True)

    def create_task(self, values):
        try:
            self.__var_num = int(values["var_num"])
            self.__non_neg_rest_num = int(values["restrictions_num_>="])
            self.__non_pos_rest_num = int(values["restrictions_num_<="])
            self.__eq_rest_num = int(values["restrictions_num_="])
            self.__positive_indexes = [int(i) for i in values["positive_var"].split(' ')]
            self.__func_coefs = [float(i) for i in values["func_coefs"].split(' ')]
            self.__rest_coefs = [[float(j) for j in i.split(' ')] for i in values["rest_coefs"].split('\n')]
            self.__rest_b = [float(i) for i in values["rest_b"].split(' ')]
        except Exception as e:
            tb = traceback.format_exc()
            sg.Print(f'An error happened.  Here is the info:', e, tb)
            sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)

    def create_default_task(self):
        # self.__var_num = 6
        # self.__non_neg_rest_num = 0
        # self.__non_pos_rest_num = 3
        # self.__eq_rest_num = 3

        # self.__positive_indexes = [0, 1, 2]
        # self.__func_coefs = [1, -9, -2, 6, 7, 6]
        # self.__rest_coefs = [
        #     [2, 4, 3, 3, 9, 8],
        #     [9, -1, 1, 2, 3, 1],
        #     [1, -2, 4, 0, 0, 1],
        #     [0, -3, 2, 8, 8, 0],
        #     [3, 10, 10, 6, 2, 8],
        #     [0, 1, -3, 0, 2, 0]
        # ]
        # self.__rest_b = [3, -4, 2, 1, 4, 3]

        self.__var_num = 6
        self.__non_neg_rest_num = 2
        self.__non_pos_rest_num = 1
        self.__eq_rest_num = 3
        
        self.__positive_indexes = [0, 1, 2]
        self.__func_coefs = [3, -4, 2, 1, 4, 3]
        self.__rest_coefs = [
            [2, 9, 1, 0, 3, 0],
            [4, -1, -2, -3, 10, 1],
            [-3, -1, -4, -2, -10, 3],
            [3, 2, 0, 8, 6, 0],
            [9, 3, 0, 8, 2, 2],
            [8, 1, 1, 0, 8, 0]
        ]
        self.__rest_b = [1, -9, 2, 6, 7, 6]

        # self.__var_num = 3
        # self.__non_neg_rest_num = 0
        # self.__non_pos_rest_num = 3
        # self.__eq_rest_num = 0
        # self.__positive_indexes = [0, 1, 2]
        # self.__func_coefs = [3, 1, 2]
        # self.__rest_coefs = [
        #     [1, 1, 3],
        #     [2, 2, 5],
        #     [4, 1, 2]
        # ]
        # self.__rest_b = [30, 24, 36]

        # self.__var_num = 3
        # self.__non_neg_rest_num = 3
        # self.__non_pos_rest_num = 0
        # self.__eq_rest_num = 0
        # self.__positive_indexes = [0, 1, 2]
        # self.__func_coefs = [30, 24, 36]
        # self.__rest_coefs = [
        #     [1, 2, 4],
        #     [1, 2, 1],
        #     [3, 5, 2]
        # ]
        # self.__rest_b = [3, 1, 2]

        # self.__var_num = 5
        # self.__non_neg_rest_num = 1
        # self.__non_pos_rest_num = 1
        # self.__eq_rest_num = 3
        #
        # self.__positive_indexes = [0, 1, 2, 4]
        # self.__func_coefs = [3, -4, 2, 1, 4]
        # self.__rest_coefs = [
        #     [2, 9, 1, 0, 3],
        #     [-3, -1, -4, -2, -10],
        #     [3, 2, 0, 8, 6],
        #     [9, 3, 0, 8, 2],
        #     [8, 1, 1, 0, 8]
        # ]
        # self.__rest_b = [1, -9, 6, 7, 6]

    def task_to_str(self, var_num, func_coefs, non_neg_rest_num, non_pos_rest_num, eq_rest_num, rest_coefs, rest_b):
        task = "f(x) = "
        for j in range(var_num):
            task += f'{func_coefs[j]}*x{j}'
            if j != var_num - 1:
                task += ' + '
        task += '\n'
        for i in range(non_neg_rest_num + non_pos_rest_num + eq_rest_num):
            for j in range(var_num):
                task += str(rest_coefs[i][j])
                task += f'*x{j}'
                if j != var_num - 1:
                    task += ' + '
            if i < non_neg_rest_num:
                task += ' >= '
            elif i < non_neg_rest_num + non_pos_rest_num:
                task += ' <= '
            else:
                task += ' = '
            task += str(rest_b[i])
            task += '\n'

        return task

    def get_simplex_solution(self, var_num, non_neg_rest_num, non_pos_rest_num, eq_rest_num,
                             positive_indexes, func_coefs, rest_coefs, rest_b, its_min):
        A, b, c = conversion_to_standart(var_num, positive_indexes,
                                         non_neg_rest_num, non_pos_rest_num,
                                         eq_rest_num, func_coefs,
                                         rest_b, rest_coefs)
        """Здесь решается симплекс методом"""
        solution = TableSymplexMethod.get_optimal_solution(A, b, [-x*its_min for x in c], positive_indexes, var_num, c)
        solution_value = sum(x * y for (x, y) in zip(solution, c))

        j = var_num
        for i in list(filter(lambda x: x not in positive_indexes, range(var_num))):
            solution[i] -= solution[j]
            j += 1

        solution = solution[:var_num]

        return solution, solution_value

    def get_enum_solution(self, var_num, non_neg_rest_num, non_pos_rest_num, eq_rest_num,
                          positive_indexes, func_coefs, rest_coefs, rest_b, its_min):
        new_A, transform, new_b, new_c = converse_to_canonical(var_num, non_neg_rest_num,
                                                               non_pos_rest_num, eq_rest_num,
                                                               positive_indexes, func_coefs,
                                                               rest_coefs, rest_b)

        solution = EnumMethod(new_A, new_b, [x*its_min for x in new_c], new_A.shape[0], new_A.shape[1], transform)
        solution_value = sum(x * y for (x, y) in zip(solution[0], func_coefs))

        return solution, solution_value

    def solve(self):
        dual_var_num, dual_non_neg_rest_num, dual_non_pos_rest_num, dual_eq_rest_num, \
        dual_positive_indexes, dual_func_coefs, dual_rest_coefs, dual_rest_b = \
            convertToDual(self.__var_num, self.__non_neg_rest_num, self.__non_pos_rest_num, self.__eq_rest_num,
                          self.__positive_indexes, self.__func_coefs, self.__rest_coefs, self.__rest_b)

        logging.info("Прямая задача")
        solution1, solution_value1 = self.get_simplex_solution(self.__var_num, self.__non_neg_rest_num,
                                                               self.__non_pos_rest_num, self.__eq_rest_num,
                                                               self.__positive_indexes, self.__func_coefs,
                                                               self.__rest_coefs, self.__rest_b, 1)
        solution2, solution_value2 = self.get_enum_solution(self.__var_num, self.__non_neg_rest_num,
                                                            self.__non_pos_rest_num, self.__eq_rest_num,
                                                            self.__positive_indexes, self.__func_coefs,
                                                            self.__rest_coefs, self.__rest_b, 1)
        logging.info("Двойственная задача")
        dual_solution1, dual_solution_value1 = self.get_simplex_solution(dual_var_num, dual_non_neg_rest_num,
                                                               dual_non_pos_rest_num, dual_eq_rest_num,
                                                               dual_positive_indexes, dual_func_coefs,
                                                               dual_rest_coefs, dual_rest_b, -1)
        dual_solution2, dual_solution_value2 = self.get_enum_solution(dual_var_num, dual_non_neg_rest_num,
                                                               dual_non_pos_rest_num, dual_eq_rest_num,
                                                               dual_positive_indexes, dual_func_coefs,
                                                               dual_rest_coefs, dual_rest_b, -1)

        layout = [
            [
              sg.Text("Прямая задача")
            ],
            [
                sg.Text(self.task_to_str( self.__var_num, self.__func_coefs, self.__non_neg_rest_num,
                                         self.__non_pos_rest_num, self.__eq_rest_num, self.__rest_coefs,
                                         self.__rest_b))
            ],
            [
                sg.Text("Симплекс метод"),
                sg.Text(solution1)
            ],
            [
                sg.Text(solution_value1)
            ],
            [
                sg.Text("Переборный метод"),
                sg.Text(solution2[0])
            ],
            [
                sg.Text(solution_value2)
            ]
        ]
        layout_dual = [
            [
                sg.Text("Двойственная задача")
            ],
            [
                sg.Text(self.task_to_str(dual_var_num, dual_func_coefs, dual_non_neg_rest_num, dual_non_pos_rest_num,
                                         dual_eq_rest_num, dual_rest_coefs, dual_rest_b))
            ],
            [
                sg.Text("Симплекс метод"),
                sg.Text(dual_solution1)
            ],
            [
                sg.Text(dual_solution_value1)
            ],
            [
                sg.Text("Переборный метод"),
                sg.Text(dual_solution2[0])
            ],
            [
                sg.Text(dual_solution_value2)
            ]
        ]
        layout.append(layout_dual)
        self.__solution_window = sg.Window("Simplex method", layout, finalize=True)

    def main_loop(self):
        while True:
            event, values = self.__main_window.read()
            if event == "Выйти" or event == sg.WIN_CLOSED:
                break
            elif event == "Решить":
                self.create_task(values)
                self.solve()
            elif event == "Решить задачу по умолчанию":
                self.create_default_task()
                self.solve()

            # elif event == "Решить":
            #     solution, c_for_dual = TableSymplexMethod.get_optimal_solution(self.A, list(self.b),
            #                                                                    [-x for x in self.c],
            #                                                                    len(self.c),
            #                                                                    self.__var_num,
            #                                                                    self.__positive_indexes)
            #     j = self.__var_num
            #     for i in list(filter(lambda x: x not in self.__positive_indexes, range(self.__var_num))):
            #         solution[i] -= solution[j]
            #         j += 1
            #
            #     print(sum(x * y for (x, y) in zip(c_for_dual[self.__var_num + 3:], self.b)))
            #
            #     del solution[self.__var_num:]
            #     print(solution)
            #     print(sum(x * y for (x, y) in zip(solution, self.c)))
