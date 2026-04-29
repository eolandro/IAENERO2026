from collections import deque
import copy

# Estado inicial
inicio = [
    ['C', ' ', 'C'],
    [' ', ' ', ' '],
    ['c', ' ', 'c']
]

# Estado objetivo
objetivo = [
    ['c', ' ', 'c'],
    [' ', ' ', ' '],
    ['C', ' ', 'C']
]

# Movimientos de caballo
movs = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]


# ===============================
# IMPRIMIR TABLERO
# ===============================
def imprimir(tablero):
    for fila in tablero:
        print(fila)
    print("------------------")


# ===============================
# OBTENER POSICIONES
# ===============================
def obtener_caballos(tablero):
    caballos = []
    for i in range(3):
        for j in range(3):
            if tablero[i][j] in ['C', 'c']:
                caballos.append((i, j))
    return caballos


# ===============================
# GENERAR MOVIMIENTOS
# ===============================
def generar_movimientos(tablero):
    nuevos_estados = []

    for i in range(3):
        for j in range(3):
            if tablero[i][j] in ['C', 'c']:
                for dx, dy in movs:
                    ni, nj = i + dx, j + dy

                    if 0 <= ni < 3 and 0 <= nj < 3 and tablero[ni][nj] == ' ':
                        nuevo = copy.deepcopy(tablero)
                        nuevo[ni][nj] = nuevo[i][j]
                        nuevo[i][j] = ' '
                        nuevos_estados.append(nuevo)

    return nuevos_estados


# ===============================
# BFS
# ===============================
def resolver():
    cola = deque()
    visitados = set()

    cola.append((inicio, []))
    visitados.add(str(inicio))

    while cola:
        actual, camino = cola.popleft()

        if actual == objetivo:
            return camino + [actual]

        for siguiente in generar_movimientos(actual):
            if str(siguiente) not in visitados:
                visitados.add(str(siguiente))
                cola.append((siguiente, camino + [actual]))

    return None


# ===============================
# MAIN
# ===============================
def main():
    solucion = resolver()

    if solucion:
        print(f"Solución encontrada en {len(solucion)-1} movimientos:\n")
        for paso in solucion:
            imprimir(paso)
    else:
        print("No hay solución")


if __name__ == "__main__":
    main()