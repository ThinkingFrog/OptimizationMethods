from typing import List
from scipy.optimize import linprog, OptimizeWarning

import numpy as np
import warnings

warnings.simplefilter("error", OptimizeWarning)

func = lambda x: 4 * x[0] + x[1] + 4 * np.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2)
func_grad = lambda x: [12 * (x[0] / np.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2)) + 4,
                       4 * (x[1] / np.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2)) + 1]

rest = [
    lambda x: x[0],
    lambda x: x[1],
    lambda x: x[0] - 2 * x[1] - 1,
    lambda x: -x[0] - x[1] - 1#0.7504
]

rest_grads = [
    lambda x: [1, 0],
    lambda x: [0, 1],
    lambda x: [1, -2],
    lambda x: [-1, -1]
]


def validatex0(x0):
    eta = max(r(x0) for r in rest)
    if eta < 0:
        return x0

    valid = False
    while not valid:
        delta = -eta
        res = simplex(x0, delta)
        s, eta = res.x[:2], res.fun

        valid = False
        alpha = 1

        while not valid:
            valid = func(x0 + alpha * s) <= func(x0) + 0.5 * eta * alpha

            for r in rest:
                valid = valid and r(x0 + alpha * s) <= 0
                if not valid:
                    break

            if not valid:
                alpha *= 0.5
                if alpha < pow(2, -10):
                    alpha = 0.5
                    break

        x0 += alpha * s
        print(f"x0: {x0}")

    return x0


def slaters_condition():
    print('\nПроверка условия Слейтера ----> решим задачу минимизации')
    A = np.array([[1, 0], [0, 1], [1, -2], [-1, -1]])
    b = np.array([0, 0, 0, 0])
    c = np.array([1, 1])
    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))
    print('=>\nНайденная точка: x=', res.x)

    print('\nПроверка условия Слейтера ----> решим задачу минимизации\n(граничные условия)')
    A = np.array([[1, 0], [0, 1], [1, -2], [-1, -1]])
    b = np.array([0, 0, 1, 0.7504])
    c = np.array([1, 1])
    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))
    print('=>\nНайденная точка: x=', res.x)


def slater_slay():
    print('\nПроверка условия Слейтера ----> решим СЛАУ:')
    print("x1 <= 0\nx2 <= 0\nx1 - 2x2 - 1<= 0\n-x1 - x2 - 1 <= 0\n=>\nНайденная точка: x = [0,0]")


def get_bounds(x, delta):
    return [idx for idx in range(len(rest)) if -delta <= rest[idx](x) <= 0.0]


def get_step(x, eta, s):
    alpha = 1
    while True:
        first_eq = func([x_k + alpha * s_k for x_k, s_k in zip(x, s)]) - func(x) <= 0.5 * eta * alpha

        second_eq = True
        for r in rest:
            second_eq = second_eq and (r([x_k + alpha * s_k for x_k, s_k in zip(x, s)]) <= 0)

        if first_eq and second_eq:
            return alpha
        alpha *= 0.5


def simplex(x_k, d_k):
    bounds_idxs = get_bounds(x_k, d_k)

    A_ub = np.zeros(shape=(1 + len(bounds_idxs), 3))
    A_ub[:, 2] = -1
    A_ub[0, 0:2] = func_grad(x_k)

    for j, i in enumerate(bounds_idxs, start=1):
        A_ub[j, 0:2] = rest_grads[i](x_k)
    c = np.zeros(3)
    c[2] = 1

    b_ub = np.zeros(A_ub.shape[0])
    bounds = [[-1, 1], [-1, 1], [None, None]]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')


def zoytendeyk(x0: List[float], eta: int) -> List[float]:
    # Начальный этап
    alpha = 1
    lam = 0.5
    delta = -eta
    x = x0

    iter = -1

    # Основной этап
    while True:
        iter += 1

        *s, eta = simplex(x, delta).x

        if eta < delta:
            alpha = get_step(x, eta, s)
            x = [x_k + alpha * s_k for x_k, s_k in zip(x, s)]
        else:
            delta *= lam

        print(f"iter: {iter} - x: {x}")  # - delta: {delta} - eta: {eta} - f(x): {func(x)}")

        if delta < -max(r(x) for r in rest) and abs(eta) < 1e-5:
            break

    return x
