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

    def _det(self, F11: float, F12: float, F21: float, F22: float) -> float:
        return F11 * F22 - F21 * F12

    def _F1(self, x1: float, x2: float) -> float:
        return 12 * (x1 / np.sqrt(1 + 3 * x1 ** 2 + x2 ** 2)) + 4

    def _F2(self, x1: float, x2: float) -> float:
        return 4 * (x2 / np.sqrt(1 + 3 * x1 ** 2 + x2 ** 2)) + 1


