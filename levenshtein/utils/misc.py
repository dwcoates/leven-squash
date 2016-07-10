import math


def nCr(n, r):
    f = math.factorial
    if n < r:
        return 0
    return f(n) / f(r) / f(n - r)
