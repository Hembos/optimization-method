import numpy as np
from itertools import combinations
from TransitionToClosedView import *


def quick_check_zero_det(matrix: np.ndarray):
    zero_line = True
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if matrix.item(i, j) != 0:
                zero_line = False
                break
        if zero_line:
            return 0
        zero_line = True
    return 1


def make_simplex_task(transport_cost: list[list], storage: list, destination: list):
    vars_count = len(storage) * len(destination)
    dest_count = len(destination)
    storage_count = len(storage)
    if vars_count == 0:
        print("wrong input data")
        return
    A = []
    b = []
    c = []
    for i in range(len(storage)):
        A.append(i * dest_count * [0] + [1] * dest_count + [0] * (vars_count - (i + 1) * dest_count))
        b.append(storage[i])
        for j in range(len(destination)):
            c.append(transport_cost[i][j])
    for i in range(len(destination)):
        A.append(storage_count * (i * [0] + [1] + (dest_count - i - 1) * [0]))
        b.append(destination[i])

    return A, b, c


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
        g = i
        new_matrix = start_matrix[:, i]
        if quick_check_zero_det(new_matrix):
            det = abs(np.linalg.det(new_matrix))
            if det > 1e-7:
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


def enum_method(A, b, c, M, N, max=False):
    """
    Метод перебора крайних точек
    :param M: количесво ограничений
    :param N: количество переменных
    :param A: матрица коэффициентов ограничений
    :param b: правый вектор ограничений
    :param c: вектор коэффициентов целевой функции
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
        f.writelines(map(lambda x: str(x) + ' ', np.matrix(tmp).tolist()[0]))
        f.write("\nf(X_" + str(i) + ") =" + str(current_val) + '\n')
        if current_val < min:
            min = current_val
            best_vector = tmp
            min_i = i
        i += 1
    f.write("\nbest vector on step " + str(min_i) + ":\n")
    f.writelines(
        map(lambda x: str(x) + ' ', np.matrix(best_vector).tolist()[0]))

    f.write("\n\nsolution:")
    f.writelines(map(lambda y: str(y) + ' ', best_vector))
    f.write("\nf(X) = " + str(np.dot(c, best_vector)))

    f.close()

    return (np.array(best_vector) * mult).tolist(), min


def solve_enum(transport_cost: list[list], storage: list, destination: list):
    """
            функция для решения транспортной задачи перебором опорных точек
            :param transport_cost: матрица стоимостей перемещений
            :param storage: вектор с количеством хранящегося на складах товара
            :param destination: вектор с количеством необходимого в точках выгрузки товара
            :return result_matrix: матрица оптимальных перевозок
            :return best_value: сумма стоимостей оптимальных перевозок
        """
    A, b, c = make_simplex_task(transport_cost, storage, destination)

    # без удаления последней строки не работает
    A.pop(len(A) - 1)
    b.pop(len(b) - 1)
    x, best_value = enum_method(A, b, c, len(A), len(A[0]))
    result_matrix = np.reshape(x, (len(transport_cost), len(transport_cost[0]))).tolist()

    return result_matrix, best_value


if __name__ == '__main__':
    storagel = [16, 5, 15, 9]
    destinationl = [12, 12, 11, 8, 11]
    transport_costl = [
        [3, 2, 7, 11, 11],
        [2, 4, 5, 14, 8],
        [9, 4, 7, 15, 11],
        [2, 5, 1, 5, 3]
    ]
    print(solve_enum(transport_costl, storagel, destinationl))
