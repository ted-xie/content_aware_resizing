def CLAMP_RANGE(x, min_x, max_x):
    if x < min_x:
        return min_x
    if x > max_x:
        return max_x
    return x
