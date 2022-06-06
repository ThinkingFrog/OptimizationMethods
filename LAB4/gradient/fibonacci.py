import numpy as np
from gradient.function import OneVarFunction

class Fibonacci:
    def seq(self, n: int) -> int:
        if n == 0: 
            return 0
        if n in {1, 2}:
            return 1
        return self.seq(n - 1) + self.seq(n - 2)

    def method(self, func, a, b, eps):
        alpha = 0
        
        while np.sqrt(pow(func._F2(a, b), 2) + pow(func._F1(a, b), 2)) >= eps:
            func_one_var = OneVarFunction(a, b, func._F1(a, b), func._F2(a, b))
            alpha = self.minimize(func_one_var, a, b, eps)
            a, b = a - alpha * func._F1(a, b), b - alpha * func._F2(a, b)
        
        return a, b

    def minimize(self, func: OneVarFunction, a_k, b_k, eps):
        l = b_k - a_k
        alpha = l / 100

        n = 1
        while self.seq(n) <= (b_k - a_k) / eps:
            n += 1

        # k = 1
        lambda_k = a_k + self.seq(n - 2) / self.seq(n) * (b_k - a_k)
        mu_k = a_k + self.seq(n - 1) / self.seq(n) * (b_k - a_k)

        # k <= n - 2
        for k in range(1, n - 1):
            if func.eval(lambda_k) > func.eval(mu_k):
                a_k, b_k, lambda_k = lambda_k, b_k, mu_k
                mu_k = a_k + self.seq(n - k - 1) / self.seq(n - k) * (b_k - a_k)
            else:
                a_k, b_k, mu_k = a_k, mu_k, lambda_k
                lambda_k = a_k + self.seq(n - k - 2) / self.seq(n - k) * (b_k  - a_k)

        # k = n - 1
        lambda_n = lambda_k
        mu_n = lambda_n + alpha

        if func.eval(lambda_n) == func.eval(mu_n):
            a_n = lambda_n
            b_n = b_k
        else:
            a_n = a_k
            b_n = mu_n

        return (a_n + b_n) / 2
