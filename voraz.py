#Enfoque voraz suma subconjuntos

def suma_subconjuntos(S, k):
    if k == 0:
        return 1, []
    resultado = []
    acumulado = 0

    for elemento in sorted(S, reverse=True):
        if elemento + acumulado <= k:
            resultado.append(elemento)
            acumulado += elemento
            if acumulado == k:
                return 1, resultado
    return 0, []
