import PySimpleGUI as sg


class Interface:
    def __init__(self):
        self.__positive_indexes = None
        self.__restrictions_num = None
        self.__var_num = None
        self.__entering_func_window = None
        self.__main_window = self.__create_main_window()

    def __create_main_window(self):
        layout = [
            [
                sg.Text("Количество переменных:"),
                sg.In(size=(25, 1), enable_events=True, key="var_num")
            ],
            [
                sg.Text("Количество ограничений:"),
                sg.In(size=(25, 1), enable_events=True, key="restrictions_num")
            ],
            [
                sg.Text("Индексы переменных >= 0:"),
                sg.In(size=(25, 1), enable_events=True, key="positive_var_num")
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
                sg.In(size=(25, 1), enable_events=True, key="func_coefs")
            ]
        ]

        for i in range(int(self.__restrictions_num)):
            layout.append(
                [
                    sg.Text(f"Введите коэффициенты ограничения {i} через пробел:"),
                    sg.In(size=(25, 1), enable_events=True, key=f"rest_coef_{i}"),
                    sg.InputCombo([">=", "<=", "="], size=(2, 3), default_value=">=", key=f"sign_{i}"),
                    sg.In(size=(3, 1), enable_events=True, key=f"rest_b_{i}")
                ]
            )

        layout.append([sg.Button("Выйти")])

        return sg.Window("Function and restricts", layout, finalize=True)

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
                self.__var_num = values["var_num"]
            elif event == "restrictions_num":
                self.__restrictions_num = values["restrictions_num"]
            elif event == "positive_var_num":
                self.__positive_indexes = values["positive_var_num"].split(' ')
            elif event == "Ввести функцию и ограничения":
                self.__entering_func_window = self.__create_entering_func_window()
