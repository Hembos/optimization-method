import PySimpleGUI as sg
import traceback

from PotentialMethod import get_solution

from TaskException import CreateTaskException

from TransitionToClosedView import TransitionToClosedView

from EnumerationMethod import solve_enum


class TransportTask:
    def __init__(self):
        self.storage = None
        self.destination = None
        self.transport_cost = None

        self.main_window = self.create_main_window()
        self.result_window = None

    def create_main_window(self):
        layout = [
            [
                sg.Text("Поставищики:"),
                sg.In(size=(25, 1), key="storage")
            ],
            [
                sg.Text("Потребители:"),
                sg.In(size=(25, 1), key="destination")
            ],
            [
                sg.Text("Матрица цен:"),
                sg.Multiline(size=(25, 10), key="transport_task")
            ],
            [
                sg.Button("Решить"),
                sg.Button("Решить задачу по умолчанию"),
                sg.Button("Выйти")
            ]
        ]

        return sg.Window("Transport task", layout=layout, finalize=True)

    def create_result_window(self, closed_transport_cost, closed_storage, closed_destinations, potential_solution, potential_solution_value, enum_solution, enum_solution_value):
        str_closed_transport_cost = ""

        for row in closed_transport_cost:
            for col in row:
                str_closed_transport_cost += f"{col}  "
            str_closed_transport_cost += "\n"

        str_closed_storage = ""
        for i in closed_storage:
            str_closed_storage += f"{i}  "

        str_closed_destinations = ""
        for i in closed_destinations:
            str_closed_destinations += f"{i}  "

        str_potential_solution = ""
        for i in range(len(closed_storage)):
            for j in range(len(closed_destinations)):
                if (i, j) in potential_solution:
                    str_potential_solution += str(potential_solution[(i, j)]) + '  '
                else:
                    str_potential_solution += "X  "
            str_potential_solution += "\n"
            
        str_enum_solution = ""
        for i in range(len(closed_storage)):
            for j in range(len(closed_destinations)):
                if enum_solution[i][j] != 0.0:
                    str_enum_solution += str(enum_solution[i][j]) + '  '
                else:
                    str_enum_solution += "X  "
            str_enum_solution += "\n"
            

        layout = [
            [
                sg.Text("Матрица стоимостей"),
                sg.Text(str_closed_transport_cost)
            ],
            [
                sg.Text("Поставщики:"),
                sg.Text(str_closed_storage)
            ],
            [
                sg.Text("Потребители:"),
                sg.Text(str_closed_destinations)
            ],
            [
                sg.Text("Решение методом потенциалов"),
                sg.Text(str_potential_solution),
                sg.Text(str(potential_solution_value))
            ],
            [
                sg.Text("Решение переборным методом"),
                sg.Text(str_enum_solution),
                sg.Text(str(enum_solution_value))
            ]
        ]

        return sg.Window("Transport task", layout, finalize=True)

    def create_default_task(self):
        self.storage = [19, 5, 21, 9]
        self.destination = [12, 12, 11, 8, 11]
        self.transport_cost = [
            [3, 2, 7, 11, 11],
            [2, 4, 5, 14, 8],
            [9, 4, 7, 15, 11],
            [2, 5, 1, 5, 3]
        ]

    def create_task(self, values):
        try:
            self.storage = [float(x) for x in values["storage"].split(' ')]
            self.destination = [float(x)
                                for x in values["destination"].split(' ')]
            self.transport_cost = [[float(x) for x in y.split(
                ' ')] for y in values["transport_task"].split('\n')]
            self.check_task()
        except Exception as e:
            tb = traceback.format_exc()
            sg.Print(f'An error happened.  Here is the info:', e, tb)
            sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)

    def check_task(self):
        rows_num = len(self.storage)
        cols_num = len(self.destination)

        if rows_num != len(self.transport_cost):
            raise CreateTaskException("Не совпадает количество строк")
        else:
            for row in self.transport_cost:
                if cols_num != len(row):
                    raise CreateTaskException(
                        "Не совпадает количество столбцов")

    def solve(self):
        closed_transport_cost, closed_storage, closed_destination, return_code = TransitionToClosedView(
            self.transport_cost, self.storage, self.destination)

        rows_num = len(closed_storage)
        cols_num = len(closed_destination)
        potential_solution, potential_solution_value = get_solution(
            closed_transport_cost, closed_storage, closed_destination, rows_num, cols_num)

        enum_solution, enum_solution_value = solve_enum(
            closed_transport_cost, closed_storage, closed_destination)
        
        self.result_window = self.create_result_window(
            closed_transport_cost, closed_storage, closed_destination, potential_solution, potential_solution_value, enum_solution, enum_solution_value)

    def main_loop(self):
        while True:
            event, values = self.main_window.read()
            if event == "Выйти" or event == sg.WIN_CLOSED:
                break
            elif event == "Решить задачу по умолчанию":
                self.create_default_task()
                self.solve()
            elif event == "Решить":
                self.create_task(values)
                self.solve()
