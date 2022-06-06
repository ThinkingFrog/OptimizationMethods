import pylab
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import math


class Function:
    def __init__(self) -> None:
        self.pointsX = None
        self.pointsY = None
        self.func_str = "$4x_1+x_2+4\sqrt{1+3x_1^2+x_2^2}$"
        self.iter = 0

    def f(self, x1: float, x2: float) -> float:
        return 4 * x1 + x2 + 4 * np.sqrt(1 + 3 * x1 ** 2 + x2 ** 2)

    def plot_lines(self) -> None:
        x = np.arange(-1, 0.5, 0.05)
        y = np.arange(-1, 0.5, 0.05)
        xgrid, ygrid = np.meshgrid(x, y)

        zgrid = 4 * xgrid + ygrid + 4 * np.sqrt(1 + 3 * xgrid ** 2 + ygrid ** 2)

        cs = pylab.contour(xgrid, ygrid, zgrid, 15)
        pylab.plot(self.pointsX, self.pointsY, 'bX--')
        pylab.clabel(cs, colors="black")
        pylab.xlabel("x1")
        pylab.ylabel("x2")
        pylab.title(f"Линии уровня функции{self.func_str}")
        pylab.show()

    def set_points(self, res):
        x = []
        y = []
        for el in res:
            x.append(el[0])
            y.append(el[1])
        self.pointsX = x
        self.pointsY = y

    def plot(self)->None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        x1, x2 = np.meshgrid(np.linspace(-2, 1, 100), np.linspace(-2, 1, 100))
        z = 4 * x1 + x2 + 4 * np.sqrt(1 + 3 * x1 ** 2 + x2 ** 2)

        ax.plot_surface(x1, x2, z)

        plt.show()


    def newton(self, x_start: np.array = np.array([-0.5, 0.25]), eps = 0.01) -> List[np.array]:
        x1 = x_start[0]
        x2 = x_start[1]
        res = [x_start]

        F1 = self._F1(x1, x2)
        F2 = self._F2(x1, x2)
        self.iter = 0
        while np.sqrt(pow(F2, 2) + pow(F1, 2)) >= eps:
            self.iter += 1
            F11, F12, F21, F22 = self._hesse_coef(x1, x2)
            detH = self._det(F11, F12, F21, F22)
            F1 = self._F1(x1, x2)
            F2 = self._F2(x1, x2)
            x1 = x1 - 1 / detH * (F22 * F1 - F21 * F2)
            x2 = x2 - 1 / detH * (F11 * F2 - F12 * F1)
            print("x1 = ", x1, "x2 = ", x2)
            res.append(np.array([x1, x2]))

        return res


    def _hesse_coef(self, x1: float, x2: float):
        F11 = -36 * pow(x1, 2) / pow((1 + 3 * pow(x1, 2) + pow(x2, 2)), 1.5) + 12 / np.sqrt(
            1 + 3 * pow(x1, 2) + pow(x2, 2))
        F12 = -12 * x1 * (x2 / pow((1 + 3 * pow(x1, 2) + pow(x2, 2)), 1.5))
        F21 = -12 * x1 * (x2 / pow((1 + 3 * pow(x1, 2) + pow(x2, 2)), 1.5))
        F22 = -4 * pow(x2, 2) / pow((1 + 3 * pow(x1, 2) + pow(x2, 2)), 1.5) + 4 / np.sqrt(1 + 3 * (x1 ** 2) + x2 ** 2)
        return F11, F12, F21, F22

    def _det(self, F11: float, F12: float, F21: float, F22: float) -> float:
        return F11 * F22 - F21 * F12

    def _F1(self, x1: float, x2: float) -> float:
        return 12 * (x1 / np.sqrt(1 + 3 * x1 ** 2 + x2 ** 2)) + 4

    def _F2(self, x1: float, x2: float) -> float:
        return 4 * (x2 / np.sqrt(1 + 3 * x1 ** 2 + x2 ** 2)) + 1


class OneVarFunction:
    def __init__(self, x_0, x_1, grad_0, grad_1) -> None:
        self._x_0 = x_0
        self._x_1 = x_1
        self._grad_0 = grad_0
        self._grad_1 = grad_1

    def eval(self, x: float) -> float:
        return -x * (4 * self._grad_0 + self._grad_1) + 4 * self._x_0 + self._x_1 + np.sqrt(pow(x, 2) * (3 * pow(self._grad_0, 2) + pow(self._grad_1, 2)) \
        - 2 * x * (3 * self._x_0 * self._grad_0 + self._x_1 * self._grad_1) + 1 + 3 * pow(self._x_0, 2) + pow(self._x_1, 2))