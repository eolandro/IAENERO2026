"""
n_reinas.py

Problema de las N-Reinas resuelto con backtracking.

"""

import sys


def es_segura(tablero, fila, col):
    #Columna
    for i in range(fila):
        if tablero[i][col] == 1:
            return False
    #Diagonal superior izquierda
    i, j = fila - 1, col - 1
    while i >= 0 and j >= 0:
        if tablero[i][j] == 1:
            return False
        i -= 1
        j -= 1
    #Diagonal superior derecha
    i, j = fila - 1, col + 1
    while i >= 0 and j < len(tablero):
        if tablero[i][j] == 1:
            return False
        i -= 1
        j += 1
    return True


def colocar_reinas(tablero, fila, soluciones, verbose=False):
    N = len(tablero)

    if fila == N:
        soluciones.append([f[:] for f in tablero])
        return

    for col in range(N):
        if es_segura(tablero, fila, col):
            tablero[fila][col] = 1 

            if verbose:
                print(f"  Fila {fila+1}, columna {col+1}:")
                mostrar(tablero)

            colocar_reinas(tablero, fila + 1, soluciones, verbose)

            tablero[fila][col] = 0  



def mostrar(tablero, numero=None):
    """
    Imprime el tablero con:
      Q  = reina
      .  = casilla atacada
      X  = casilla libre
    """
    N = len(tablero)

    atacadas = [[False] * N for _ in range(N)]
    for fila in range(N):
        for col in range(N):
            if tablero[fila][col] == 1:
                _marcar_ataques(atacadas, fila, col, N)

    encabezado = f"  Solución {numero}" if numero else ""
    if encabezado:
        print(encabezado)

    print("  ┌" + "───┬" * (N - 1) + "───┐")
    for i, fila in enumerate(tablero):
        linea = "  │"
        for j, celda in enumerate(fila):
            if celda == 1:
                linea += " Q │"
            elif atacadas[i][j]:
                linea += " . │"
            else:
                linea += " X │"
        print(linea)
        if i < N - 1:
            print("  ├" + "───┼" * (N - 1) + "───┤")
    print("  └" + "───┴" * (N - 1) + "───┘")
    print()


def _marcar_ataques(atacadas, fila, col, N):
    """Marca todas las celdas atacadas por la reina en (fila, col)."""
    for j in range(N):
        atacadas[fila][j] = True
    for i in range(N):
        atacadas[i][col] = True
    i, j = fila - 1, col - 1
    while i >= 0 and j >= 0:
        atacadas[i][j] = True
        i -= 1; j -= 1
    i, j = fila - 1, col + 1
    while i >= 0 and j < N:
        atacadas[i][j] = True
        i -= 1; j += 1
    i, j = fila + 1, col - 1
    while i < N and j >= 0:
        atacadas[i][j] = True
        i += 1; j -= 1
    i, j = fila + 1, col + 1
    while i < N and j < N:
        atacadas[i][j] = True
        i += 1; j += 1



def guardar_yaml(soluciones, N):

    nombre = f"soluciones_{N}_reinas.yaml"
    with open(nombre, "w", encoding="utf-8") as f:
        for idx, tablero in enumerate(soluciones, start=1):
            posiciones = [fila.index(1) + 1 for fila in tablero]
            f.write(f"- solución: {idx}\n")
            f.write(f"  posiciones: {posiciones}\n")
            f.write(f"  tablero:\n")
            for fila in tablero:
                f.write(f"  - {' '.join(str(c) for c in fila)}\n")
    print(f"-> Soluciones guardadas en '{nombre}'\n")
    return nombre



def main():
    args = sys.argv[1:]
    verbose = "-v" in args
    args = [a for a in args if a != "-v"]

    N = int(args[0]) if args else 4

    print(f"  Problema de las {N}-Reinas\n")
    print(f"  Tablero: {N}×{N}")
    print(f"  Modo detallado: {'sí' if verbose else 'no'}")
    print()

    if verbose:
        print("---")

    tablero = [[0] * N for _ in range(N)]
    soluciones = []
    colocar_reinas(tablero, 0, soluciones, verbose=verbose)

    print(f" Resultados: \n")
    print(f" Se encontraron {len(soluciones)} soluciones:\n")

    for i, sol in enumerate(soluciones, start=1):
        mostrar(sol, numero=i)

    guardar_yaml(soluciones, N)


if __name__ == "__main__":
    main()
