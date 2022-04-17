from math import *


def fun(x, y):
    return 2 * x**2 + y**2 + 2 * sin((x - y) / 2)


def fun_derivative_x(x, y):
    return 4 * x + cos((x - y) / 2)


def fun_derivative_y(x, y):
    return 2 * y - cos((x - y) / 2)


def fun_second_derivative_x(x, y):
    return 4 - sin((x - y) / 2) / 2


def fun_second_derivative_y(x, y):
    return 2 - sin((x - y) / 2) / 2
