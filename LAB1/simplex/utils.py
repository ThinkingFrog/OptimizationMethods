def minimizing_index(delta: list, B: list):
    for idx, val in enumerate(delta):
        if idx not in B:
            continue

        min = val
        min_idx = idx

        if min != "inf":
            break

    if min == "inf":
        return min_idx

    for idx, val in enumerate(delta):
        if idx not in B:
            continue

        if val == "inf":
            continue

        if val < min:
            min = val
            min_idx = idx

    return min_idx