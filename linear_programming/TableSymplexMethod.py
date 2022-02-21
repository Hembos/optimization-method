import bisect

import numpy as np


def simplex(A, b, c, var_num, rest_num, positive_indexes):
    """
    Табличный симплекси метод из Кормена
    :param rest_num: количесво ограничений
    :param var_num: количество переменных
    :param A: матрица коэффициентов ограничений
    :param b: правый вектор ограничений
    :param c: вектор коэффициентов целевой функции
    :return: целевой вектор при котором достигается оптимальное решение
    """
    original_c = list(c)
    N, B, A, b, c, v = initialize_simplex(A, b, c, var_num, rest_num)

    delta = list(np.zeros(len(b)))

    f = open('tableMethod.txt', 'w')
    step = 0
    while next(filter(lambda j: round(c[j], 16) > 0, N), 'stop') != 'stop':
        cur_sol = list(np.zeros(len(A[0])))
        for i in range(len(A[0])):
            if i in B:
                cur_sol[i] = b[i]

        j = rest_num
        for i in list(filter(lambda x: x not in positive_indexes, range(rest_num))):
            cur_sol[i] -= cur_sol[j]
            j += 1

        del cur_sol[rest_num:]
        step += 1
        f.write(f"\nstep {step}:\nsolution: ")
        f.writelines(map(lambda y: str(y) + ' ', cur_sol))
        f.write("\nf_value: " + str(sum(-x * y for (x, y) in zip(cur_sol, original_c))))

        e = next(filter(lambda i: round(c[i], 16) > 0, N))
        min_delta = None
        for i in B:
            if A[i][e] > 0:
                delta[i] = b[i] / A[i][e]
            else:
                delta[i] = None

        for i in B:
            if min_delta is None or (delta[i] is not None and min_delta > delta[i]):
                min_delta = delta[i]
                l = i

        if min_delta is None:
            raise ValueError('Задача неограничена')
        else:
            N, B, A, b, c, v = pivot(N, B, A, b, c, v, l, e)

    solution = np.zeros(len(A[0]))
    for i in range(len(A[0])):
        if i in B:
            solution[i] = b[i]

    f.close()

    return solution, c


def pivot(N, B, A, b, c, v, l, e):
    """
    Замещение - переход от одной канонической задачи к другой (более оптимальной)
    :param N: множество индексов небазисных переменных
    :param B: множество индексов базисных переменных
    :param A: матрица ограничений
    :param b: вектор правой части ограничений
    :param c: вектор целевой функции
    :param v: свободный член в целевой функции
    :param l: индекс выводимой переменной
    :param e: индекс вводимой переменной
    :return: новая каноническая задача
    """
    n = len(A[0])
    m = len(b)

    b_new = list(np.zeros(m))
    A_new = list(np.zeros((m, n)))

    b_new[e] = b[l] / A[l][e]

    for j in list(filter(lambda x: x != e, N)):
        A_new[e][j] = A[l][j] / A[l][e]

    A_new[e][l] = 1 / A[l][e]

    for i in list(filter(lambda x: x != l, B)):
        b_new[i] = b[i] - A[i][e] * b_new[e]
        for j in list(filter(lambda x: x != e, N)):
            A_new[i][j] = A[i][j] - A[i][e] * A_new[e][j]
        A_new[i][l] = -A[i][e] * A_new[e][l]

    v_new = v + c[e] * b_new[e]

    c_new = np.zeros(len(c))
    for j in list(filter(lambda x: x != e, N)):
        c_new[j] = c[j] - c[e] * A_new[e][j]
    c_new[l] = -c[e] * A_new[e][l]

    N_new = list(filter(lambda x: x != e, N))
    bisect.insort(N_new, l)
    B_new = list(filter(lambda x: x != l, B))
    bisect.insort(B_new, e)

    return N_new, B_new, A_new, b_new, c_new, v_new


def initialize_simplex(A, b, c, var_num, rest_num):
    """
    Если задача неразрешима, то выводится соответствующее сообщение. Иначе возвращает каноническую форму, начальное
    базисное решение которой допустимое
    :param rest_num: количесво ограничений
    :param var_num: количество переменных
    :param A: матрица ограничений
    :param b: правый вектор
    :param c: вектор целевой функции
    :return: ошибку или каноническую форму
    """
    min_b = min(b)
    ind_min_b = b.index(min_b)

    if min_b >= 0:
        return converse_to_canonical(A, b, c)

    c_new = list(np.zeros(len(c) + 1))
    c_new[0] = -1

    for row in A:
        row.insert(0, -1)

    N, B, A, b, c_new, v = converse_to_canonical(A, b, c_new)

    l = var_num + ind_min_b + 1

    N, B, A, b, c_new, v = pivot(N, B, A, b, c_new, v, l, 0)

    delta = list(np.zeros(len(b)))

    while next(filter(lambda q: round(c_new[q], 16) > 0, N), 'stop') != 'stop':
        e = next(filter(lambda q: round(c_new[q], 16) > 0, N))
        min_delta = None
        for i in B:
            if A[i][e] > 0:
                delta[i] = b[i] / A[i][e]
            else:
                delta[i] = None

        for i in B:
            if min_delta is None or (delta[i] is not None and min_delta > delta[i]):
                min_delta = delta[i]
                l = i

        if min_delta is None:
            raise ValueError('Задача неограничена')
        else:
            N, B, A, b, c_new, v = pivot(N, B, A, b, c_new, v, l, e)

    if round(b[0], 16) == 0:
        if 0 in B:
            N, B, A, b, c_new, v = pivot(N, B, A, b, c_new, v, 0, N[0])
        N.remove(0)
        N = list(map(lambda x: x - 1, N))
        B = list(map(lambda x: x - 1, B))

        for row in range(len(A)):
            A[row] = np.delete(A[row], 0)

        A.pop(0)
        b.pop(0)

        for i in range(len(c_new) - len(c) - 1):
            c.append(0)

        for j in B:
            for i in range(len(c)):
                if i != j:
                    c[i] -= c[j] * A[j][i]
            v += c[j] * b[j]
            c[j] = 0

        return N, B, A, b, c, v
    else:
        raise ValueError('задача неразрешима')


def converse_to_canonical(A, b, c):
    """
    Преобразование стандартной задачи (все ограничения <=) к канонической (все ограничения в виде равенств)
    :param A: матрица коэффициентов ограничений
    :param b: вектор правой части ограничений
    :param c: вектор целевой функции
    :return: каноническую задачу в виде (N, B, A, b, c, v):
                N: множество индексов небазисных переменных
                B: множество индексов базисных переменных
                A: матрица ограничений
                b: вектор правой части ограничений
                c: вектор целевой функции
                v: свободный член в целевой функции
    """
    m = len(b)
    n = len(c)

    N = list(range(0, n))
    B = list(range(n, n + m))

    A_new = np.zeros((n + m, n + m))
    for i in B:
        for j in N:
            A_new[i][j] = A[i - n][j]

    b_new = np.zeros(n + m)
    for i in B:
        b_new[i] = b[i - n]

    c.extend(np.zeros(m))

    return N, B, A_new, b_new, c, 0


def get_optimal_solution(A, b, c, var_num, rest_num, positive_indexes):
    solution, c_dual = simplex(A, b, c, var_num, rest_num, positive_indexes)
    #    fun_value = sum(x * y for (x, y) in zip(solution, c))

    return list(solution), list(c_dual)


if __name__ == "__main__":
    c = [-2, 3, -3]
    A = [[1, 1, -1], [-1, -1, 1], [1, -2, 2]]
    b = [7, -7, 4]

    # B = [3, 4, 5]
    # N = [0, 1, 2]
    #
    # A = [
    #     [1, 1, 3],
    #     [2, 2, 5],
    #     [4, 1, 2]
    # ]
    #
    # b = [30, 24, 36]
    # c = [3, 1, 2]
    #
    # v = 0
    # e = 0
    # l = 5

    # B = [3, 4]
    # N = [0, 1]
    #
    # A = [
    #     [2, -1],
    #     [1, -5]
    # ]
    #
    # b = [2, -4]
    # c = [2, -1]
    # v = 0
    # e = 0
    # l = 5

    solution = get_optimal_solution(A, b, c, 3, 3)
    c = [2, -3, 3]
    print(solution, sum(x * y for (x, y) in zip(solution, c)))
