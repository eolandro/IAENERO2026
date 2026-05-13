# ============================================
# COME SOLO - TABLERO CLÁSICO 7x7 (FUNCIONA)
# ============================================

"""
DESCRIPCIÓN:
Este programa resuelve el juego "Come Solo" (Peg Solitaire) utilizando
backtracking. El objetivo es dejar una sola ficha en el tablero mediante
movimientos válidos.

El problema se modela como un espacio de estados:
- Cada estado representa una configuración del tablero
- Cada movimiento representa una transición entre estados

El algoritmo explora todas las combinaciones posibles hasta encontrar
una solución.
"""

"""
REPRESENTACIÓN DEL TABLERO:
-1 -> casilla inválida (no forma parte del tablero)
 1 -> ficha presente
 0 -> espacio vacío

El tablero tiene forma de cruz (configuración clásica del juego).
"""

tablero = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
    [ 1,  1, 1, 1, 1,  1,  1],
    [ 1,  1, 1, 0, 1,  1,  1],  # centro vacío
    [ 1,  1, 1, 1, 1,  1,  1],
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1]
]

"""
MOVIMIENTOS:
Cada movimiento está representado por:
(dx, dy, dx2, dy2)

dx, dy   -> posición de la ficha intermedia (la que se "come")
dx2, dy2 -> posición final del salto

Ejemplo:
(0, 1, 0, 2) -> mover a la derecha
"""
movimientos = [
    (0, 1, 0, 2),
    (0, -1, 0, -2),
    (1, 0, 2, 0),
    (-1, 0, -2, 0)
]

def es_valido(x, y):
    """
    Verifica que una posición:
    - esté dentro del tablero
    - no sea una casilla inválida (-1)
    """
    return 0 <= x < 7 and 0 <= y < 7 and tablero[x][y] != -1


def contar_fichas(tab):
    """
    Cuenta cuántas fichas (valor 1) hay en el tablero.
    Se usa para verificar si se llegó al estado objetivo.
    """
    return sum(c for fila in tab for c in fila if c == 1)


def imprimir_tablero(tab):
    """
    Imprime el tablero de forma visual.
    Las casillas inválidas (-1) se muestran como espacios en blanco.
    """
    for fila in tab:
        print(" ".join(str(c) if c != -1 else " " for c in fila))
    print()


def resolver(tab):
    """
    Algoritmo de backtracking.

    FUNCIONAMIENTO:
    1. Verifica si se alcanzó el objetivo (una sola ficha)
    2. Recorre todo el tablero buscando fichas
    3. Intenta todos los movimientos posibles
    4. Si un movimiento es válido, lo aplica
    5. Llama recursivamente para continuar
    6. Si no funciona, deshace el movimiento (backtracking)
    """

    # Caso base: solo queda una ficha
    if contar_fichas(tab) == 1:
        return True

    for i in range(7):
        for j in range(7):

            if tab[i][j] == 1:

                for dx, dy, dx2, dy2 in movimientos:

                    nx, ny = i + dx, j + dy     # ficha intermedia
                    fx, fy = i + dx2, j + dy2  # destino final

                    if es_valido(nx, ny) and es_valido(fx, fy):

                        """
                        CONDICIÓN DE MOVIMIENTO VÁLIDO:
                        - Debe haber una ficha en la posición intermedia
                        - La posición final debe estar vacía
                        """
                        if tab[nx][ny] == 1 and tab[fx][fy] == 0:

                            # ---- HACER MOVIMIENTO ----
                            tab[i][j] = 0
                            tab[nx][ny] = 0
                            tab[fx][fy] = 1

                            # Llamada recursiva
                            if resolver(tab):
                                return True

                            # ---- BACKTRACKING ----
                            # Se deshace el movimiento si no funcionó
                            tab[i][j] = 1
                            tab[nx][ny] = 1
                            tab[fx][fy] = 0

    return False


# ============================================
# EJECUCIÓN
# ============================================

print("\n--- COME SOLO (7x7) ---")

print("Tablero inicial:")
imprimir_tablero(tablero)

"""
Se ejecuta el algoritmo de backtracking.
Puede tardar debido a la gran cantidad de combinaciones posibles.
"""
if resolver(tablero):
    print("Solución encontrada")
else:
    print("No se encontró solución")

print("Tablero final:")
imprimir_tablero(tablero)