# ============================================
# R006 - RECORRIDO DEL CABALLO
# ============================================

"""
DESCRIPCIÓN:
Este programa resuelve el problema del "Recorrido del Caballo" (Knight's Tour),
el cual consiste en mover un caballo de ajedrez sobre un tablero de tal forma
que visite todas las casillas exactamente una vez.

El algoritmo utiliza backtracking para explorar el espacio de estados,
probando diferentes movimientos hasta encontrar una solución válida.
"""

# Tamaño del tablero (6x6)
N = 6

"""
El tablero se representa como una matriz NxN.
- El valor -1 indica que la casilla no ha sido visitada
- Los números (0,1,2,...) representan el orden en que el caballo visita las casillas
"""
tablero = [[-1]*N for _ in range(N)]

"""
Movimientos posibles del caballo en ajedrez:
El caballo se mueve en forma de "L":
2 casillas en una dirección y 1 en perpendicular
"""
movimientos = [
    (2,1),(1,2),(-1,2),(-2,1),
    (-2,-1),(-1,-2),(1,-2),(2,-1)
]

def es_valido(x, y):
    """
    Verifica si una posición es válida:
    - Debe estar dentro del tablero
    - No debe haber sido visitada anteriormente
    """
    return 0 <= x < N and 0 <= y < N and tablero[x][y] == -1


def resolver_caballo(x, y, paso):
    """
    Función recursiva que intenta encontrar un recorrido completo.

    PARÁMETROS:
    x, y  -> posición actual del caballo
    paso  -> número de movimiento actual

    FUNCIONAMIENTO:
    - Marca la casilla con el número de paso
    - Intenta todos los movimientos posibles
    - Si no encuentra solución, retrocede (backtracking)
    """

    # Caso base: si se han visitado todas las casillas
    if paso == N*N:
        return True

    # Probar todos los movimientos posibles
    for dx, dy in movimientos:

        nx, ny = x + dx, y + dy

        if es_valido(nx, ny):

            # Marcar la casilla con el número de paso
            tablero[nx][ny] = paso

            # Llamada recursiva
            if resolver_caballo(nx, ny, paso + 1):
                return True

            # BACKTRACKING:
            # Si no funcionó, deshacer el movimiento
            tablero[nx][ny] = -1

    return False


# ============================================
# EJECUCIÓN
# ============================================

print("\n--- RECORRIDO DEL CABALLO ---")

"""
Se inicia el recorrido desde la posición (0,0)
Se marca como paso 0 porque es la primera casilla visitada
"""
tablero[0][0] = 0

"""
Se llama al algoritmo empezando desde (0,0)
El siguiente paso será 1
"""
resolver_caballo(0, 0, 1)

"""
Se imprime el tablero final.
Cada número representa el orden en que el caballo visitó esa casilla.
"""
for fila in tablero:
    print(fila)