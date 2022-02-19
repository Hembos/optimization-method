class TaskConversion:
    """Преобразование задачи линейного программирования к другому виду"""

    def __init__(self, task):
        self.task = task
        self.num_var = task["number variables"]
        self.pos_var = task["indices of positive variables"]
        self.non_neg_rest = task["non-negative inequalities"]
        self.non_pos_rest = task["non-positive inequalities"]
        self.equalities = task["equalities"]
        self.obj_func = task["objective function"]

    def creation_non_negative_vars(self):
        """Создание неотрицательных переменных, если в задаче существуют переменные без ограничения на знак"""
        for i in range(self.task["number variables"]):
            if i not in self.task["indices of positive variables"]:
                self.pos_var.append(i)
                self.pos_var.append(self.num_var)

                for non_neg_ineq in self.task["non-negative inequalities"]:
                    non_neg_ineq.insert(self.num_var, -non_neg_ineq[i])

                for non_pos_ineq in self.task["non-positive inequalities"]:
                    non_pos_ineq.insert(self.num_var, -non_pos_ineq[i])

                for eq in self.task["equalities"]:
                    eq.insert(self.num_var, -eq[i])

                self.obj_func.append(-self.task["objective function"][i])

                self.num_var += 1

        self.task["indices of positive variables"] = sorted(self.pos_var)
        self.task["number variables"] = self.num_var

    def conversion_to_standart(self):
        """
        Преобразование задачи линейного программирования к стандартной форме:
            1. На все переменные наложены условия неотрицательности
            2. Все ограничения имеют форму неравенств <=
        """
        conv.creation_non_negative_vars()
        for non_neg_rest in self.non_neg_rest:
            self.non_pos_rest.append([-x for x in non_neg_rest])

        for eq in self.equalities:
            self.non_pos_rest.append(eq)
            self.non_pos_rest.append([-x for x in eq])

        self.non_neg_rest.clear()
        self.equalities.clear()

    def canonicalization(self):
        """
        Преобразование к каноническому виду:
            1. На все переменные наложены условия неотрицательности
            2. Все ограничения имеют форму равенств
        """
        self.conversion_to_standart()

        for non_pos_rest in self.non_pos_rest:
            self.pos_var.append(self.num_var)
            self.num_var += 1

        self.task["indices of positive variables"] = sorted(self.pos_var)
        self.task["number variables"] = self.num_var

    def transformation_to_dual(self):
        """Преобразование к двойственной задаче"""


if __name__ == "__main__":
    task = {
        "number variables": 2,
        "objective function": [2, -3],
        "non-negative inequalities": [],
        "non-positive inequalities": [[1, -2, 4]],
        "equalities": [[1, 1, 7]],
        "indices of positive variables": [0]
    }

    conv = TaskConversion(task)
    conv.canonicalization()
    print(conv.task)
