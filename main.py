

import csv
import random
import sys
import time

from dinamica import subset_sum                 # Programación dinámica
from voraz import suma_subconjuntos       # Enfoque voraz

MAX_CASILLAS_DP = 20_000_000

SEMILLA = 2026 

def entrada_valida(S, k):
    """Verifica si la entrada es valida."""
    if k < 0:
        return "k debe ser mayor o igual que 0."
    for x in S:
        if x <= 0:
            return "Todos los elementos de S deben ser enteros positivos."
    if len(set(S)) != len(S):
        return "S es un conjunto: no puede tener elementos repetidos."
    return None


def dp_es_viable(S, k):
    return (len(S) + 1) * (k + 1) <= MAX_CASILLAS_DP


def verificar(S, A, k):
    return set(A) <= set(S) and len(set(A)) == len(A) and sum(A) == k


def parsear_caso(texto_S, texto_k):
    try:
        S = [int(x) for x in texto_S.replace(",", " ").split()]
        k = int(texto_k.strip())
    except ValueError:
        raise ValueError("S y k deben ser números enteros.")
    error = entrada_valida(S, k)
    if error:
        raise ValueError(error)
    return S, k

def medir(funcion, S, k, repeticiones=1):
    mejor = float("inf")
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(S, k)
        fin = time.perf_counter()
        mejor = min(mejor, fin - inicio)
    return resultado, mejor


def resolver_caso(S, k, repeticiones=1):
    (r_voraz, sub_voraz), t_voraz = medir(suma_subconjuntos, S, k, repeticiones)

    if dp_es_viable(S, k):
        (r_dp, sub_dp), t_dp = medir(subset_sum, S, k, repeticiones)
    else:
        r_dp, sub_dp, t_dp = None, None, None

    return {
        "n": len(S), "k": k,
        "dp": r_dp, "sub_dp": sub_dp, "t_dp": t_dp,
        "voraz": r_voraz, "sub_voraz": sub_voraz, "t_voraz": t_voraz,
        "voraz_acierta": None if r_dp is None else (r_voraz == r_dp),
    }


def mostrar_resultado(S, k, res):
    muestra = S if len(S) <= 15 else S[:15] + ["..."]
    print(f"\n  S = {muestra}  (n = {len(S)})")
    print(f"  k = {k}")

    if res["dp"] is None:
        print(f"  DP     -> no se ejecutó: la tabla tendría {(len(S) + 1) * (k + 1):,} casillas "
              f"(límite {MAX_CASILLAS_DP:,}).")
    else:
        ok = "" if res["dp"] == 0 or verificar(S, res["sub_dp"], k) else "  [¡ERROR DE VERIFICACIÓN!]"
        print(f"  DP     -> salida {res['dp']}, subconjunto {res['sub_dp']}, "
              f"tiempo {res['t_dp'] * 1000:.4f} ms{ok}")

    ok = "" if res["voraz"] == 0 or verificar(S, res["sub_voraz"], k) else "  [¡ERROR DE VERIFICACIÓN!]"
    print(f"  Voraz  -> salida {res['voraz']}, subconjunto {res['sub_voraz']}, "
          f"tiempo {res['t_voraz'] * 1000:.4f} ms{ok}")

    if res["voraz_acierta"] is True:
        print("  Comparación: el voraz coincide con la DP.")
    elif res["voraz_acierta"] is False:
        print("  Comparación: EL VORAZ FALLA (la DP encontró solución y el voraz no).")


# ----------------------------------------------------------------------------
# Generador de casos
# ----------------------------------------------------------------------------

def generar_caso(rng, n, valor_max, k=None):
    S = rng.sample(range(1, valor_max + 1), n)
    if k is None:
        if rng.random() < 0.5:
            tam = rng.randint(1, n)
            k = sum(rng.sample(S, tam))
        else:
            k = rng.randint(1, sum(S))
    return S, k


def generar_caso_falla_voraz(rng, n, valor_max, intentos=10_000):
    for _ in range(intentos):
        S = rng.sample(range(1, valor_max + 1), n)
        tam = rng.randint(2, n)
        k = sum(rng.sample(S, tam))
        if suma_subconjuntos(S, k)[0] == 0 and dp_es_viable(S, k) and subset_sum(S, k)[0] == 1:
            return S, k
    return None


# Casos fijos diseñados por el equipo (incluye contraejemplos del voraz, sección 3.3)
CASOS_EJEMPLO = [
    ("Caso positivo (1.1)", [3, 5], 8),
    ("Caso negativo (1.1)", [3, 5], 4),
    ("k = 0 (conjunto vacío)", [3, 5], 0),
    ("Tabla de la DP (2.3)", [2, 3, 5], 7),
    ("Contraejemplo 1 del voraz (3.3)", [4, 3, 2], 5),
    ("Contraejemplo 2 del voraz (3.3)", [3, 34, 4, 12, 5, 2], 40),
    ("Contraejemplo del voraz (3.4)", [5, 4, 3], 7),
    ("k mayor que la suma de S", [1, 2, 3], 100),
    ("S vacío y k > 0", [], 5),
    ("Un solo elemento igual a k", [9], 9),
]


def opcion_consola():
    texto_S = input("Elementos de S separados por espacios: ")
    texto_k = input("Valor de k: ")
    try:
        S, k = parsear_caso(texto_S, texto_k)
    except ValueError as e:
        print("Entrada inválida:", e)
        return
    res = resolver_caso(S, k)
    mostrar_resultado(S, k, res)
    if res["dp"] is not None and len(S) <= 10 and k <= 30:
        if input("\n¿Mostrar la tabla de la DP? (s/n): ").strip().lower() == "s":
            subset_sum(S, k, mostrar_tabla=True)


def leer_archivo(ruta):
    casos = []
    with open(ruta, encoding="utf-8") as f:
        for num, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if ";" not in linea:
                print(f"  Línea {num} ignorada: falta el ';' que separa S de k.")
                continue
            texto_S, texto_k = linea.split(";", 1)
            try:
                S, k = parsear_caso(texto_S, texto_k)
                casos.append((num, S, k))
            except ValueError as e:
                print(f"  Línea {num} ignorada: {e}")
    return casos


def opcion_archivo(ruta=None):
    if ruta is None:
        ruta = input("Ruta del archivo de casos: ").strip()
    try:
        casos = leer_archivo(ruta)
    except OSError:
        print(f"No se pudo abrir el archivo '{ruta}'.")
        return
    if not casos:
        print("El archivo no tiene casos válidos.")
        return
    for num, S, k in casos:
        print(f"\n--- Caso de la línea {num} ---", end="")
        mostrar_resultado(S, k, resolver_caso(S, k))


def opcion_ejemplos():
    for nombre, S, k in CASOS_EJEMPLO:
        print(f"\n--- {nombre} ---", end="")
        mostrar_resultado(S, k, resolver_caso(S, k))


def leer_entero(mensaje, minimo=1, por_defecto=None):
    while True:
        texto = input(mensaje).strip()
        if texto == "" and por_defecto is not None:
            return por_defecto
        try:
            valor = int(texto)
            if valor >= minimo:
                return valor
        except ValueError:
            pass
        print(f"  Debe ser un entero mayor o igual que {minimo}.")


def opcion_aleatorios():
    cantidad = leer_entero("¿Cuántos casos generar? [10]: ", 1, 10)
    n = leer_entero("Tamaño n de cada S [10]: ", 1, 10)
    valor_max = leer_entero("Valor máximo de los elementos [50]: ", n, max(50, n))
    rng = random.Random(SEMILLA)

    aciertos = total = 0
    for i in range(1, cantidad + 1):
        S, k = generar_caso(rng, n, valor_max)
        res = resolver_caso(S, k)
        print(f"\n--- Caso aleatorio {i} ---", end="")
        mostrar_resultado(S, k, res)
        if res["voraz_acierta"] is not None:
            total += 1
            aciertos += res["voraz_acierta"]
    if total:
        print(f"\nResumen: el voraz acertó en {aciertos} de {total} casos "
              f"({100 * aciertos / total:.1f} %).")

    print("\nBuscando un caso donde el voraz falle...", end="")
    caso = generar_caso_falla_voraz(rng, max(n, 3), valor_max)
    if caso:
        mostrar_resultado(caso[0], caso[1], resolver_caso(*caso))
    else:
        print(" no se encontró con estos parámetros.")


def ms(t):
    return "no ejecutada (tabla demasiado grande)" if t is None else f"{t * 1000:10.3f} ms"


def opcion_experimento():
    rng = random.Random(SEMILLA)
    repeticiones = 3
    filas = []

    print("\nExperimento 1: k fijo = 10 000, n variable")
    for n in [10, 50, 100, 200, 400, 800]:
        S, _ = generar_caso(rng, n, 20_000)
        res = resolver_caso(S, 10_000, repeticiones)
        filas.append(("n variable", res))
        print(f"  n = {n:4d}  DP = {ms(res['t_dp'])}   Voraz = {ms(res['t_voraz'])}")

    print("\nExperimento 2: n fijo = 50, k variable")
    S, _ = generar_caso(rng, 50, 10**6)
    for k in [10**2, 10**3, 10**4, 10**5, 10**6]:
        res = resolver_caso(S, k, repeticiones)
        filas.append(("k variable", res))
        print(f"  k = {k:8d}  DP = {ms(res['t_dp'])}   Voraz = {ms(res['t_voraz'])}")

    ruta = "resultados_tiempos.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["experimento", "n", "k", "salida_dp", "salida_voraz",
                    "voraz_acierta", "tiempo_dp_ms", "tiempo_voraz_ms"])
        for exp, r in filas:
            w.writerow([exp, r["n"], r["k"], r["dp"], r["voraz"], r["voraz_acierta"],
                        "" if r["t_dp"] is None else f"{r['t_dp'] * 1000:.4f}",
                        f"{r['t_voraz'] * 1000:.4f}"])
    print(f"\nResultados guardados en '{ruta}'.")



# Menú principal

def menu():
    opciones = {
        "1": ("Ingresar un caso por consola", opcion_consola),
        "2": ("Leer casos desde un archivo", opcion_archivo),
        "3": ("Ejecutar los casos de ejemplo del equipo", opcion_ejemplos),
        "4": ("Generar casos aleatorios", opcion_aleatorios),
        "5": ("Experimento de tiempos (exporta CSV)", opcion_experimento),
    }
    while True:
        print("\n===== SUMA DE SUBCONJUNTOS: DP vs. VORAZ =====")
        for clave, (texto, _) in opciones.items():
            print(f"  {clave}. {texto}")
        print("  0. Salir")
        eleccion = input("Opción: ").strip()
        if eleccion == "0":
            break
        if eleccion in opciones:
            try:
                opciones[eleccion][1]()
            except KeyboardInterrupt:
                print("\nOperación cancelada.")
            except MemoryError:
                print("\nNo hay memoria suficiente para este caso.")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            opcion_archivo(sys.argv[1])
        else:
            menu()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")
