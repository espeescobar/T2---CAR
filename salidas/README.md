# Salidas ya medidas

Resultados del código del repo medidos el 15/10 en dos computadores. Sirven para el informe sin compilar ni correr nada. Ambos compilados con `g++ -O3 -march=native -fopenmp`.

| Computador | Detalle |
|---|---|
| `MacBookM2` | MacBook Air M2, VM Linux con 4 vCPU |
| `Xeon` | Intel Xeon @ 2,10 GHz, 2 vCPU, 1 hilo por core |

Cada computador tiene estos archivos (`<maq>` = `MacBookM2` o `Xeon`):

| Archivo | Ítem | Contenido |
|---|---|---|
| `salida_serial_<maq>.txt` | (a) | Lo que imprime `./serial N n`: barrido de n con N = 2048 y referencias de `correr.py` |
| `salida_B_<maq>.txt` | (b) | Lo que imprime `./B N p` en cada corrida |
| `salida_C_<maq>.txt` | (c) | Lo que imprime `./C N n p` en cada corrida |
| `salida_D_<maq>.txt` | (d) | Lo que imprime `python3 D.py N p` (sin el campo `jit`, que no queda en el CSV) |
| `resultados_<maq>.csv` | (b)–(f) | CSV de `correr.py`: una fila por corrida, `ok` verifica el checksum |
| `a_serial_<maq>.csv` | (a) | Tiempos de `serial` con N = 2048 y n de 2048 a 32 |
| `tablas_<maq>.md` | (e), (f) | Tablas T, S, E y eficiencia débil de `graficos.py` |
| `E_<maq>.png` | (e) | T(p), S(p) y E(p) con N = 2048 |
| `E_bloques_<maq>.png` | (e) | Alg. 2 según el bloque n |
| `F_<maq>.png` | (f) | E(p) con N = 1024, 2048 y 4096 |
| `maquina_<maq>.txt` | (g) | Cores y reloj (`lscpu`) |

Archivos comunes:
- `A_bloques.png`: (a), tiempo serial según n en ambos computadores.
- `G_comparacion.png`: (g), speedup en ambos computadores.
- `correr_Xeon.log`: salida en pantalla de `correr.py` en el Xeon.

## Resumen (mínimo de las repeticiones, N = 2048)

| | MacBookM2 | Xeon |
|---|---|---|
| (a) serial, n = N / mejor n | 1,49 s / n = 2048 | 2,60 s / n = 128 (2,10 s) |
| (b) Alg. 1, T(1) → mejor T(p) | 1,55 → 0,60 s (p = 4) | 2,63 → 1,17 s (p = 4) |
| (c) Alg. 2 n = 128, T(1) → mejor T(p) | 1,66 → 0,49 s (p = 8) | 2,11 → 1,06 s (p = 2) |
| (d) Alg. 3 Numba, T(1) → mejor T(p) | 1,33 → 0,60 s (p = 4) | 2,59 → 1,16 s (p = 8) |

Las 412 filas de los dos CSV tienen `ok = True` (checksum igual al serial).

Para regenerar figuras y tablas sin volver a medir: `cd salidas && python3 ../graficos.py`.
