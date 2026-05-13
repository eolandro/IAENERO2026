# PROBLEMA DE LOS CABALLOS 1 (INTERCAMBIO)

# MATERIA: Inteligencia Artificial
# TEMA: Espacios de Estados
# MÉTODO: Búsqueda en Anchura (BFS)



from collections import deque

N = 6

movimientos = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
    print()

def es_valido(x, y):
    return 0 <= x < N and 0 <= y < N

def estado_a_tupla(tablero):

    return tuple(tuple(fila) for fila in tablero)

def generar_movimientos(tablero):
    nuevos_estados = []

    for i in range(N):
        for j in range(N):
            if tablero[i][j] in ["♘", "♞"]:

                for dx, dy in movimientos:
                    nx, ny = i + dx, j + dy

                    if es_valido(nx, ny) and tablero[nx][ny] == ".":
                        nuevo = [fila[:] for fila in tablero]

                        # Mover caballo
                        nuevo[nx][ny] = tablero[i][j]
                        nuevo[i][j] = "."

                        nuevos_estados.append(nuevo)

    return nuevos_estados


def bfs(inicio, objetivo):

    cola = deque()
    visitados = set()

    cola.append((inicio, []))
    visitados.add(estado_a_tupla(inicio))

    while cola:
        estado, camino = cola.popleft()

        # Verificar si llegamos al objetivo
        if estado == objetivo:
            return camino + [estado]

        for nuevo_estado in generar_movimientos(estado):
            t = estado_a_tupla(nuevo_estado)

            if t not in visitados:
                visitados.add(t)
                cola.append((nuevo_estado, camino + [estado]))

    return None

def main():

    inicio = [["." for _ in range(N)] for _ in range(N)]
    inicio[0][0] = "♘"
    inicio[0][1] = "♘"
    inicio[5][4] = "♞"
    inicio[5][5] = "♞"

    objetivo = [["." for _ in range(N)] for _ in range(N)]
    objetivo[0][0] = "♞"
    objetivo[0][1] = "♞"
    objetivo[5][4] = "♘"
    objetivo[5][5] = "♘"

    print("\nESTADO INICIAL:\n")
    imprimir_tablero(inicio)

    print("Buscando solución...\n")

    solucion = bfs(inicio, objetivo)

    if solucion:
        print(f"Solución encontrada en {len(solucion)-1} pasos:\n")

        for paso, estado in enumerate(solucion):
            print(f"Paso {paso}:")
            imprimir_tablero(estado)
    else:
        print("No se encontró solución.")


if __name__ == "__main__":
    main()