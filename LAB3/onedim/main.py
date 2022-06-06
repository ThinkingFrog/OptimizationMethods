from onedim.function import Function
from onedim.dichotomy_method import dichotomy_method
from onedim.parabolic import parabolic
from onedim.parabolic import payell_method
from onedim.dichotomy_method import theoretical_assessment


def main():
    eps_list = [0.1, 0.01, 0.001]
    my_fun = Function()
    print(f"Function: {my_fun.func_str}" + '\n')
    for eps in eps_list:
        print("eps = ", eps)

        print("Dichotomy method results:")
        x_d, f_d, iterations = dichotomy_method(my_fun, eps)
        print("x = ", x_d)
        print("f(x) = ", f_d)

        print("Number of function call:")
        print("\t theoretical  = " + str(theoretical_assessment(my_fun, eps)))
        print("\t practical = " + str(my_fun.count - 1))
        my_fun.count = 0

        print("\nParabolic method results:")
        x_p, f_p = parabolic(my_fun, eps)
        print("x = ", x_p)
        print("f(x) = ", f_p)
        print("\t practical = " + str(my_fun.count - 1))
        my_fun.count = 0

        print("\n")

    my_fun.plot_func()
    # print(payel_method(my_fun, 0.001))
