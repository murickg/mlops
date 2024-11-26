CXX=g++
CXXFLAGS=-std=c++14 -O3 -march=native -Wall -I$(SRC_DIR) $(shell python3 -m pybind11 --includes)
PY_LDFLAGS=$(shell python3-config --ldflags) -shared -fPIC -undefined dynamic_lookup
GTEST_FLAGS=-lgtest -lgtest_main -pthread
LDFLAGS=-lopenblas
SRC_DIR=traceofmatrix/src
TESTS_DIR=traceofmatrix/tests
PYTHON_DIR=traceofmatrix/python

all: traceofmatrix test

TraceOfMatrix: $(PYTHON_DIR)/binding.o $(SRC_DIR)/trace_of_matrix.o
	$(CXX) $^ -o $(PYTHON_DIR)/trace_core`python3-config --extension-suffix` $(PY_LDFLAGS) $(CXXFLAGS)

$(PYTHON_DIR)/binding.o: $(PYTHON_DIR)/binding.cpp $(SRC_DIR)/trace_of_matrix.h
	$(CXX) $(CXXFLAGS) -fPIC -c $< -o $@

$(SRC_DIR)/trace_of_matrix.o: $(SRC_DIR)/trace_of_matrix.cpp $(SRC_DIR)/trace_of_matrix.h
	$(CXX) $(CXXFLAGS) -fPIC -c $< -o $@

test: $(TESTS_DIR)/test_trace.o $(SRC_DIR)/trace_of_matrix.o
	$(CXX) $^ -o $(TESTS_DIR)/test_trace $(GTEST_FLAGS)

$(TESTS_DIR)/test_trace.o: $(TESTS_DIR)/test_trace.cpp $(SRC_DIR)/trace_of_matrix.h
	$(CXX) $(CXXFLAGS) -c $< -o $@

run_tests: test
	./$(TESTS_DIR)/test_trace

clean:
	rm -f $(PYTHON_DIR)/*.o $(SRC_DIR)/*.o $(TESTS_DIR)/*.o $(PYTHON_DIR)/trace_core`python3-config --extension-suffix` $(TESTS_DIR)/test_trace