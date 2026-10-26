def subset_sum(S, k, mostrar_tabla=False):
    n = len(S)
    dp = [[False] * (k + 1) for _ in range(n + 1)] #matriz llena de False
    dp[0][0] = True  # Caso base en la fila 0, columna 0: suma 0 con 0 elementos
    
    # Llenado de la tabla con la recurrencia
    for i in range(1, n + 1):
        for j in range(0, k + 1):
            if S[i - 1] <= j: # Si el elemento actual es menor o igual que la suma actual
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - S[i - 1]] # Actualizar la celda con la recurrencia
            else:
                dp[i][j] = dp[i - 1][j] # Si el elemento actual es mayor que la suma actual, no se puede incluir en el subconjunto

    if mostrar_tabla: # Imprimir la tabla de programación dinámica
        for fila in dp:
            print(fila)

    # Respuesta final: dp[n][k] indica si es posible formar la suma k con los n elementos
    if not dp[n][k]:
        return 0, []

    # Reconstrucción del subconjunto, de la fila n hacia la fila 1
    subconjunto = []
    j = k
    for i in range(n, 0, -1): # Iterar desde la última fila hasta la primera
        if not dp[i - 1][j]: # Si la celda de arriba es False, significa que el elemento actual S[i-1] fue incluido en el subconjunto
            subconjunto.append(S[i - 1]) 
            j -= S[i - 1] # Restar el valor del elemento incluido de la suma restante
    return 1, subconjunto


