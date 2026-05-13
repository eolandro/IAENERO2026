# ============================================
# R004 - N REINAS (4x4)
# ============================================

"""
DESCRIPCIÓN:
Este programa resuelve el problema de las N reinas utilizando backtracking.

El objetivo es colocar N reinas en un tablero NxN de forma que:
- Ninguna reina ataque a otra
- Es decir, no pueden estar en la misma fila, columna o diagonal

El problema se modela como un espacio de estados:
- Cada estado representa una configuración parcial del tablero
- Se construye fila por fila hasta encontrar una solución válida
"""

# Tamaño del tablero
N = 4

"""
REPRESENTACIÓN:
El tablero se representa como una lista:
tablero[i] = columna donde está la reina en la fila i

Ejemplo:
[1, 3, 0, 2] significa:
Fila 0 → columna 1
Fila 1 → columna 3
Fila 2 → columna 0
Fila 3 → columna 2
"""


def es_seguro(tablero, fila, col):
    """
    Verifica si es seguro colocar una reina en la posición (fila, col).

    CONDICIONES:
    - No debe haber otra reina en la misma columna
    - No debe haber otra reina en diagonales

    NOTA IMPORTANTE:
    Solo se revisan filas anteriores porque el algoritmo construye
    el tablero de arriba hacia abajo.
    """

    # Verificar columna
    for i in range(fila):
        if tablero[i] == col:
            return False

    # Verificar diagonales
    for i in range(fila):
        """
        Dos posiciones están en diagonal si:
        |col1 - col2| == |fila1 - fila2|
        """
        if abs(tablero[i] - col) == abs(i - fila):
            return False

    return True


def resolver_n_reinas(tablero, fila):
    """
    Algoritmo de backtracking.

    FUNCIONAMIENTO:
    - Intenta colocar una reina en cada columna de la fila actual
    - Si la posición es segura, continúa con la siguiente fila
    - Si no encuentra solución, retrocede (backtracking)
    """

    # Caso base: se colocaron todas las reinas
    if fila == N:
        return True

    # Probar todas las columnas
    for col in range(N):

        if es_seguro(tablero, fila, col):

            # Colocar reina
            tablero[fila] = col

            # Llamada recursiva para la siguiente fila
            if resolver_n_reinas(tablero, fila + 1):
                return True

            # BACKTRACKING:
            # Si no funciona, quitar la reina
            tablero[fila] = -1

    return False


def imprimir_tablero(tablero):
    """
    Imprime el tablero de forma visual:
    Q -> reina
    . -> espacio vacío
    """
    for i in range(N):
        fila = ["Q" if tablero[i] == j else "." for j in range(N)]
        print(" ".join(fila))


# ============================================
# EJECUCIÓN
# ============================================

"""
Inicializamos el tablero con -1 (sin reinas)
"""
tablero = [-1] * N

"""
Se ejecuta el algoritmo empezando desde la fila 0
"""
resolver_n_reinas(tablero, 0)

print("\n--- N REINAS (4x4) ---")

"""
Se imprime la solución encontrada
"""
imprimir_tablero(tablero)