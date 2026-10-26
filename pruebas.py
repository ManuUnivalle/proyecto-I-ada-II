from voraz import suma_subconjuntos 
from subset_sum_dp import subset_sum 

CASOS = [  # (categoría, s, k, esperado)
    # base
    ("base", [], 0, 1), 
    ("base", [], 5, 0), 
    ("base", [7], 7, 1),
    ("base", [7], 5, 0), 
    ("base", [3, 5], 0, 1),
    # límite
    ("límite", [1, 2, 3, 4], 10, 1), 
    ("límite", [1, 2, 3], 10, 0),
    ("límite", [3, 34, 4, 12, 5, 2], 34, 1), 
    ("límite", [10, 20, 30], 5, 0),
    # normales
    ("normal", [3, 5], 8, 1), 
    ("normal", [4, 2, 1], 5, 1),
    ("normal", [3, 34, 4, 12, 5, 2], 16, 1), 
    ("normal", [3, 5], 4, 0),
    ("normal", [3, 34, 4, 12, 5, 2], 30, 0), 
    ("normal", [2, 4, 6, 8], 5, 0),
    # el voraz falla
    ("voraz falla", [4, 3, 2], 5, 1), 
    ("voraz falla", [5, 4, 3], 7, 1),
    ("voraz falla", [3, 34, 4, 12, 5, 2], 40, 1),
    # valores grandes en S, k pequeño (la DP depende de k, no del valor de S)
    ("S grande, k pequeño", [10**18, 5 * 10**17, 3, 4], 7, 1),
    ("S grande, k pequeño", [10**18, 5 * 10**17], 7, 0),
    # k mediano
    ("k mediano", [100000, 250000, 300000, 450000, 125000, 75000], 500000, 1),
    ("k mediano", [10**6, 400000, 350000, 250000, 100000], 750000, 1),
    ("k mediano", [200000, 400000, 600000, 800000], 10**6 + 1, 0),
]

for i, (cat, s, k, esp) in enumerate(CASOS, 1):
    v, d = suma_subconjuntos(s, k), subset_sum(s, k)
    print(f"{i} | {cat} | {s} | {k} | esperado {esp} | voraz {v} | DP {d}")