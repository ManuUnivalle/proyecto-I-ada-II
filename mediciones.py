import random
import time
import matplotlib.pyplot as plt

from subset_sum_dp import subset_sum as dp_subset_sum
from voraz import suma_subconjuntos


def generar_instancia(n):
    """S con n números pares positivos y distintos (así S es un conjunto)."""
    return random.sample(range(2, 8 * n + 2, 2), n)


def medir(funcion, S, k, repeticiones):
    """Devuelve el menor tiempo (en segundos) de varias ejecuciones."""
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(S, k)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return min(tiempos)


def experimento(nombre, instancias):
    """Imprime la tabla de tiempos y devuelve los datos para graficar."""
    print("\n" + nombre)
    print(f"{'n':>6} {'k':>8} {'DP (s)':>12} {'x DP':>7} {'Voraz (s)':>12} {'x Voraz':>8}")
    datos = []
    dp_anterior = None
    voraz_anterior = None
    for n, k in instancias:
        S = generar_instancia(n)
        t_dp = medir(dp_subset_sum, S, k, repeticiones=5)
        t_voraz = medir(suma_subconjuntos, S, k, repeticiones=50)
        c_dp = "-" if dp_anterior is None else f"{t_dp / dp_anterior:.2f}"
        c_voraz = "-" if voraz_anterior is None else f"{t_voraz / voraz_anterior:.2f}"
        print(f"{n:>6} {k:>8} {t_dp:>12.6f} {c_dp:>7} {t_voraz:>12.6f} {c_voraz:>8}")
        datos.append((n, k, t_dp, t_voraz))
        dp_anterior = t_dp
        voraz_anterior = t_voraz
    return datos


def graficar(datos, indice, etiqueta_x, titulo, archivo):
    """indice 0 = eje x es n, indice 1 = eje x es k."""
    x = [fila[indice] for fila in datos]
    t_dp = [fila[2] for fila in datos]
    t_voraz = [fila[3] for fila in datos]
    plt.figure()
    plt.plot(x, t_dp, marker="o", label="Programación dinámica")
    plt.plot(x, t_voraz, marker="s", label="Voraz")
    plt.yscale("log")   # escala logarítmica: el voraz es mucho más rápido que la DP
    plt.xlabel(etiqueta_x)
    plt.ylabel("Tiempo (s), escala logarítmica")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.savefig(archivo)
    plt.show()


if __name__ == "__main__":
    random.seed(42)   # para que las instancias se puedan repetir
    PRUEBA = False     # True: una sola instancia pequeña. False: todos los experimentos.

    if PRUEBA:
        experimento("Prueba pequeña", [(200, 1001)])
    else:
        # Todos los elementos de S son pares y todos los k son impares:
        # ninguna instancia tiene solución, así que ambos algoritmos hacen todo su trabajo.
        datos_a = experimento("Experimento A: n = 200, k variable",
                              [(200, k) for k in (1001, 2001, 4001, 8001, 16001)])
        datos_b = experimento("Experimento B: k = 2001, n variable",
                              [(n, 2001) for n in (100, 200, 400, 800, 1600)])

        graficar(datos_a, 1, "k", "Tiempo según k (n = 200)", "grafica_k.png")
        graficar(datos_b, 0, "n", "Tiempo según n (k = 2001)", "grafica_n.png")