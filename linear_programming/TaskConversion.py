from copy import deepcopy


def creation_non_negative_vars(num_var, positive_indexes, non_neg_coefs_num, non_pos_coefs_num, eq_coefs_num,
                               rest_coefs, func_coefs):
    """Создание неотрицательных переменных, если в задаче существуют переменные без ограничения на знак"""
    new_num_var = num_var
    new_rest_coefs = deepcopy(rest_coefs)
    new_func_coefs = deepcopy(func_coefs)
    for i in range(new_num_var):
        if i not in positive_indexes:
            for j in range(non_neg_coefs_num):
                new_rest_coefs[j].append(-new_rest_coefs[j][i])

            for j in range(non_neg_coefs_num, non_pos_coefs_num + non_neg_coefs_num):
                new_rest_coefs[j].append(-new_rest_coefs[j][i])

            for j in range(non_pos_coefs_num + non_neg_coefs_num, eq_coefs_num + non_pos_coefs_num + non_neg_coefs_num):
                new_rest_coefs[j].append(-new_rest_coefs[j][i])

            new_func_coefs.append(-new_func_coefs[i])

            new_num_var += 1

    return new_num_var, new_rest_coefs, new_func_coefs


def conversion_to_standart(num_var, positive_indexes, non_neg_coefs_num, non_pos_coefs_num, eq_coefs_num, func_coefs,
                           rest_b, rest_coefs):
    """
    Преобразование задачи линейного программирования к канонической форме:
        1. На все переменные наложены условия неотрицательности
        2. Все ограничения имеют форму равенств
    """
    num_var, rest_coefs, func_coefs = creation_non_negative_vars(num_var, positive_indexes, non_neg_coefs_num,
                                                                 non_pos_coefs_num, eq_coefs_num, rest_coefs,
                                                                 func_coefs)
    A = []
    b = []

    for non_neg_rest in range(non_neg_coefs_num):
        A.append([-x for x in rest_coefs[non_neg_rest]])
        b.append(-rest_b[non_neg_rest])

    for non_pos_rest in range(non_neg_coefs_num, non_neg_coefs_num + non_pos_coefs_num):
        A.append(rest_coefs[non_pos_rest])
        b.append(rest_b[non_pos_rest])

    for eq in range(non_neg_coefs_num + non_pos_coefs_num, non_neg_coefs_num + non_pos_coefs_num + eq_coefs_num):
        A.append(rest_coefs[eq])
        b.append(rest_b[eq])
        b.append(-rest_b[eq])
        A.append([-x for x in rest_coefs[eq]])

    return A, b, func_coefs
