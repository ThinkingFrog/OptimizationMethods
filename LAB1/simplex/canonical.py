def append_member(matrix: list, sign_pos: int, value: int, target: list):
    for i in range(len(matrix)):
        if i == sign_pos:
            matrix[i].append(value)
        else:
            matrix[i].append(0)
    target.insert(len(target) - 1, 0)


def to_canon(matrix: list, matrix_signs: list, free_members: list, members_signs: list, target: list):
    num_members = len(target) - 1
    num_basic = list(range(num_members))
    for pos in range(len(members_signs)):
        if members_signs[pos] == "<=":
            for item in matrix:
                item[pos] = -item[pos]
            target[pos] = -target[pos]

        if members_signs[pos] == "":
            for item_ in matrix:
                item_.append(item_[pos])
                item_.append(-item_[pos])
            target.insert(len(target) - 1, target[pos])
            target.insert(len(target) - 1, -target[pos])

            for item__ in matrix:
                item__.pop(pos)
            target.pop(pos)
            num_basic.append(len(target) - 2)

    for i in range(len(matrix_signs)):
        if matrix_signs[i].count("<=") != 0:
            append_member(matrix, i,  1, target)
        if matrix_signs[i].count(">=") != 0:
            append_member(matrix, i, -1, target)

    num_not_basic = [
        i + len(num_basic) for i in range(len(target) - 1 - len(num_basic))
    ]

    for i in range(len(matrix_signs)):
        matrix_signs[i] = "="

    for i in range(len(members_signs)):
        members_signs[i] = ">="
    members_signs.extend(">=" for _ in range(len(target) - len(members_signs) - 1))
    return num_basic, num_not_basic, matrix, free_members, target, 0