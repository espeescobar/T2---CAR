# Tarea 2 — CAR (IIC3533)

Multiplicación de matrices C = A·B con OpenMP y Numba.

| Ítem | Archivo | Qué hace |
|---|---|---|
| (a) | `serial.cpp`, `graficoA.py` | Versión serial y tiempo según el bloque n |
| (b) | `B.cpp` | Alg. 1: `omp parallel for` sobre las filas de C |
| (c) | `C.cpp` | Alg. 2: dividir y conquistar con `omp task` |
| (d) | `D.py` | Alg. 3: Alg. 1 en Python con Numba `prange` |
| (e), (f) | `correr.py`, `graficos.py` | Mide B, C y D con p ∈ {1,2,4,8} y N ∈ {1024,2048,4096}; grafica T, S y E |
| (g) | `correr.py` en otro computador | `graficos.py` compara ambos computadores |

Los resultados de (a)–(c) están en `Resultados.md`.

## Requisitos
- Linux/WSL: `g++` con OpenMP. En macOS: `brew install libomp`.
- Python 3: `pip install numpy numba pandas matplotlib`

## Cómo correr (d)–(g)
```bash
python3 correr.py <maquina>   # compila con -O3 -march=native -fopenmp y mide todo
python3 graficos.py           # figuras E_, F_, G_ y tablas_<maquina>.md
```
- `correr.py` guarda `resultados_<maquina>.csv` (una fila por corrida) y `maquina_<maquina>.txt` (cores y reloj, para (g)).
- Cada corrida se verifica contra el checksum de `serial` con n = N (columna `ok`).
- Opciones: `--reps 3` (repeticiones; con N = 4096 se hacen 2), `--n 128` (hoja del Alg. 2) y `--Ns 1024 2048 4096`.
- Para (g), corre `correr.py` en el segundo computador con otro nombre y luego `graficos.py` con ambos CSV en la carpeta.
