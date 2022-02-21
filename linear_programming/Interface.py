import PySimpleGUI as sg


class Interface:
    def __init__(self):
        self.__var_num = None
        self.__non_neg_rest_num = None
        self.__non_pos_rest_num = None
        self.__eq_rest_num = None

        self.__positive_indexes = []
        self.__func_coefs = []
        self.__non_neg_coefs = []
        self.__non_pos_coefs = []
        self.__eq_coefs = []
        self.__rest_b = []

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
        for i in range(self.__non_neg_rest_num):
            self.__non_neg_coefs.append([float(x) for x in values[i].split(' ')])

        for i in range(self.__non_neg_rest_num, self.__non_neg_rest_num + self.__non_pos_rest_num):
            self.__non_pos_coefs.append([float(x) for x in values[i].split(' ')])

        for i in range(self.__non_neg_rest_num + self.__non_pos_rest_num,
                       self.__non_neg_rest_num + self.__non_pos_rest_num + self.__eq_rest_num):
            self.__eq_coefs.append([float(x) for x in values[i].split(' ')])

        self.__func_coefs = [float(x) for x in values["func_coefs"].split()]
        self.__positive_indexes = [float(x) for x in values["positive_var_num"].split()]
        self.__rest_b = [float(x) for x in values["rest_b"].split()]

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
                self.__var_num = int(values["var_num"])
            elif event == "restrictions_num_>=":
                self.__non_neg_rest_num = int(values["restrictions_num_>="])
            elif event == "restrictions_num_<=":
                self.__non_pos_rest_num = int(values["restrictions_num_<="])
            elif event == "restrictions_num_=":
                self.__eq_rest_num = int(values["restrictions_num_="])
            elif event == "Ввести функцию и ограничения":
                self.__entering_func_window = self.__create_entering_func_window()
            elif event == "Создать":
                self.create_task(values)

