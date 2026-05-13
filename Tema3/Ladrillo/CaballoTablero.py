
# PROBLEMA DEL CABALLO (KNIGHT'S TOUR)

# MATERIA: Inteligencia Artificial
# TEMA: Espacios de Estados
# MÉTODO: Heurística de Warnsdorff

N = 5  

movimientos = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def imprimir_tablero(tablero):
    print("-" * (4 * N))
    for fila in tablero:
        print(" ".join(f"{x:2}" for x in fila))
    print("-" * (4 * N))
    print()

def es_valido(x, y, tablero):

    return 0 <= x < N and 0 <= y < N and tablero[x][y] == -1

def contar_movimientos(x, y, tablero):

    count = 0
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if es_valido(nx, ny, tablero):
            count += 1
    return count

def resolver():

    tablero = [[-1 for _ in range(N)] for _ in range(N)]

    x, y = 0, 0
    tablero[x][y] = 0

    print("\nRECORRIDO DEL CABALLO (PASO A PASO)\n")
    imprimir_tablero(tablero)

    for paso in range(1, N * N):

        opciones = []

        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if es_valido(nx, ny, tablero):
                grado = contar_movimientos(nx, ny, tablero)
                opciones.append((grado, nx, ny))

        if not opciones:
            print("No se encontró solución.")
            return

        opciones.sort()
        _, x, y = opciones[0]

        tablero[x][y] = paso

        print(f"Paso {paso}: movimiento a ({x}, {y})")
        imprimir_tablero(tablero)

    print("Recorrido completo encontrado.\n")

if __name__ == "__main__":
    resolver()