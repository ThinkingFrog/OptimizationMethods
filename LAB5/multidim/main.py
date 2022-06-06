from multidim.restrictions import plot_restrictions
from multidim.zoytendeyk import zoytendeyk, func, rest, slaters_condition, slater_slay, validatex0


def main():
    # plot_restrictions(point_on_boarder=False)
    # plot_restrictions(point_on_boarder=True)

    x0 = [-2, -4]
    x0 = validatex0(x0)

    eta0 = -max(fun(x0) for fun in rest)

    res = zoytendeyk(x0, eta0)
    print(f"Answer: {res}")
    print(f"f(x) = {func(res)}")

    slaters_condition()
    slater_slay()

    return