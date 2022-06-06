from itertools import combinations
import numpy as np


def get_bases_matrix(matrix: np.ndarray):
    all_bases_matrix = []
    combination = []
    indexes = list(range(matrix.shape[1]))

    for i in combinations(indexes, matrix.shape[0]):
        bases_matrix = matrix[:, i]
        if np.linalg.det(bases_matrix) != 0:
            all_bases_matrix.append(bases_matrix)
            combination.append(i)

    return all_bases_matrix, combination


def get_bases(matrix: list, free_members: list):
    bases = []
    if len(matrix) >= len(matrix[0]):
        return []
    bases_matrix, indexes = get_bases_matrix(np.array(matrix))

    for i in range(len(bases_matrix)):
        result = np.linalg.solve(bases_matrix[i], free_members)
        if len(result[result < 0]) != 0:
            continue
        if len(result[result > 1e+16]) != 0:
            continue

        base = [0 for _ in range(len(matrix[0]))]
        for j in range(len(indexes[i])):
            base[indexes[i][j]] = result[j]
        bases.append(base)
    return bases


def brute_force(matrix: list, free_members: list, target: list):
    if target[-1] == "max":
        for i in range(len(target) - 1):
            target[i] = -target[i]
    target.pop()

    bases = get_bases(matrix, free_members)
    if len(bases) == 0:
        return []

    result = bases[0]
    for i in range(len(bases)):
        if np.dot(bases[i], target) < np.dot(result, target):
            result = bases[i]

    return result
