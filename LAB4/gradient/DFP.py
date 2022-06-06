import numpy as np
import matplotlib.pyplot as plot

def coefs():
    return 4,3,1

def f(x):
    a, b, c = coefs()
    return a * x[0] + x[1] + 4 * np.sqrt(1 + b * x[0] ** 2 + c * x[1] ** 2)

def grad_f(x):
    a, b, c = coefs()
    return np.asarray([a + 4 * b * x[0] / np.sqrt(1 + b * x[0] ** 2 + c * x[1] ** 2),
                 1 + 4 * c * x[1] / np.sqrt(1 + b * x[0] ** 2 + c * x[1] ** 2)])

def norm(x):
    return float('inf') if x is None else np.sqrt(x[0] ** 2 + x[1] ** 2)

def fib(n):
    numbers = [1, 1]
    for i in range(2, n):
        num = numbers[i - 2] + numbers[i - 1]
        numbers.append(num)
    return numbers

def fib_min(nums, x_k, grad_k):
    a = 0
    b = 1
    lam = a + nums[-3] / nums[-1] * (b - a)
    mu = a + nums[-2] / nums[-1] * (b - a)
    f_lam = f(x_k - lam * grad_k)
    f_mu = f(x_k - mu * grad_k)
    for i in range(1, len(nums)):
        if f_lam > f_mu:
            a = lam
            lam = mu
            mu = a + nums[-1 - i - 1] / nums[-1 - i] * (b - a)
            if i == len(nums) - 3:
                break
            f_lam = f_mu
            f_mu = f(x_k - mu * grad_k)
        else:
            b = mu
            mu = lam
            lam = a + nums[-1 - i - 2] / nums[-1 - i] * (b - a)
            if i == len(nums) - 3:
                break
            f_mu = f_lam
            f_lam = f(x_k - lam * grad_k)
    return (lam + b) / 2 if f_lam >= f_mu else (a + mu) / 2

class Solver:
    x: list
    iters = 0
    fib_iter_num = 20

    def __init__(self):
        self.x = []

    def get_x_seq(self):
        return self.x.copy()

    def get_iter_num(self):
        return self.iters

    def draw_contoures(self):
        fig, axis = plot.subplots()
        x = np.ndarray((1,len(self.x)))
        y = np.ndarray((1,len(self.x)))
        for i in range(len(self.x)):
            x[0, i] = self.x[i][0]
            y[0, i] = self.x[i][1]
        x_mesh_min = np.min(x)
        x_mesh_max = np.max(x)
        x_mesh_delta = (x_mesh_max - x_mesh_min) / 10
        x_mesh_min -= x_mesh_delta
        x_mesh_max += x_mesh_delta
        y_mesh_min = np.min(y)
        y_mesh_max = np.max(y)
        y_mesh_delta = (y_mesh_max - y_mesh_min) / 10
        y_mesh_min -= y_mesh_delta
        y_mesh_max += y_mesh_delta
        mesh_dest = max(x_mesh_max - x_mesh_min, y_mesh_max - y_mesh_min)
        x_mesh_max = x_mesh_min + mesh_dest
        y_mesh_max = y_mesh_min + mesh_dest
        x_mesh, y_mesh = np.mgrid[x_mesh_min:x_mesh_max:100j, y_mesh_min:y_mesh_max:100j]
        z = np.ndarray(x_mesh.shape)
        for i in range(x_mesh.shape[0]):
            for j in range(x_mesh.shape[1]):
                z[i,j] = f((x_mesh[i,j], y_mesh[i,j]))
        cs = axis.contour(x_mesh, y_mesh, z, levels=15)
        axis.plot(x.tolist()[0], y.tolist()[0],  'bX--')
        axis.clabel(cs, colors="black")
        fig.set_figwidth(8)
        fig.set_figheight(8)
        return fig, axis


class FastestDesc(Solver):
    def __init__(self):
        super(FastestDesc, self).__init__()

    def get_solution(self, x_0, eps):
        self.x = [np.asarray(x_0)]
        self.iters = 0
        fib_nums = fib(self.fib_iter_num)
        grad = None
        while norm(grad) >= eps:
            grad = grad_f(self.x[-1])
            alpha = fib_min(fib_nums, self.x[-1], grad)
            self.x.append(self.x[-1] - alpha * grad)
            self.iters += 1
            print("x1 = ", self.x[-1][0], "x2 = ", self.x[-1][1])
            print("step =", alpha)
        return self.x[-1]

class DFP(Solver):
    def __init__(self):
        super().__init__()

    def refresh_matrix(self, A):
        dx = self.x[-1] - self.x[-2]
        dw = grad_f(self.x[-2]) - grad_f(self.x[-1])
        return A - np.outer(dx, dx) / np.dot(dw, dx) - A.dot(np.outer(dw, dw)).dot(A.transpose()) / (np.dot(dw, A.dot(dw)))

    def get_solution(self, x_0, eps):
        self.x = [np.asarray(x_0)]
        self.iters = 0
        fib_nums = fib(self.fib_iter_num)
        grad = None
        A = np.eye(2)
        while norm(grad) >= eps:
            grad = grad_f(self.x[-1])
            p = A.dot(grad)
            alpha = fib_min(fib_nums, self.x[-1], p)
            self.x.append(self.x[-1] - alpha * p)
            self.iters += 1
            if self.iters % 2 == 0:
                A = self.refresh_matrix(A)
            print("x1 = ", self.x[-1][0],"x2 = ", self.x[-1][1] )
            print("step =", alpha)
        return self.x[-1]
