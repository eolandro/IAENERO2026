# ============================================
# R005 - CABALLOS INTERCAMBIO (CORREGIDO)
# ============================================

"""
DESCRIPCIÓN:
Este programa resuelve el problema de intercambio de caballos en un tablero,
donde dos caballos de un lado y dos del otro deben intercambiar sus posiciones.

El problema se modela como un espacio de estados donde:
- Cada estado representa la posición de los caballos en el tablero
- Cada movimiento es un movimiento válido de caballo en ajedrez

Se utiliza el algoritmo BFS (Breadth-First Search) para encontrar la solución
con el menor número de movimientos.
"""

from collections import deque

"""
Movimientos posibles del caballo en ajedrez.
El caballo se mueve en forma de "L":
2 casillas en una dirección y 1 en perpendicular.
"""
movimientos = [
    (2,1),(2,-1),(-2,1),(-2,-1),
    (1,2),(1,-2),(-1,2),(-1,-2)
]

def dentro_tablero(x, y):
    """
    Verifica que una posición esté dentro de los límites del tablero (6x6).
    """
    return 0 <= x < 6 and 0 <= y < 6


def bfs_caballos(inicial, objetivo):
    """
    Implementación de búsqueda en anchura (BFS).

    PARÁMETROS:
    inicial  -> estado inicial (posiciones de los caballos)
    objetivo -> estado objetivo

    CADA ESTADO:
    Es una lista de tuplas [(x,y), ...] donde cada tupla representa
    la posición de un caballo.

    FUNCIONAMIENTO:
    - Se usa una cola (FIFO) para explorar los estados
    - Se almacenan los estados visitados para evitar ciclos
    - Se genera un árbol de búsqueda hasta encontrar el objetivo
    """

    # Cola que almacena (estado, camino recorrido)
    cola = deque([(inicial, [])])

    # Conjunto de estados ya visitados
    visitados = set()

    while cola:

        # Extraer el primer elemento (FIFO)
        estado, camino = cola.popleft()

        """
        Convertimos el estado a tupla porque:
        - Las listas no se pueden usar en sets
        - Las tuplas sí son hashables (inmutables)
        """
        estado_t = tuple(estado)

        if estado_t in visitados:
            continue

        visitados.add(estado_t)

        # Verificar si se alcanzó el objetivo
        if estado == objetivo:
            return camino + [estado]

        """
        Generación de nuevos estados:
        Se intenta mover cada caballo en todas las direcciones posibles
        """
        for i, (x, y) in enumerate(estado):

            for dx, dy in movimientos:

                nx, ny = x + dx, y + dy

                if dentro_tablero(nx, ny):

                    """
                    IMPORTANTE:
                    Se evita que dos caballos ocupen la misma casilla.
                    Esto garantiza estados válidos.
                    """
                    if (nx, ny) in estado:
                        continue

                    # Crear nuevo estado copiando el actual
                    nuevo = list(estado)

                    # Mover solo el caballo i
                    nuevo[i] = (nx, ny)

                    # Agregar a la cola con su camino
                    cola.append((nuevo, camino + [estado]))

    return None


# ============================================
# CONFIGURACIÓN
# ============================================

"""
Estado inicial:
Dos caballos en la parte superior izquierda
Dos caballos en la parte inferior derecha
"""
inicio = [(0,0),(0,1),(5,4),(5,5)]

"""
Estado objetivo:
Los caballos intercambian posiciones
"""
objetivo = [(5,4),(5,5),(0,0),(0,1)]

print("\n--- CABALLOS INTERCAMBIO ---")

resultado = bfs_caballos(inicio, objetivo)

if resultado:
    print("Solución encontrada:\n")

    """
    Se imprime la secuencia de estados desde el inicio hasta el objetivo.
    Cada paso muestra la posición de todos los caballos.
    """
    for paso in resultado:
        print(paso)
else:
    print("No se encontró solución")