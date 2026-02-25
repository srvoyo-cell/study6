#include <cmath>
#include <cstdio>
#include <omp.h>

double term(int k) { return pow(1.0 / k, 2); };

int main() {
  omp_set_num_threads(6);
  const int N = 1000000000;
  double product = 0;
  double t1 = omp_get_wtime();
#pragma omp parallel for reduction(+ : product)
  for (int k = 1; k <= N; ++k) {
    product += term(k);
  }
  double t2 = omp_get_wtime();
  printf("Approximation = %.15f\n", std::sqrt(6.0 * product));
  printf("Time = %lf\n", t2 - t1);
}
