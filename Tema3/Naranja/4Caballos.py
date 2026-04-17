# Movimientos del caballo.
MOVES = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]

# Esta función verifica si el caballo puede moverse a una posición.
def genmovs(estado):
    nestados = []

    # Itera sobre cada pieza en el estado actual.
    for i, pieza in enumerate(estado):
        if pieza == 0:
            continue

        # Convierte los índices a coordenadas.
        x, y = divmod(i, 3)

        # Calcula los nuevos movimientos del caballo.
        # dx, dy representan el cambio en las coordenadas.
        # nx, ny representan las nuevas coordenadas después de aplicar el movimiento.
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy

            # Verifica si las nuevas coordenadas están dentro del tablero y si la casilla está vacía.
            if 0 <= nx < 3 and 0 <= ny < 3:
                # ni representa el nuevo índice.
                ni = nx * 3 + ny

                # Si la casilla de destino está vacía, crea un nuevo estado con el movimiento aplicado.
                if estado[ni] == 0:
                    nuevo = list(estado)
                    nuevo[ni] = pieza
                    nuevo[i] = 0
                    nestados.append(tuple(nuevo))
    return nestados

# Busqueda en anchura (BFS)

# Esta función es el algoritmo de búsqueda en anchura (BFS) para encontrar el camino desde el estado inicial al estado objetivo.
def resolver(inicio, objetivo):
    # cola es una lista que simula una cola para BFS, donde cada elemento es una tupla que contiene el estado actual y el camino recorrido hasta ese estado.
    cola = [(inicio, [inicio])]
    # visitados es un conjunto que almacena los estados ya visitados.
    visita = set()

    indice = 0

    # El algoritmo continúa hasta que se hayan procesado todos los estados en la cola.
    while indice < len(cola):
        estado, camino = cola[indice]
        indice += 1

        # Si el estado actual es el objetivo, se devuelve el camino recorrido.
        if estado == objetivo:
            return camino

        # Si el estado ya ha sido visitado, se omite para evitar ciclos.
        if estado in visita:
            continue

        visita.add(estado)

        # Para cada nuevo estado generado a partir del estado actual, si no ha sido visitado, se agrega a la cola junto con el camino actualizado.
        for nuevo in genmovs(estado):
            if nuevo not in visita:
                cola.append((nuevo, camino + [nuevo]))

    return None

# Imprimir tablero

# Solo imprime el tablero en la consola ... y ya, y creo que es lo mas facil de entender de aquí.
def imprimir(estado):
    simbolos = {0: ".", 1: "B", 2: "N"}
    for i in range(0, 9, 3):
        print(" ".join(simbolos[x] for x in estado[i:i+3]))
    print()

# Estados
inicio = (
    1, 0, 1,
    0, 0, 0,
    2, 0, 2
)

objetivo = (
    2, 0, 2,
    0, 0, 0,
    1, 0, 1
)

# Aqui solo se llama a la función para que resuelva el problema.
camino = resolver(inicio, objetivo)

# Mostrar resultado
if camino:
    print(f"Solución en {len(camino)-1} movimientos:\n")
    for paso in camino:
        imprimir(paso)
else:
    print("No hay solución.")