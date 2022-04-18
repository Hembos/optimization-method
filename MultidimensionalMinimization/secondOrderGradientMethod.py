import numpy as np
import numpy.linalg as la
from function import *


def f(x: np.array) -> np.array:
    return fun(x.item(0), x.item(1))


def f_grad(x: np.array) -> np.array:
    return np.array([fun_derivative_x(x.item(0), x.item(1)), fun_derivative_y(x.item(0), x.item(1))])


def find_alpha(x_k: np.array, p_k: np.array, eps: float, max_step: float):
    left = 1e-7
    right = max_step

    while abs(right - left) > eps:
        center = (right + left) / 2
        delta = (right - left) / 100
        y1 = f(x_k + (center - delta) * p_k)
        y2 = f(x_k + (center + delta) * p_k)

        if y1 > y2:
            left = center
        else:
            right = center

    return (right + left) / 2


def bfgs_solve(x_0: list, eps: float, max_step: float, n: int):
    xk = np.array(x_0)
    N = len(xk)
    I = np.eye(N, dtype=float)
    Ak = I
    omega = -f_grad(xk)
    iteration = 0

    while la.norm(omega) > eps:
        pk = np.dot(Ak, omega)
        alpha_k = find_alpha(xk, pk, eps, max_step)
        xk_new = xk + alpha_k * pk
        dxk = xk_new - xk
        omega_new = -f_grad(xk_new)
        domega = omega_new - omega
        dAk1 = (dxk * np.transpose(dxk)).item(0) / (np.transpose(omega) * dxk).item(0)
        dAk2 = (Ak * domega * np.transpose(domega) * np.transpose(Ak)).item(0) / (
                np.transpose(domega) * Ak * domega).item(0)
        Ak_new = Ak - dAk1 - dAk2
        Ak = Ak_new
        xk = xk_new
        omega = omega_new
        iteration += 1
        if iteration % n == 0:
            Ak = I

    return xk, f(xk), iteration


if __name__ == '__main__':
    print(bfgs_solve([100, 0], 1e-1, 10, 1))
