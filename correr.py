# correr.py - Mide B, C y D para los items (d)-(g) y guarda un CSV.
# Uso: python3 correr.py <maquina> [--reps 3] [--n 128] [--Ns 1024 2048 4096]
import argparse
import csv
import os
import platform
import re
import subprocess

PS = [1, 2, 4, 8]                        # hilos
BLOQUES = [1024, 512, 256, 128, 64, 32]  # n para el item (e)


def compilar():
    # Mismos flags del enunciado; binarios en bin/
    os.makedirs("bin", exist_ok=True)
    if platform.system() == "Darwin":
        omp = subprocess.run(["brew", "--prefix", "libomp"], capture_output=True, text=True).stdout.strip()
        cc = ["clang++", "-O3", "-mcpu=native", "-Xpreprocessor", "-fopenmp",
              f"-I{omp}/include", f"-L{omp}/lib", "-lomp"]
    else:
        cc = ["g++", "-O3", "-march=native", "-fopenmp"]
    for f in ["serial", "B", "C"]:
        subprocess.run(cc + [f"{f}.cpp", "-o", f"bin/{f}"], check=True)


def ejecutar(cmd):
    # Corre un programa y lee tiempo y checksum
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    t = float(re.search(r"tiempo=([\d.]+)", out).group(1))
    cs = float(re.search(r"checksum=(-?[\d.]+)", out).group(1))
    return t, cs


def info_maquina(nombre):
    # Cores y reloj para el item (g)
    txt = [f"sistema: {platform.platform()}", f"cores logicos: {os.cpu_count()}"]
    for cmd in (["lscpu"], ["sysctl", "-n", "machdep.cpu.brand_string", "hw.physicalcpu", "hw.logicalcpu"]):
        try:
            txt.append(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
        except (OSError, subprocess.CalledProcessError):
            pass
    with open(f"maquina_{nombre}.txt", "w") as f:
        f.write("\n".join(txt))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("maquina")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--n", type=int, default=128, help="hoja del Alg. 2")
    ap.add_argument("--Ns", type=int, nargs="+", default=[1024, 2048, 4096])
    ap.add_argument("--sin-compilar", action="store_true")
    a = ap.parse_args()

    if not a.sin_compilar:
        compilar()
    info_maquina(a.maquina)
    salida = f"resultados_{a.maquina}.csv"
    f = open(salida, "w", newline="")
    w = csv.writer(f)
    w.writerow(["maquina", "alg", "N", "n", "p", "rep", "tiempo_ms", "checksum", "ok"])

    # Referencia serial (n = N) y checksum de cada N
    ref = {}
    for N in a.Ns:
        t, ref[N] = ejecutar(["bin/serial", str(N), str(N)])
        w.writerow([a.maquina, "serial", N, N, 1, 0, t, ref[N], True])
        t, cs = ejecutar(["bin/serial", str(N), str(a.n)])
        w.writerow([a.maquina, "serial", N, a.n, 1, 0, t, cs, True])

    # Repeticiones intercaladas; con N grande se hacen 2
    for rep in range(a.reps):
        for N in a.Ns:
            if N >= 4096 and rep >= 2:
                continue
            bloques = sorted(set(BLOQUES + [a.n]), reverse=True) if N == 2048 else [a.n]
            for p in PS:
                corridas = [("B", N, ["bin/B", str(N), str(p)])]
                corridas += [("C", n, ["bin/C", str(N), str(n), str(p)]) for n in bloques if n <= N]
                corridas += [("D", N, ["python3", "D.py", str(N), str(p)])]
                for alg, n, cmd in corridas:
                    t, cs = ejecutar(cmd)
                    ok = abs(cs - ref[N]) <= 1e-6 * max(1.0, abs(ref[N]))  # verifica vs serial
                    w.writerow([a.maquina, alg, N, n, p, rep, t, cs, ok])
                    f.flush()
                    print(f"{alg} N={N} n={n} p={p} rep={rep} t={t:.1f} ms ok={ok}")
    f.close()
    print("listo:", salida)


if __name__ == "__main__":
    main()
