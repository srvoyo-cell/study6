#include <mpi.h>

#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>

int main(int argc, char** argv) {
  MPI_Init(&argc, &argv);

  int rank = 0;
  int size = 1;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  std::int64_t n_terms = 100000000; // default
  if (argc >= 2) {
    try {
      n_terms = std::stoll(argv[1]);
    } catch (...) {
      if (rank == 0) {
        std::cerr << "Invalid N. Usage: mpirun -np <p> ./main [N]" << std::endl;
      }
      MPI_Finalize();
      return 1;
    }
  }
  if (n_terms < 1) {
    if (rank == 0) {
      std::cerr << "N must be >= 1" << std::endl;
    }
    MPI_Finalize();
    return 1;
  }

  // Split [1..n_terms] into contiguous chunks
  std::int64_t base = n_terms / size;
  std::int64_t rem = n_terms % size;

  std::int64_t local_n = base + (rank < rem ? 1 : 0);
  std::int64_t start = rank * base + (rank < rem ? rank : rem) + 1;
  std::int64_t end = start + local_n - 1;

  double t0 = MPI_Wtime();

  double local_sum = 0.0;
  for (std::int64_t i = start; i <= end; ++i) {
    double x = static_cast<double>(i);
    local_sum += 1.0 / (x * x);
  }

  double global_sum = 0.0;
  MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  double t1 = MPI_Wtime();
  double local_time = t1 - t0;
  double max_time = 0.0;
  MPI_Reduce(&local_time, &max_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    double pi_est = std::sqrt(6.0 * global_sum);
    double pi_true = std::acos(-1.0);

    std::cout << std::setprecision(15);
    std::cout << "N=" << n_terms << " processes=" << size << "\n";
    std::cout << "zeta(2) ~ " << global_sum << "\n";
    std::cout << "pi ~ " << pi_est << "\n";
    std::cout << "abs error = " << std::fabs(pi_est - pi_true) << "\n";
    std::cout << "time (max over ranks) = " << max_time << " s\n";
  }

  MPI_Finalize();
  return 0;
}
