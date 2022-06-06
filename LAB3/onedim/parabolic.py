from typing import Tuple

from onedim.function import Function


def parabolic(fun: Function, eps: float) -> Tuple[float, float]:
    x1 = fun.x_min
    x2 = (fun.x_max + fun.x_min) / 2
    x3 = fun.x_max

    f1 = fun.func(x1)
    f2 = fun.func(x2)
    f3 = fun.func(x3)

    x_prev = x2

    while True:
        a0 = f1
        a1 = (f2 - f1) / (x2 - x1)
        a2 = (1 / (x3 - x2)) * ((f3 - f1) / (x3 - x1) - (f2 - f1) / (x2 - x1))

        x_ = 0.5 * (x2 + x1 - a1 / a2)
        f_ = fun.func(x_)

        if abs(x_ - x_prev) < eps:
            return x_, f_
        x_prev = x_

        # if x_ is out of bounds
        if x_ < x1:
            x1, x2, x3 = x_, x1, x2
            f1, f2, f3 = f_, x1, x2
            continue

        if x_ > x3:
            x1, x2, x3 = x2, x3, x_
            f1, f2, f3 = f2, f3, f_
            continue
        
        # if x_ is inside bounds
        if x_ < x2:
            xl, xr = x_, x2
            yl, yr = f_, f2
        else:
            xl, xr = x2, x_
            yl, yr = f2, f_

        if yl < yr:
            x1, x2, x3 = x1, xl, xr
            f1, f2, f3 = f1, yl, yr
        else:
            x1, x2, x3 = xl, xr, x3
            f1, f2, f3 = yl, yr, f3


        

class PointValue:
    def __init__(self, x, f_x) -> None:
        self.x = x
        self.y = f_x


def payell_method(fun: Function, eps: float):
    h = 0.1
    x1 = 1
    iter_num = 0
    while 1:
        iter_num += 1
        x2 = x1 + h
        f1 = PointValue(x1, fun.func(x1))
        f2 = PointValue(x2, fun.func(x2))
        x3 = x1 + 2 * h if f1.y > f2.y else x1 - h
        f3 = PointValue(x3, fun.func(x3))
        if f1.y < f2.y and f1.y < f3.y:
            f_min = f1
        elif f1.y < f2.y or f2.y >= f3.y:
            f_min = f3
        else:
            f_min = f2
        a1 = (f2.y - f1.y) / (f2.x - f1.x)
        a2 = 1 / (f3.x - f2.x) * (((f3.y - f1.y) / (f3.x - f1.x)) - ((f2.y - f1.y) / (f2.x - f1.x)))
        x_res = (f2.x - f1.x) / 2 - a1 / 2 * a2
        if abs(x_res - f_min.x) < eps:
            return x_res, fun.func(x_res), iter_num
        else:
            x1 = x_res if fun.func(x_res) < f_min.y else f_min.x
