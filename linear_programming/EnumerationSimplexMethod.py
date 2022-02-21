from itertools import combinations
import numpy as np


def converse_to_canonical(positive_indexes, func_coefs, non_neg_coefs, non_pos_coefs, eq_coefs, rest_b):
    """
    функция для перевода задачи линейного программирования в канонический вид
    :param positive_indexes: индексы положительных переменных
    :param func_coefs: коэффициенты при переменных в функции цели
    :param non_neg_coefs: вектор коэффициентов при переменных в ограничениях >= b_i
    :param non_pos_coefs: вектор коэффициентов при переменных в ограничениях <= b_i
    :param eq_coefs: вектор коэффициентов при переменных в ограничениях == b_i
    :return new_matrix: матрица ограничений в каноническом виде A (a_i * X == b_i)
    :return transform_matrix: матрица для перевода вектора решения к начальной задаче x_old = (transform_matrix * x_new)
    :return new_rest_b: вектор правой части ограничений в каноническом виде AX == b
    :return new_func_coefs: вектор коэффициентов функции в каноническом виде f(X) = c' * X
    """

    non_neg_matrix = np.matrix(non_neg_coefs)
    non_pos_matrix = np.matrix(non_pos_coefs)
    eq_matrix = np.matrix(eq_coefs)
    start_vars_count = max(non_neg_matrix.shape[1], eq_matrix.shape[1], non_pos_matrix.shape[1])
    new_rest_b = rest_b.copy()
    new_func_coefs = func_coefs.copy()

    # количество новых переменных, которые появятся после превращения неравенств в равенства
    new_neq_vars_count = len(non_neg_coefs) + len(non_pos_coefs)

    for i in range(len(non_neg_matrix)):  # заменяем знаки >= на <= в неравенствах
        new_rest_b[i] *= -1
        for j in range(len(non_neg_matrix[i])):
            non_neg_matrix[i][j] *= -1
    for i in range(new_neq_vars_count):
        new_func_coefs.append(0)

    # объединяем неравенства в общую матрицу вертикально
    if len(non_pos_coefs) == 0:
        if len(non_neg_coefs) > 0:
            new_matrix = non_neg_matrix
        else:
            if len(eq_coefs) == 0:
                return [], [], [], []
            else:
                return eq_matrix, np.eye(eq_matrix.shape[1]), new_rest_b, new_func_coefs
    else:
        if len(non_neg_coefs) > 0:
            new_matrix = np.vstack((non_neg_matrix, non_pos_matrix))
        else:
            new_matrix = non_pos_matrix

    # добавляем единичную матрицу справа, чтобы превратить неравенства в равенства
    new_matrix = np.hstack((new_matrix, np.eye(new_matrix.shape[0])))
    # добавляем к матрице коэффициентов равенств нулевую матрицу справа
    if len(eq_coefs) > 0:
        new_eq_matrix = np.hstack((eq_matrix, np.zeros((eq_matrix.shape[0], new_matrix.shape[1] - eq_matrix.shape[1]))))
        # объединяем бывшие неравенства с равенствами, получаем квадратную матрицу
        new_matrix = np.vstack((new_matrix, new_eq_matrix))

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

    vectors = find_all_vectors(A, b, M, N)
    if len(vectors) == 0:
        return []

    best_vector = vectors[0]
    min = np.dot(best_vector, c)
    i = 1
    min_i = 1
    for tmp in vectors:
        current_val = np.dot(tmp, c)
        # print("step " + str(i) + ":")
        if (current_val < min):
            min = current_val
            best_vector = tmp
            min_i = i
        print(np.dot(transform, np.matrix(tmp).transpose() * mult).transpose().tolist(), '\n', "f(X_" + str(i) + ") =",
              current_val * mult, '\n')
        i += 1

    print("best vector on step " + str(min_i) + ":\n",
          np.dot(transform, np.matrix(best_vector).transpose() * mult).transpose().tolist())

    return (np.array(best_vector) * mult).tolist()


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
    c = [1, -9, -2, 6, 7, 6]
    bigger = []
    less = [
        [2, 4, 3, 3, 9, 8],
        [9, -1, 1, 2, 3, 1],
        [1, -2, 4, 0, 0, 1]
    ]
    equal = [[0, -3, 2, 8, 8, 0],
             [3, 10, 10, 6, 2, 8],
             [0, 1, -3, 0, 2, 0]]
    b = [3, -4, 2, 1, 4, 3]

    new_A, transform, new_b, new_c = converse_to_canonical(positive, c, bigger, less, equal, b)

    print_canon_task_human_readable(new_A, new_c, new_b)

    x = EnumMethod(new_A, new_b, new_c, new_A.shape[0], new_A.shape[1], transform, True)
    print("\nsolution:", np.dot(transform, x))
    print("f(X) = ", np.dot(new_c, x))
