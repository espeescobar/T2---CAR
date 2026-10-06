#include <vector>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <omp.h> 
double det_value(int i, int j, double offset) {
    return std::sin(i * 0.1 + j * 0.3 + offset);
}

void init_matrix(std::vector<double>& M, int N, double offset) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            M[i * N + j] = det_value(i, j, offset);
        }
    }
}

void multiply_alg1(const std::vector<double>& A, const std::vector<double>& B, std::vector<double>& C, int N) {
    #pragma omp parallel for
    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < N; ++k) {
            for (int j = 0; j < N; ++j) {
                C[i * N + j] += A[i * N + k] * B[k * N + j];
            }
        }
    }
}

int main(int argc, char** argv) {
    int N = (argc > 1) ? std::atoi(argv[1]) : 2048;
    int p = (argc > 2) ? std::atoi(argv[2]) : 1; 

    omp_set_num_threads(p);

    std::vector<double> A(N * N), B(N * N), C(N * N, 0.0);
    init_matrix(A, N, 1);
    init_matrix(B, N, 2);

    auto t0 = std::chrono::high_resolution_clock::now();
    multiply_alg1(A, B, C, N);
    auto t1 = std::chrono::high_resolution_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    double checksum = 0.0;
    for (double v : C) {
        checksum += v;
    }
    
    std::printf("N=%d p=%d tiempo=%.2f ms checksum=%.6f\n", N, p, ms, checksum);
    return 0;
}