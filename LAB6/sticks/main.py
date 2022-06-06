import math
import numpy

from scipy.optimize import linprog


def main():
    with open("output/matrix.txt", "r") as matrix_file:
        matrix = [[int(num) for num in line.split()] for line in matrix_file]
    print(f"Matrix columns: {len(matrix[0])}")

    with open("output/free_vector.txt", "r") as free_vec_file:
        free_vec = [[int(num) for num in line.split()] for line in free_vec_file]

    with open("output/target_func.txt", "r") as target_func_file:
        target_func = [[float(num) for num in line.split()] for line in target_func_file]

    solution = linprog(c=target_func, A_eq=matrix, b_eq=free_vec, method='simplex').x

    np_matrix = numpy.matrix(matrix)
    print(f"Matrix rank: {numpy.linalg.matrix_rank(np_matrix)}")

    not_zero = []
    sum = 0
    for idx, num in enumerate(solution):
        if num != 0:
            not_zero.append([list(map(lambda x: -x, numpy.array(matrix)[:, idx])), math.ceil(num)])
            sum += math.ceil(num)
    print(f"Non-zero solutions: {not_zero}")
    print(f"Summary: {sum}")