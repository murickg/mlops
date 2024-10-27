from typing import List, Callable
import time
import numpy as np

import traceofmatrix

def test_timings(func: Callable, *args):
    _ = func(*args)
    start_time = time.time()
    _ = func(*args)
    end_time = time.time()
    return round(end_time - start_time, 5)

def compare(matrix_size: int) -> None:
    matrix_a = np.random.rand(matrix_size, matrix_size)
    matrix_b = np.random.rand(matrix_size, matrix_size)

    list_a = matrix_a.tolist()
    list_b = matrix_b.tolist()

    print(
        "Trace of matrix (Pure C++), size={0}x{0}: {1} seconds".format(
            matrix_size, test_timings(traceofmatrix.TraceOfMatrix.traceOfMatrix,
                                      list_a, matrix_size)
        )
    )

    print(
        "Trace of matrix (Python numpy), size={0}x{0}: {1} seconds\n".format(
            matrix_size, test_timings(np.trace, np.array(list_a), matrix_size)
        )
    )

if __name__ == "__main__":
    for size in [10, 50, 100, 300, 500, 700]:
        compare(size)