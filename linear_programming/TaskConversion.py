def creation_non_negative_vars(num_var, positive_indexes, non_neg_coefs, non_pos_coefs, eq_coefs, func_coefs):
    """Создание неотрицательных переменных, если в задаче существуют переменные без ограничения на знак"""
    for i in range(num_var):
        if i not in positive_indexes:
            for j in range(len(non_neg_coefs)):
                non_neg_coefs[j].insert(num_var, -non_neg_coefs[j][i])

            for j in range(len(non_pos_coefs)):
                non_pos_coefs[j].insert(num_var, -non_pos_coefs[j][i])

            for j in range(len(eq_coefs)):
                eq_coefs[j].insert(num_var, -eq_coefs[j][i])

            func_coefs.append(-func_coefs[i])

            num_var += 1

    return num_var, positive_indexes, non_neg_coefs, non_pos_coefs, eq_coefs, func_coefs


def conversion_to_standart(num_var, positive_indexes, non_neg_coefs, non_pos_coefs, eq_coefs, func_coefs, rest_b):
    """
    Преобразование задачи линейного программирования к стандартной форме:
        1. На все переменные наложены условия неотрицательности
        2. Все ограничения имеют форму неравенств <=
    """
    num_var, positive_indexes, non_neg_coefs, non_pos_coefs, eq_coefs, func_coefs = creation_non_negative_vars(num_var,
                                                                                                               positive_indexes,
                                                                                                               non_neg_coefs,
                                                                                                               non_pos_coefs,
                                                                                                               eq_coefs,
                                                                                                               func_coefs)
    i = 0
    num_non_pos = len(non_pos_coefs)

    A = []
    b = []

    for non_neg_rest in non_neg_coefs:
        A.append([-x for x in non_neg_rest])
        b.append(-rest_b[i])
        i += 1

    for non_pos_rest in non_pos_coefs:
        A.append(non_pos_rest)
        b.append(rest_b[i])
        i += 1

    for eq in eq_coefs:
        A.append(eq)
        b.append(rest_b[i])
        b.append(-rest_b[i])
        A.append([-x for x in eq])
        i += 1

    return A, b, func_coefs


if __name__ == "__main__":
    num_var = 6
    positive_indexes = [0, 1, 2]
    non_neg_coefs = []
    non_pos_coefs = [[2, 9, 1, 0, 3, 1],
     [-3, -1, 5, 2, -7, 2],
     [4, 7, 3, 1, -2, 5]]
    eq_coefs = [[4, 5, 10, 4, -3, 1],
     [0, 4, 2, 5, 2, -1],
     [2, 3, 1, 7, 2, -1]]
    func_coefs = [3, -4, 2, 1, 4, 7]
    rest_b = [1, -9, 5, 7, 3, 2]

    print(conversion_to_standart(num_var, positive_indexes, non_neg_coefs, non_pos_coefs, eq_coefs, func_coefs, rest_b))

