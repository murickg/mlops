#include "trace_of_matrix.h"
#include <iostream>
#include <vector>

double TraceOfMatrix::traceOfMatrix(const std::vector<std::vector<double>> &a, int N) {
    double result = 0;
    for (int i = 0; i < N; i++) {
        result += a[i][i];
    }
    return result;
}