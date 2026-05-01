from collections import deque

# Tamaño del tablero
FILAS = 6
COLUMNAS = 6

# Los 8 movimientos posibles del caballo
MOVIMIENTOS_CABALLO = (
    (-2, -1), (-2, 1),
    (-1, -2), (-1, 2),
    ( 1, -2), ( 1, 2),
    ( 2, -1), ( 2, 1),
)

# Estado inicial: blancos arriba, negros abajo
ESTADO_INICIAL = (
    'W', '.', '.', '.', '.', 'W',
    '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.',
    'B', '.', '.', '.', '.', 'B',
)

# Estado objetivo: negros arriba, blancos abajo
ESTADO_OBJETIVO = (
    'B', '.', '.', '.', '.', 'B',
    '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.',
    'W', '.', '.', '.', '.', 'W',
)


def posicion_a_fila_columna(posicion):
    """Convierte un índice lineal a coordenadas (fila, columna)."""
    fila = posicion // COLUMNAS
    columna = posicion % COLUMNAS
    return fila, columna


def fila_columna_a_posicion(fila, columna):
    """Convierte coordenadas (fila, columna) a un índice lineal."""
    return fila * COLUMNAS + columna


def generar_movimientos(estado):
    """Genera todos los estados válidos alcanzables desde el estado actual."""
    estados_siguientes = []

    # Recorrer cada casilla del tablero
    for posicion in range(FILAS * COLUMNAS):
        pieza = estado[posicion]

        # Solo mover piezas (W o B), no casillas vacías
        if pieza == '.':
            continue

        fila, columna = posicion_a_fila_columna(posicion)

        # Probar cada movimiento en "L" del caballo
        for desplazamiento_fila, desplazamiento_columna in MOVIMIENTOS_CABALLO:
            nueva_fila = fila + desplazamiento_fila
            nueva_columna = columna + desplazamiento_columna

            # Verificar que no se salga del tablero
            if 0 <= nueva_fila < FILAS and 0 <= nueva_columna < COLUMNAS:
                nueva_posicion = fila_columna_a_posicion(nueva_fila, nueva_columna)

                # Verificar que la casilla destino esté vacía
                if estado[nueva_posicion] == '.':
                    # Crear nuevo estado intercambiando posiciones
                    tablero_nuevo = list(estado)
                    tablero_nuevo[nueva_posicion] = pieza
                    tablero_nuevo[posicion] = '.'
                    estados_siguientes.append(tuple(tablero_nuevo))

    return estados_siguientes


def busqueda_bfs(estado_inicial, estado_objetivo):
    """Busca el camino más corto del estado inicial al objetivo usando BFS."""
    # Cola de búsqueda: cada elemento es (estado_actual, camino_recorrido)
    cola = deque()
    cola.append((estado_inicial, [estado_inicial]))

    # Conjunto de estados visitados para evitar ciclos
    visitados = set()
    visitados.add(estado_inicial)

    while cola:
        estado_actual, camino = cola.popleft()

        # Verificar si llegamos al objetivo
        if estado_actual == estado_objetivo:
            return camino

        # Explorar todos los estados sucesores
        for estado_siguiente in generar_movimientos(estado_actual):
            if estado_siguiente not in visitados:
                visitados.add(estado_siguiente)
                nuevo_camino = camino + [estado_siguiente]
                cola.append((estado_siguiente, nuevo_camino))

    # No se encontró solución
    return None


def imprimir_tablero(estado):
    for fila in range(FILAS):
        fila_texto = ""
        for columna in range(COLUMNAS):
            posicion = fila_columna_a_posicion(fila, columna)
            fila_texto += estado[posicion] + " "
        print(fila_texto.strip())
    print()


if __name__ == "__main__":
    print("=" * 25)
    print("  PROBLEMA DE LOS 4 CABALLOS")
    print("=" * 25)
    print()

    print("Estado inicial:")
    imprimir_tablero(ESTADO_INICIAL)

    print("Estado objetivo:")
    imprimir_tablero(ESTADO_OBJETIVO)

    solucion = busqueda_bfs(ESTADO_INICIAL, ESTADO_OBJETIVO)

    if solucion is not None:
        numero_movimientos = len(solucion) - 1
        print(f"Solución encontrada en {numero_movimientos} movimientos.")
        print()

        # Imprimir cada paso de la solución
        for paso, estado in enumerate(solucion):
            print(f"--- Paso {paso} ---")
            imprimir_tablero(estado)
    else:
        print("No se encontró solución.")
