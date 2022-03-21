import math

import numpy as np

import bisect

import logging

def initialize_simplex(A, b, c, var_num, rest_num):
    """
    Находит начальную каноническую задачу, решение которой допустимо
    :param A: матрица ограничений
    :param b: вектор правой части ограничений
    :param c: вектор целевой функции
    :return: В случае неограниченной или неразрешимой задачи выбрасывается ошибка. Иначе возвращает начальную
        каноническую форму
    """
    min_b = min(b)
    ind_min_b = b.index(min_b)

    if min_b >= 0:
        return range(var_num), range(var_num, var_num + rest_num), A, b, c, 0

    N = list(range(var_num + 1))
    B = list(range(var_num + 1, var_num + rest_num + 1))

    size = len(b) + 1

    c_new = np.zeros(size)
    c_new[0] = -1

    for row in range(len(A)):
        A[row] = list(A[row])
        A[row].insert(0, -1)

    A.insert(0, np.zeros(size))
    b.insert(0, 0)

    v = 0

    l = ind_min_b + 1

    N, B, A, b, c_new, v = pivot(N, B, A, b, c_new, v, l, 0)
    delta = np.zeros(size)
    while next(filter(lambda j: round(c_new[j], 16) > 0, N), 'stop') != 'stop':
        for i in range(size):
            for j in range(size):
                A[i][j] = round(A[i][j], 16)
            c_new[i] = round(c_new[i], 16)
            b[i] = round(b[i], 16)

        e = next(filter(lambda i: round(c_new[i], 16) > 0, N))
        min_delta = math.inf
        for i in B:
            if A[i][e] > 0:
                delta[i] = b[i] / A[i][e]
            else:
                delta[i] = None

        for i in B:
            if min_delta > delta[i]:
                min_delta = delta[i]
                l = i

        if min_delta == math.inf:
            raise ValueError('Задача неограничена')
        else:
            N, B, A, b, c_new, v = pivot(N, B, A, b, c_new, v, l, e)

    if round(b[0], 14) == 0:
        for i in range(size):
            for j in range(size):
                A[i][j] = round(A[i][j], 14)

            c_new[i] = round(c_new[i], 14)
            b[i] = round(b[i], 14)

        if 0 in B:
            N, B, A, b, c_new, v = pivot(N, B, A, b, c_new, v, 0, N[0])
        N.remove(0)
        N = list(map(lambda x: x - 1, N))
        B = list(map(lambda x: x - 1, B))

        A = list(A)

        for row in range(len(A)):
            A[row] = list(A[row])
            A[row].pop(0)

        A.pop(0)
        b = list(b)
        b.pop(0)

        for i in range(len(c_new) - len(c) - 1):
            c.append(0)

        for j in B:
            for i in range(len(c)):
                if i != j:
                    c[i] -= c[j] * A[j][i]
            v += c[j] * b[j]
            c[j] = 0

        return list(N), list(B), list(A), list(b), list(c), v
    else:
        raise ValueError('задача неразрешима')


def pivot(N, B, A, b, c, v, l, e):
    """
    Переход от одной канонической задачи к другой (более оптимальной)
    :param N: небазисные переменные
    :param B: базисные переменные
    :param A: коэффициенты ограничения
    :param b: правая часть ограничений
    :param c: коэффициенты целевой функции
    :param v: свободный член целевой функции
    :param l: выводимая переменная
    :param e: вводимая переменная
    :return: каноническая задача
    """
    size = len(b)
    A_new = np.zeros((size, size))
    b_new = np.zeros(size)

    b_new[e] = b[l] / A[l][e]
    for j in N:
        if j != e:
            A_new[e][j] = A[l][j] / A[l][e]

    A_new[e][l] = 1 / A[l][e]

    for i in B:
        if i != l:
            b_new[i] = b[i] - A[i][e] * b_new[e]
            for j in N:
                if j != e:
                    A_new[i][j] = A[i][j] - A[i][e] * A_new[e][j]
            A_new[i][l] = -A[i][e] * A_new[e][l]

    v_new = v + c[e] * b_new[e]
    c_new = np.zeros(len(c))
    for j in N:
        if j != e:
            c_new[j] = c[j] - c[e] * A_new[e][j]

    c_new[l] = -c[e] * A_new[e][l]

    N_new = list(filter(lambda x: x != e, N))
    bisect.insort(N_new, l)
    B_new = list(filter(lambda x: x != l, B))
    bisect.insort(B_new, e)

    return N_new, B_new, A_new, b_new, c_new, v_new


def simplex(A, b, c, var_num, rest_num, positive_indexes, start_var_num, start_c):
    """
    Решает каноническую задачу линейного программирования
    :param A: матрица ограничений
    :param b: вектор правой части огарничений
    :param c: вектор целевой функции
    :return: возвращает вектор решения
    """
    N, B, A, b, c, v = initialize_simplex(A, b, c, var_num, rest_num)

    size = len(b)
    delta = np.zeros(size)
    while next(filter(lambda j: round(c[j], 16) > 0, N), 'stop') != 'stop':

        solution = np.zeros(len(A[0]))
        for i in range(len(A[0])):
            if i in B:
                solution[i] = b[i]
        j = start_var_num
        for i in list(filter(lambda x: x not in positive_indexes, range(start_var_num))):
            solution[i] -= solution[j]
            j += 1       
        solution = solution[:start_var_num]
        logging.info(solution)
        solution_value = sum(x * y for (x, y) in zip(solution, start_c))
        logging.info('\n')
        logging.info(solution_value)
        logging.info('\n')
        
        for i in range(size):
            for j in range(size):
                A[i][j] = round(A[i][j], 16)
            c[i] = round(c[i], 16)
            b[i] = round(b[i], 16)

        e = next(filter(lambda i: round(c[i], 16) > 0, N))
        min_delta = math.inf
        for i in B:
            if A[i][e] > 0:
                delta[i] = b[i] / A[i][e]
            else:
                delta[i] = None

        for i in B:
            if min_delta > delta[i]:
                min_delta = delta[i]
                l = i

        if min_delta == math.inf:
            raise ValueError('Задача неограничена')
        else:
            N, B, A, b, c, v = pivot(N, B, A, b, c, v, l, e)
    
    solution = np.zeros(len(A[0]))
    for i in range(len(A[0])):
        if i in B:
            solution[i] = b[i]

    return solution


def get_optimal_solution(A, b, c, positive_indexes, start_var_num, start_c):
    num_var = len(c)
    num_rest = len(b)
    size = num_var + num_rest

    A_new = np.zeros((size, size))
    b_new = np.zeros(size)
    c_new = np.zeros(size)

    for i in range(num_var, size):
        for j in range(num_var):
            A_new[i][j] = A[i - num_var][j]
        b_new[i] = b[i - num_var]

    for i in range(num_var):
        c_new[i] = c[i]

    return simplex(list(A_new), list(b_new), list(c_new), num_var, rest_num=num_rest, positive_indexes=positive_indexes, start_var_num=start_var_num, start_c=start_c)
