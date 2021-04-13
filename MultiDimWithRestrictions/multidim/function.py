import pylab
import matplotlib.pyplot as plt
import numpy as np


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
        pylab.title("Линии уровня функции" + self.func_str)
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


class OneVarFunction:
    def __init__(self, x_0, x_1, grad_0, grad_1) -> None:
        self._x_0 = x_0
        self._x_1 = x_1
        self._grad_0 = grad_0
        self._grad_1 = grad_1

    def eval(self, x: float) -> float:
        return -x * (4 * self._grad_0 + self._grad_1) + 4 * self._x_0 + self._x_1 + np.sqrt(pow(x, 2) * (3 * pow(self._grad_0, 2) + pow(self._grad_1, 2)) \
        - 2 * x * (3 * self._x_0 * self._grad_0 + self._x_1 * self._grad_1) + 1 + 3 * pow(self._x_0, 2) + pow(self._x_1, 2))