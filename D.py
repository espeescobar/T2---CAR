# D.py - Algoritmo 1 en Python con Numba (prange).
# Uso: python3 D.py [N p]
import os
import sys
import time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
p = int(sys.argv[2]) if len(sys.argv) > 2 else 1
# Permite p > n. de cores (se fija antes de importar numba)
os.environ.setdefault("NUMBA_NUM_THREADS", str(max(p, os.cpu_count() or 1)))

import numpy as np  # noqa: E402
import numba  # noqa: E402
from numba import njit, prange  # noqa: E402


def init_matrix(n, offset):
    # Mismos valores que serial.cpp
    i = np.arange(n).reshape(-1, 1)
    j = np.arange(n).reshape(1, -1)
    return np.sin(i * 0.1 + j * 0.3 + offset)


@njit(parallel=True)
def multiply_alg1(A, B, C):
    # prange reparte las filas de C entre hilos
    n = A.shape[0]
    for i in prange(n):
        for k in range(n):
            a = A[i, k]
            for j in range(n):
                C[i, j] += a * B[k, j]


@njit
def checksum(C):
    # Suma secuencial, igual que en C++
    s = 0.0
    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            s += C[i, j]
    return s


def main():
    numba.set_num_threads(p)
    A, B = init_matrix(N, 1.0), init_matrix(N, 2.0)

    # Warm-up: compila JIT fuera de la medicion
    w = np.zeros((64, 64))
    t0 = time.perf_counter()
    multiply_alg1(w, w, w.copy())
    checksum(w)
    jit_ms = (time.perf_counter() - t0) * 1e3

    C = np.zeros((N, N))
    t0 = time.perf_counter()
    multiply_alg1(A, B, C)
    ms = (time.perf_counter() - t0) * 1e3

    print(f"N={N} p={p} tiempo={ms:.2f} ms checksum={checksum(C):.6f} jit={jit_ms:.2f} ms")


if __name__ == "__main__":
    main()
