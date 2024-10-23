#include "trace_of_matrix.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(trace_core, m) {
    m.doc() = R"doc(Python binding for trace of matrix library)doc";

    py::class_<TraceOfMatrix>(m, "TraceOfMatrix")
        .def_static("traceOfMatrix", &TraceOfMatrix::traceOfMatrix, R"doc(
            Compute Trace of Matrix using pure C++.

            Parametrs:
                a : list of list of float
                    The square matrix.
                N : int
                    The size of square matrix.

            Returns:
                float
                    The trace of square matrix.

        )doc");

}