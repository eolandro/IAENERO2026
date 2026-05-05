# R004: N Reinas (Imprimiendo TODAS las soluciones)
def n_reinas(n=4):
    print(f"\n=== R004: {n} Reinas (Todas las soluciones) ===")
    
    def resolver(fila, tablero):
        if fila == n: 
            return [tablero[:]]
        soluciones = []
        for col in range(n):
            seguro = True
            # Verificamos ataques en columna y diagonales
            for i in range(fila):
                if tablero[i] == col or abs(tablero[i] - col) == abs(i - fila):
                    seguro = False
                    break
            
            if seguro:
                tablero[fila] = col
                soluciones.extend(resolver(fila + 1, tablero))
        return soluciones

    sols = resolver(0, [-1]*n)
    
    if sols:
        print(f"Se encontraron {len(sols)} soluciones diferentes para un tablero de {n}x{n}:\n")
        # Iteramos sobre todas las soluciones guardadas
        for num, sol in enumerate(sols, 1):
            print(f"--- Solución {num} ---")
            for fila in range(n):
                linea = ["[Q]" if c == sol[fila] else "[ ]" for c in range(n)]
                print(" ".join(linea))
            print("") # Espacio entre tableros
    else:
        print("No hay solución.")

n_reinas(4)