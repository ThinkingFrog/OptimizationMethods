def to_dual_task(matrix: list, matrix_signs: list, free_members: list, members_signs: list, target: list):
    dual_matrix = [list(i) for i in zip(*matrix)]
    dual_free_members = list(target)
    dual_free_members.pop()
    dual_target = list(free_members)
    dual_target.append("max")

    dual_matrix_signs = []
    for members_sign in members_signs:
        if members_sign == "":
            dual_matrix_signs.append("=")
        elif members_sign == ">=":
            dual_matrix_signs.append("<=")
        else:
            dual_matrix_signs.append(">=")

    dual_members_signs = []
    for matrix_sign in matrix_signs:
        if matrix_sign == ">=":
            dual_members_signs.append(">=")
        elif matrix_sign == "=":
            dual_members_signs.append("")
        else:
            dual_members_signs.append("<=")

    return dual_matrix, dual_matrix_signs, dual_free_members, dual_members_signs, dual_target
