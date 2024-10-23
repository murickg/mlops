#include "trace_of_matrix.h"
#include <gtest/gtest.h>

TEST(LinearAlgebraTests, DotProductBlas) {
  std::vector<std::vector<double>> a = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
  std::vector<std::vector<double>> b = {
        {1, 2, 3, 4},
        {4, 5, 6, 7},
        {7, 8, 9, 10},
        {1.2, 1.4, 1.6, 1.8}
    };
  std::vector<std::vector<double>> c = {
        {10.2, 12},
        {24, 5.162},
    };
  EXPECT_DOUBLE_EQ(15.0, TraceOfMatrix::traceOfMatrix(a, 3));
  EXPECT_DOUBLE_EQ(16.8, TraceOfMatrix::traceOfMatrix(a, 4));
  EXPECT_DOUBLE_EQ(15.362, TraceOfMatrix::traceOfMatrix(a, 2));
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}