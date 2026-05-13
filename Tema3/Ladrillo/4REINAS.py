# PROBLEMA DE LAS N REINAS (N = 4)

# MATERIA: Inteligencia Artificial
# TEMA: Espacios de Estados
# MÉTODO: Búsqueda con Backtracking

N = 4                  
REINA = "♛"           
VACIO = "."           

iteracion = 0         

def imprimir_tablero(tablero):
    print("   " + " ".join(str(i) for i in range(N)))
    print("  " + "-" * (2 * N - 1))

    for i, fila in enumerate(tablero):
        print(f"{i}| " + " ".join(fila))
    print()  

def es_seguro(tablero, fila, col):

    for i in range(fila):
        if tablero[i][col] == REINA:
            return False

    for i, j in zip(range(fila - 1, -1, -1), range(col - 1, -1, -1)):
        if tablero[i][j] == REINA:
            return False

    for i, j in zip(range(fila - 1, -1, -1), range(col + 1, N)):
        if tablero[i][j] == REINA:
            return False

    return True


def resolver(tablero, fila):

    global iteracion

    if fila == N:
        print("Solución encontrada:\n")
        imprimir_tablero(tablero)
        return True

    for col in range(N):
        iteracion += 1
        print(f"[Iteración {iteracion}] Probando posición ({fila}, {col})")

        if es_seguro(tablero, fila, col):

            tablero[fila][col] = REINA
            print("Colocación de reina:")
            imprimir_tablero(tablero)

            if resolver(tablero, fila + 1):
                return True

            tablero[fila][col] = VACIO
            print(f"Retroceso desde ({fila}, {col})")
            imprimir_tablero(tablero)

        else:

            print("Posición inválida\n")

    return False

def main():

    tablero = [[VACIO for _ in range(N)] for _ in range(N)]

    print("\nPROBLEMA DE LAS 4 REINAS\n")


    if not resolver(tablero, 0):
        print("No existe solución.")

if __name__ == "__main__":
    main()