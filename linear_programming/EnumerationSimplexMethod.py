from itertools import combinations
import numpy as np


def converse_to_canonical(var_num, non_neg_rest_num, non_pos_rest_num, eq_rest_num, positive_indexes, func_coefs,
                          rest_coefs, rest_b):

    #############################
    #начальная проверка
    #проверка количества переменных
    #проверка пустоты матрицы
    #проверка соответствия вектора правой части
    #############################

    start_vars_count = var_num
    new_rest_coefs = rest_coefs.copy()
    new_rest_b = rest_b.copy()
    new_func_coefs = func_coefs.copy()

    #заменяем >= на <=
    for i in range(non_neg_rest_num):
        for j in range(len(new_rest_coefs[i])):
            new_rest_coefs[i][j] *= -1
        new_rest_b[i] *= -1

    # количество новых переменных, которые появятся после превращения неравенств в равенства
    new_neq_vars_count = non_neg_rest_num + non_pos_rest_num;

    for i in range(new_neq_vars_count):
        new_func_coefs.append(0)

    new_matrix = np.matrix(rest_coefs)
    #добавляем справа от неравенств единичную квадратную матрицу, оставшееся пространство заполняем нулями
    right_matrix = np.eye(new_neq_vars_count)
    if eq_rest_num > 0:
        right_matrix = np.vstack((right_matrix, np.zeros((eq_rest_num, new_neq_vars_count))))
    new_matrix = np.hstack((new_matrix, right_matrix))

    # замена знаконезависимых переменных

    transform_matrix = []
    additional_matrix = []
    columns_deleted = 0

    for i in range(start_vars_count):
        if i in positive_indexes:
            new_column = np.zeros(start_vars_count)
            new_column[i] = 1
            transform_matrix.append(new_column.tolist())
        else:
            # заменяем знаконезависимые переменные на разность двух новых положительных
            new_vars = np.zeros((new_matrix.shape[0], 2))
            for j in range(new_matrix.shape[0]):
                new_vars[j][0] = new_matrix.item((j, i - columns_deleted))
                new_vars[j][1] = -new_matrix.item((j, i - columns_deleted))
            new_matrix = np.delete(new_matrix, i - columns_deleted, 1)
            new_matrix = np.hstack((new_matrix, new_vars))
            new_func_coefs.append(new_func_coefs[i - columns_deleted])
            new_func_coefs.append(-new_func_coefs[i - columns_deleted])
            new_func_coefs.pop(i - columns_deleted)
            columns_deleted += 1
            # делаем столбцы для матрицы обратного перехода
            new_column = np.zeros(start_vars_count)
            new_column[i] = 1
            additional_matrix.append(new_column.tolist())
            new_column[i] = -1
            additional_matrix.append(new_column.tolist())

    for i in range(new_neq_vars_count):
        transform_matrix.append(np.zeros(start_vars_count).tolist())
    for i in additional_matrix:
        transform_matrix.append(i)
    transform_matrix = np.matrix(transform_matrix).transpose()

    return new_matrix, transform_matrix, new_rest_b, new_func_coefs


def find_all_matrices(A, M, N):
    """
    функция для перебора наборов из N переменных по M ненулевых. Возвращает соответствующие тамим наборам вектор матриц
    :param A: матрица ограничений в каноническом виде
    :param M: количество строк в матрице A
    :param N: количество столбцов в матрице A
    :return matrices: вектор невырожденных матриц составленных из столбцов A
    :return indexes: вектор с наборами индексов. В каждом наборе индексы соответствующих им столбцов расположены в том
        же порядке, что и в матрице из вектора matrices
    """
    start_matrix = np.matrix(A)
    index_set = [i for i in range(N)]
    matrices = []
    indexes = []

    for i in combinations(index_set, M):
        new_matrix = start_matrix[:, i]
        if abs(np.linalg.det(new_matrix)) > 1e-7:
            matrices.append(new_matrix)
            indexes.append(i)
    return matrices, indexes


def find_all_vectors(A, b, M, N):
    """
    функция для поиска всех опорных векторов
    :param A: матрица коэффициентов органичений в каноническом виде
    :param b: вектор правой части ограничений в каноническом виде
    :param M: количество строк в матрице A
    :param N: количество столбцов в матрице A
    :return: массив всех опорных векторов
    """
    vectors = []
    if M >= N:
        return []
    matrices, indexes = find_all_matrices(A, M, N)

    for i in range(len(indexes)):
        solution = np.linalg.solve(matrices[i], b)
        solution[abs(solution) < 1e-15] = 0

        if (len(solution[solution < 0]) != 0):
            continue

        if (len(solution[solution > 1e+15]) != 0):
            continue

        vector = [0 for i in range(N)]
        for j in range(len(indexes[i])):
            vector[indexes[i][j]] = solution[j]
        vectors.append(vector)
    return vectors


def EnumMethod(A, b, c, M, N, transform, max=False):
    """
    Метод перебора крайних точек
    :param M: количесво ограничений
    :param N: количество переменных
    :param A: матрица коэффициентов ограничений
    :param b: правый вектор ограничений
    :param c: вектор коэффициентов целевой функции
    :param transform: матрица перевода вектора к изначальной задаче (нужно только для логирования)
    :param max: True если нужно решать задачу максимизации вместо минимизации
    :return: опорный вектор при котором достигается оптимальное решение
    """
    mult = -1 if max else 1

    if max:
        for i in range(len(c)):
            c[i] *= mult

    f = open('EnumMethod.txt', 'w')

    vectors = find_all_vectors(A, b, M, N)
    if len(vectors) == 0:
        return []

    best_vector = vectors[0]
    min = np.dot(best_vector, c)
    i = 1
    min_i = 1
    for tmp in vectors:
        current_val = np.dot(tmp, c)
        f.write("step " + str(i) + ":\n")
        f.writelines(map(lambda x: str(x) + ' ', np.dot(transform, np.matrix(tmp).transpose()).transpose().tolist()[0]))
        f.write("\nf(X_" + str(i) + ") =" + str(current_val) + '\n')
        if current_val < min:
            min = current_val
            best_vector = tmp
            min_i = i
        i += 1
    f.write("\nbest vector on step " + str(min_i) + ":\n")
    f.writelines(
        map(lambda x: str(x) + ' ', np.dot(transform, np.matrix(best_vector).transpose()).transpose().tolist()[0]))

    f.write("\n\nsolution:")
    f.writelines(map(lambda y: str(y) + ' ', np.dot(transform, best_vector)))
    f.write("\nf(X) = " + str(np.dot(c, best_vector)))

    f.close()

    return (np.array(np.dot(transform, best_vector)) * mult).tolist()


def print_canon_task_human_readable(A, c, b):
    """
    функция для вывода канонической задачи ЛП на экран в читаемом для человека формате
    :param A: матрица ограничений
    :param c: вектор коэффициентов при функции
    :param b: вектор правой части ограниченй
    """
    new_A = np.matrix(A)
    new_c = np.matrix(c)
    new_b = np.matrix(b)
    s = "f(X) = "

    for i in range(new_c.shape[1]):
        if abs(new_c.item(i)) > 1e-13:
            if new_c.item(i) > 0 and i != 0:
                s += "+ "
            elif i != 0:
                s += "- "
            s += str(abs(new_c.item(i))) + "x_" + str(i + 1) + ' '
    s += "-> min\n"

    for i in range(new_A.shape[0]):
        for j in range(new_A.shape[1]):
            if abs(new_A.item(i, j)) > 1e-13:
                if new_A.item(i, j) > 0 and j != 0:
                    s += "+ "
                elif j != 0:
                    s += "- "
                s += str(abs(new_A.item(i, j))) + "x_" + str(j + 1) + ' '
        s += "= " + str(new_b.item(i)) + '\n'
    print(s)


def convertToDual(positive_indexes, func_coefs, non_neg_coefs, non_pos_coefs, eq_coefs, b):
    # 1
    new_c = b
    # 2
    new_b = func_coefs
    # 3
    A = []
    new_positive_indexes = []
    for i in range(len(non_neg_coefs)):
        new_positive_indexes.append(i)
        row = (np.array(non_neg_coefs[i])).tolist()
        A.append(row)
    positive_indexes_count = len(new_positive_indexes)

    for i in range(len(non_pos_coefs)):
        A.append(non_pos_coefs[i])
        new_positive_indexes.append(i + positive_indexes_count)

    for i in eq_coefs:
        A.append(i)
    A = np.matrix(A).transpose().tolist()

    new_non_neg_coefs = []
    new_eq_coefs = []

    for i in range(len(func_coefs)):
        if i in positive_indexes:
            new_non_neg_coefs.append(A[i])
        else:
            new_eq_coefs.append(A[i])

    return new_positive_indexes, new_c, new_non_neg_coefs, [], new_eq_coefs, new_b


if __name__ == "__main__":
    # positive = [0,1,2,4]
    # bigger = [[2,9,1,0,3]]
    # less = [[-3,-1,-4,-2,-10]]
    # equal = [[3,2,0,8,6],
    #          [9,3,0,8,2],
    #          [8,1,1,0,8]]
    # b = [1,-9,6,7,6]
    # c = [3,-4,2,1,4]

    positive = [0, 1, 2]
    c = [3, -4, 2, 1, 4, 3]
    bigger = [[2, 9, 1, 0, 3, 0],
              [4, -1, -2, -3, 10, 1]]
    less = [[-3, -1, -4, -2, -10, 3]
            ]
    equal = [[3, 2, 0, 8, 6, 0],
             [9, 3, 0, 8, 2, 2],
             [8, 1, 1, 0, 8, 0]]
    b = [1, -9, 2, 6, 7, 6]

    new_A, transform, new_b, new_c = converse_to_canonical(positive, c, bigger, less, equal, b)

    print_canon_task_human_readable(new_A, new_c, new_b)

    f = open('EnumMethod.txt', 'a')

    x = EnumMethod(new_A, new_b, new_c, new_A.shape[0], new_A.shape[1], transform)
