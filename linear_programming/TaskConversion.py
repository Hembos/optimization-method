def creation_non_negative_vars(num_var, positive_indexes, non_neg_coefs, non_pos_coefs):
    """Создание неотрицательных переменных, если в задаче существуют переменные без ограничения на знак"""
    for i in range(num_var):
        if i not in positive_indexes:
            for non_neg_ineq in non_neg_coefs:
                non_neg_ineq.insert(num_var, -non_neg_ineq[i])

            for non_pos_ineq in non_pos_coefs:
                non_pos_ineq.insert(num_var, -non_pos_ineq[i])

            for eq in self.task["equalities"]:
                eq.insert(self.num_var, -eq[i])

            obj_func.append(-self.task["objective function"][i])

            num_var += 1

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
