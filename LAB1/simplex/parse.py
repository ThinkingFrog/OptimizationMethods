from pathlib import Path


def parse(filename: Path):
    signs = [">=", "=", "<="]
    variables = ["x1", "x2", "x3", "x4", "x5"]

    matrix = []
    line_signs = []
    free_vec = []

    var_signs = ["" for _ in variables]
    target = []

    with filename.open("r") as file:
        for lidx, line in enumerate(file):
            line = line.split()
            matrix_line = []

            # Parse line with null inequalities
            if lidx == 5:
                for tidx, token in enumerate(line):
                    if token in signs:
                        var_signs[int(line[tidx - 1][1]) - 1] = token
                continue

            # Parse any other line
            for tidx, token in enumerate(line):
                if token.isdigit():
                    if line[tidx - 1] == "+":
                        matrix_line.append(float(token))
                    else:
                        matrix_line.append(-float(token))

                if token in signs:
                    # If line contains target function
                    if lidx == 6:
                        target += matrix_line
                        target.append(line[tidx + 1])

                    else:
                        line_signs.append(token)
                        free_vec.append(float(line[tidx + 1]))
                        matrix.append(matrix_line)
                    break


    return matrix, line_signs, free_vec, var_signs, target
