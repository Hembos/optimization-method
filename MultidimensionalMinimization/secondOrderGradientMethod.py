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
    """

    Args:
        x_0: начальная точка
        eps: точность
        max_step: максимальный шаг
        n: частота сброса Ak

    Returns: точка минимума, значение функции в точке минимума, количество итераций

    """
    xk = np.array(x_0)
    N = len(xk)
    I = np.eye(N, dtype=float)
    Ak = I
    omega = -f_grad(xk)
    iteration = 0
    file = open('secondOrderGradientMethod.log', 'w')
    while True:
        file.write("iteration: " + str(iteration) + '\n' + "x_k: [" + str(xk.item(0)) + "," + str(
            xk.item(1)) + "]\nf(X_k) = " + str(f(xk)) + "\n")
        pk = np.dot(Ak, omega)
        alpha_k = find_alpha(xk, pk, eps, max_step)
        xk_new = xk + alpha_k * pk
        dxk = xk_new - xk
        omega_new = -f_grad(xk_new)
        domega = omega_new - omega
        dAk1 = (dxk * np.transpose(dxk)).item(0) / (np.transpose(omega) * dxk).item(0)
        dAk2 = (Ak * domega * np.transpose(domega) * np.transpose(Ak)).item(0) / (
                np.transpose(domega) * Ak * domega).item(0)
        rk = (Ak * domega) / (np.transpose(domega) * Ak * domega).item(0) - dxk / (np.transpose(dxk) * domega).item(0)
        dAk3 = np.transpose(domega) * Ak * domega * rk
        Ak_new = Ak + dAk1 + dAk2 - dAk3
        Ak = Ak_new
        xk = xk_new
        omega = omega_new
        if la.norm(omega) < eps:
            break
        iteration += 1
        if iteration % n == 0:
            Ak = I
    file.close()
    return xk, f(xk), iteration


if __name__ == '__main__':
    print(bfgs_solve([0, 0], 1e-6, 10, 10))
