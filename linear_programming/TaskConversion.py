def creation_non_negative_vars(num_var, positive_indexes, non_neg_coefs_num, non_pos_coefs_num, eq_coefs_num,
                               rest_coefs, func_coefs):
    """Создание неотрицательных переменных, если в задаче существуют переменные без ограничения на знак"""
    for i in range(num_var):
        if i not in positive_indexes:
            for j in range(non_neg_coefs_num):
                rest_coefs[j].append(-rest_coefs[j][i])

            for j in range(non_neg_coefs_num, non_pos_coefs_num + non_neg_coefs_num):
                rest_coefs[j].append(-rest_coefs[j][i])

            for j in range(non_pos_coefs_num + non_neg_coefs_num, eq_coefs_num + non_pos_coefs_num + non_neg_coefs_num):
                rest_coefs[j].append(-rest_coefs[j][i])

            func_coefs.append(-func_coefs[i])

            num_var += 1

    return num_var, rest_coefs, func_coefs


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

def converse__to_dual(num_var, positive_indexes, non_neg_coefs_num, non_pos_coefs_num, eq_coefs_num, func_coefs,
                            rest_b, rest_coefs):
    """Преобразование к двойственной заадаче"""
