"""Refer to vec_cos_collections.py for caomparisons
of various implementations.
"""
import numpy
from numpy import inner
from numpy.linalg import norm


def vec_cos(vec1, vec2):
    """inner norm"""
    if isinstance(vec1, numpy.ndarray) and len(vec1.shape) > 1:
        vec1 = list(vec1[0])
    if isinstance(vec2, numpy.ndarray) and len(vec1.shape) > 1:
        vec2 = list(vec2[0])

    if vec1 is None or vec2 is None:
        return 0.0

    norm1 = norm(vec1)
    norm2 = norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0

    return inner(vec1, vec2) / (norm(vec1) * norm(vec2))


def main():
    """main"""
    # import random
    import timeit

    # 100: vec_cos0
    dim = 1000
    dim = 100
    dim = 500

    number = 100000
    print("dim: %s" % dim)
    funcs = [
        "vec_cos",
    ]

    for func in funcs:
        setup = "from vec_cos import %s; " % func
        setup += "import random; "
        setup += "u = [random.random() for i in range(%s)]; " % dim
        setup += "v = [random.random() for i in range(%s)]; " % dim
        stmt = "%s(u, v)" % func
        # print(stmt)
        # print(setup)
        time_ = (
            timeit.timeit(stmt=stmt, setup=setup, number=number) / number * 10**6
        )  # noqa

        print("%s: %.2f us" % (func, time_))


if __name__ == "__main__":
    main()
