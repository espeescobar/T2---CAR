**A**
./serial 2048 2048
N=2048 n=2048 tiempo=5409.92 ms checksum=172.331627

./serial 2048 1024
N=2048 n=1024 tiempo=5505.41 ms checksum=172.331627

./serial 2048 512
N=2048 n=512 tiempo=6395.82 ms checksum=172.331627

./serial 2048 256
N=2048 n=256 tiempo=4918.70 ms checksum=172.331627

./serial 2048 128
N=2048 n=128 tiempo=4172.19 ms checksum=172.331627

./serial 2048 64
N=2048 n=64 tiempo=4760.45 ms checksum=172.331627

./serial 2048 32
N=2048 n=32 tiempo=5484.10 ms checksum=172.331627

**B**
N=2048 p=1 tiempo=8294.60 ms checksum=172.331627
N=2048 p=2 tiempo=3242.35 ms checksum=172.331627
N=2048 p=4 tiempo=2005.11 ms checksum=172.331627
N=2048 p=8 tiempo=1899.74 ms checksum=172.331627

| Hilos ($p$) | Tiempo $T(p)$ [ms] | Speedup $S(p)$ | Eficiencia $E(p)$ |
| :---: | :---: | :---: | :---: |
| **1** | 8294.60 | 1.00 | 1.00 (100%) |
| **2** | 3242.35 | 2.56 | 1.28 (128%) |
| **4** | 2005.11 | 4.14 | 1.03 (103%) |
| **8** | 1899.74 | 4.37 | 0.55 (55%) |

**Análisis de resultados:**
Los valores se obtienen aplicando las fórmulas de aceleración $S(p) = T(1)/T(p)$ y eficiencia $E(p) = S(p)/p$[cite: 3]. Con estos datos se observa un fenómeno llamado **speedup superlineal** (eficiencia mayor al 100%) para $p=2$ y $p=4$. Esto ocurre frecuentemente en multiplicaciones de matrices grandes porque, al dividir el trabajo entre los hilos, los sub-bloques de datos procesados por cada núcleo ahora caben mejor en sus memorias caché locales (L1/L2), reduciendo los tiempos de acceso a la RAM general. Sin embargo, al llegar a los 8 hilos, la eficiencia vuelve a caer drásticamente al 55%, lo que indica que el bus de memoria principal se saturó al intentar alimentar de datos a los 8 núcleos simultáneamente, generando un cuello de botella.

**C**

N=2048 n=128 p=1 tiempo=4034.02 ms checksum=172.331627
N=2048 n=128 p=2 tiempo=2422.69 ms checksum=172.331627
N=2048 n=128 p=4 tiempo=1499.94 ms checksum=172.331627
N=2048 n=128 p=8 tiempo=1272.35 ms checksum=172.331627

| Hilos ($p$) | Tiempo $T(p)$ [ms] | Speedup $S(p)$ | Eficiencia $E(p)$ |
| :---: | :---: | :---: | :---: |
| **1** | 4034.02 | 1.00 | 1.00 (100%) |
| **2** | 2422.69 | 1.67 | 0.83 (83%) |
| **4** | 1499.94 | 2.69 | 0.67 (67%) |
| **8** | 1272.35 | 3.17 | 0.40 (40%) |

Los valores se obtienen aplicando las fórmulas de aceleración $S(p) = T(1)/T(p)$ y eficiencia $E(p) = S(p)/p$[cite: 3]. Al igual que en el Algoritmo 1, el rendimiento decae fuertemente al llegar a los 8 hilos. Aunque el uso de bloques optimiza el acceso a la caché[cite: 2], el paralelismo de tareas (`#pragma omp task`) introduce un overhead significativo debido a la creación, gestión y sincronización continua de los hilos en el árbol recursivo mediante la directiva `taskwait`. A medida que aumenta $p$, el costo de coordinar las tareas sobrepasa los beneficios de distribuirlas, limitando la eficiencia máxima.