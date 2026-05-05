import sys

def recorrido_caballo_interactivo():
    print("\n=== R006: Recorrido del Caballo (Heurística de Warnsdorff) ===")
    
    print("\n   A  B  C  D  E  F  G  H")
    for i in range(8, 0, -1):
        print(f"{i} " + "  ".join(["--"] * 8) + f"  {i}")
    print("   A  B  C  D  E  F  G  H")
        
    while True:
        pos = input("\n¿Dónde pondrás el caballo? (Ej. A1, E4) [S para salir]: ").strip().upper()
        if pos == 'S': 
            print("\nSaliendo...\n")
            return
        
        # Validar que sea una coordenada correcta de ajedrez (A-H, 1-8)
        if len(pos) == 2 and 'A' <= pos[0] <= 'H' and '1' <= pos[1] <= '8':
            break
        print("  [!] Entrada inválida. Usa el formato LetraNúmero (Ej. C3).")

    # Convertir coordenada a índices de matriz (Ej: A8 -> fila 0, col 0 | A1 -> fila 7, col 0)
    col_ini = ord(pos[0]) - ord('A')
    fila_ini = 8 - int(pos[1])
    
    n = 8
    tablero = [[-1]*n for _ in range(n)]
    movs = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]

    def es_valido(x, y):
        return 0 <= x < n and 0 <= y < n and tablero[x][y] == -1

    def contar_salidas(x, y):
        salidas = 0
        for dx, dy in movs:
            if es_valido(x + dx, y + dy): salidas += 1
        return salidas

    def resolver(x, y, paso):
        tablero[x][y] = paso
        
        # Si llegamos al paso 63 (64 casillas en total, contando desde el 0)
        if paso == n * n - 1: 
            return True

        siguientes = []
        for dx, dy in movs:
            nx, ny = x + dx, y + dy
            if es_valido(nx, ny):
                # Guardamos la cantidad de salidas futuras y las coordenadas
                siguientes.append((contar_salidas(nx, ny), nx, ny))

        # Warnsdorff: ordenar para saltar primero a la casilla con MENOS salidas futuras
        siguientes.sort(key=lambda item: item[0])

        for _, nx, ny in siguientes:
            if resolver(nx, ny, paso + 1): 
                return True

        # Backtrack si nos quedamos sin salida
        tablero[x][y] = -1
        return False

    print(f"\nCalculando recorrido completo desde '{pos}'...")
    
    if resolver(fila_ini, col_ini, 0):
        print("\n¡Recorrido completado con éxito!\n")
        print("Leyenda: 01 al 63 = Camino recorrido | ' C' = Posición final del caballo\n")
        
        print("   A   B   C   D   E   F   G   H")
        for r in range(n):
            fila_print = []
            for c in range(n):
                val = tablero[r][c]
                if val == 63:
                    fila_print.append(" C") # El caballo en su última posición
                else:
                    fila_print.append(f"{val+1:02d}") # Pasos del 01 al 63
                    
            print(f"{8-r}  " + "  ".join(fila_print) + f"  {8-r}")
        print("   A   B   C   D   E   F   G   H\n")
    else:
        print("No se encontró solución (Algo extremadamente raro con Warnsdorff).")

if __name__ == "__main__":
    recorrido_caballo_interactivo()