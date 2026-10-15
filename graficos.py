# graficos.py - Graficos y tablas de los items (e), (f) y (g).
# Uso: python3 graficos.py   (lee todos los resultados_*.csv)
import glob
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

PS = [1, 2, 4, 8]
COL = {"B": "#2a78d6", "C": "#eb6834", "D": "#1baf7a"}
NOMBRE = {"B": "Alg. 1 OpenMP", "C": "Alg. 2 OpenMP", "D": "Alg. 3 Numba"}
AZULES = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281", "#0d366b"]


def cores(maq):
    # Cores logicos guardados por correr.py
    try:
        return int(re.search(r"cores logicos: (\d+)", open(f"maquina_{maq}.txt").read()).group(1))
    except (OSError, AttributeError):
        return None


def tiempos(df, alg, N, n=None):
    # Minimo de las repeticiones por p (en segundos)
    q = df[(df.alg == alg) & (df.N == N)]
    if n is not None:
        q = q[q.n == n]
    return {p: q[q.p == p].tiempo_ms.min() / 1e3 for p in PS}


def ejes(ax, c, ylab):
    # Formato comun: eje p en base 2 y linea de cores
    ax.set_xscale("log", base=2)
    ax.set_xticks(PS)
    ax.set_xticklabels(PS)
    ax.set_xlabel("hilos p")
    ax.set_ylabel(ylab)
    ax.grid(alpha=0.3)
    if c:
        ax.axvline(c, color="gray", ls=":", lw=1)


def tabla_md(T):
    # Tabla T, S, E en el formato de Resultados.md
    s = "| Hilos ($p$) | Tiempo $T(p)$ [s] | Speedup $S(p)$ | Eficiencia $E(p)$ |\n| :---: | :---: | :---: | :---: |\n"
    for p in PS:
        s += f"| **{p}** | {T[p]:.3f} | {T[1] / T[p]:.2f} | {T[1] / T[p] / p:.2f} |\n"
    return s


def por_maquina(maq, df):
    c = cores(maq)
    nstar = int(df[(df.alg == "C") & (df.N != 2048)].n.mode().iloc[0]) if (df.N != 2048).any() else 128
    NE = 2048 if (df.N == 2048).any() else int(df.N.max())
    md = f"# Resultados {maq}\n\n"

    # Item (e): T, S y E de las tres versiones
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
    for alg in "BCD":
        T = tiempos(df, alg, NE, nstar if alg == "C" else None)
        lab = NOMBRE[alg] + (f" (n={nstar})" if alg == "C" else "")
        ax[0].plot(PS, [T[p] for p in PS], "o-", color=COL[alg], label=lab)
        ax[1].plot(PS, [T[1] / T[p] for p in PS], "o-", color=COL[alg], label=lab)
        ax[2].plot(PS, [T[1] / T[p] / p for p in PS], "o-", color=COL[alg], label=lab)
        md += f"## {lab}, N={NE}\n\n" + tabla_md(T) + "\n"
    ax[1].plot(PS, PS, "--", color="gray", label="ideal")
    ax[2].axhline(1, ls="--", color="gray", label="ideal")
    for a, y in zip(ax, ["T(p) [s]", "S(p)", "E(p)"]):
        ejes(a, c, y)
    ax[0].legend()
    ax[1].legend()
    fig.suptitle(f"(e) {maq}: tiempo, speedup y eficiencia, N={NE}")
    fig.tight_layout()
    fig.savefig(f"E_{maq}.png", dpi=150)
    plt.close(fig)

    # Item (e): efecto del bloque n en el Alg. 2
    bloques = sorted(df[(df.alg == "C") & (df.N == NE)].n.unique(), reverse=True)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    md += f"## Alg. 2 segun n, N={NE} (T en s)\n\n| n | " + " | ".join(f"T({p})" for p in PS) + " | S max |\n|" + " :---: |" * 6 + "\n"
    for n, col in zip(bloques, AZULES):
        T = tiempos(df, "C", NE, n)
        ax[0].plot(PS, [T[p] for p in PS], "o-", color=col, label=f"n={n}")
        ax[1].plot(PS, [T[1] / T[p] for p in PS], "o-", color=col, label=f"n={n}")
        md += f"| {n} | " + " | ".join(f"{T[p]:.3f}" for p in PS) + f" | {max(T[1] / T[p] for p in PS):.2f} |\n"
    ax[1].plot(PS, PS, "--", color="gray", label="ideal")
    ejes(ax[0], c, "T(p) [s]")
    ejes(ax[1], c, "S(p)")
    ax[1].legend(ncol=2)
    fig.suptitle(f"(e) {maq}: Alg. 2 para distintos n, N={NE}")
    fig.tight_layout()
    fig.savefig(f"E_bloques_{maq}.png", dpi=150)
    plt.close(fig)

    # Item (f): eficiencia por N y eficiencia debil
    Ns = sorted(df.N.unique())
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
    md += "\n## (f) Eficiencia por N\n\n| Version | N | " + " | ".join(f"E({p})" for p in PS) + " | E debil |\n|" + " :---: |" * 7 + "\n"
    for a, alg in zip(ax, "BCD"):
        Tn = {N: tiempos(df, alg, N, nstar if alg == "C" else None) for N in Ns}
        for N, col in zip(Ns, AZULES[::2]):
            T = Tn[N]
            a.plot(PS, [T[1] / T[p] / p for p in PS], "o-", color=col, label=f"N={N}")
            # Trabajo 2N^3: N con p=8 equivale a N/2 con p=1
            ed = f"{Tn[N // 2][1] / T[8]:.2f}" if N // 2 in Tn else "-"
            md += f"| {NOMBRE[alg]} | {N} | " + " | ".join(f"{T[1] / T[p] / p:.2f}" for p in PS) + f" | {ed} |\n"
        a.axhline(1, ls="--", color="gray")
        ejes(a, c, "E(p)")
        a.set_title(NOMBRE[alg])
    ax[0].legend()
    fig.suptitle(f"(f) {maq}: eficiencia al crecer N")
    fig.tight_layout()
    fig.savefig(f"F_{maq}.png", dpi=150)
    plt.close(fig)

    open(f"tablas_{maq}.md", "w").write(md)
    return {alg: tiempos(df, alg, NE, nstar if alg == "C" else None) for alg in "BCD"}


def main():
    datos = {re.search(r"resultados_(.+)\.csv", f).group(1): pd.read_csv(f) for f in sorted(glob.glob("resultados_*.csv"))}
    for maq, df in datos.items():
        if not df.ok.all():
            print(f"aviso: {maq} tiene corridas que no coinciden con la referencia")
    res = {maq: por_maquina(maq, df) for maq, df in datos.items()}

    # Item (g): speedup en cada computador
    if len(res) >= 2:
        fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
        for a, alg in zip(ax, "BCD"):
            for maq, col in zip(res, ["#2a78d6", "#eb6834", "#1baf7a"]):
                T = res[maq][alg]
                a.plot(PS, [T[1] / T[p] for p in PS], "o-", color=col, label=maq)
            a.plot(PS, PS, "--", color="gray", label="ideal")
            ejes(a, None, "S(p)")
            a.set_title(NOMBRE[alg])
        ax[0].legend()
        fig.suptitle("(g) Speedup en ambos computadores")
        fig.tight_layout()
        fig.savefig("G_comparacion.png", dpi=150)
        plt.close(fig)
    print("graficos y tablas_<maquina>.md listos")


if __name__ == "__main__":
    main()
