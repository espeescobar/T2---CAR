#include <vector>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <omp.h>

struct MatView {
    double* data;
    int stride;
    int size;
    double& at(int i, int j) const { return data[i * stride + j]; }
    MatView sub(int r, int c, int s) const { return { data + r * stride + c, stride, s }; }
};

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

void multiply_leaf(const MatView& A, const MatView& B, const MatView& C) {
    int s = C.size;
    for (int i = 0; i < s; ++i) {
        for (int k = 0; k < s; ++k) {
            double a = A.at(i, k);
            for (int j = 0; j < s; ++j) {
                C.at(i, j) += a * B.at(k, j);
            }
        }
    }
}

void multiply_rec_omp(const MatView& A, const MatView& B, const MatView& C, int n) {
    int s = C.size;
    if (s <= n) {
        multiply_leaf(A, B, C); 
        return;
    }
    int h = s / 2;
    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(0, 0, h), B.sub(0, 0, h), C.sub(0, 0, h), n); // C11
    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(0, 0, h), B.sub(0, h, h), C.sub(0, h, h), n); // C12
    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(h, 0, h), B.sub(0, 0, h), C.sub(h, 0, h), n); // C21
    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(h, 0, h), B.sub(0, h, h), C.sub(h, h, h), n); // C22
    
    #pragma omp taskwait 

    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(0, h, h), B.sub(h, 0, h), C.sub(0, 0, h), n); // C11
    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(0, h, h), B.sub(h, h, h), C.sub(0, h, h), n); // C12
    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(h, h, h), B.sub(h, 0, h), C.sub(h, 0, h), n); // C21
    #pragma omp task shared(A, B, C)
    multiply_rec_omp(A.sub(h, h, h), B.sub(h, h, h), C.sub(h, h, h), n); // C22
    
    #pragma omp taskwait
}

int main(int argc, char** argv) {
    int N = (argc > 1) ? std::atoi(argv[1]) : 2048; 
    int n = (argc > 2) ? std::atoi(argv[2]) : 128;  
    int p = (argc > 3) ? std::atoi(argv[3]) : 1;    

    omp_set_num_threads(p);

    std::vector<double> A(N * N), B(N * N), C(N * N, 0.0);
    init_matrix(A, N, 1);
    init_matrix(B, N, 2);
    MatView Av{ A.data(), N, N }, Bv{ B.data(), N, N }, Cv{ C.data(), N, N }; //[cite: 1]

    auto t0 = std::chrono::high_resolution_clock::now();
    
    #pragma omp parallel
    {
        #pragma omp single
        {
            multiply_rec_omp(Av, Bv, Cv, n);
        }
    }
    
    auto t1 = std::chrono::high_resolution_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    double checksum = 0.0;
    for (double v : C) {
        checksum += v;
    }
    std::printf("N=%d n=%d p=%d tiempo=%.2f ms checksum=%.6f\n", N, n, p, ms, checksum);
    return 0;
}