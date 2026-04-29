import json
import heapq
from pathlib import Path


def leer_tablero(nombre_archivo="tablero.json"):
    ruta = Path(nombre_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta.resolve()}")

    with ruta.open("r", encoding="utf-8") as archivo:
        data = json.load(archivo)

    if "tablero" not in data:
        raise KeyError("El archivo JSON no contiene la clave 'tablero'.")

    tablero = data["tablero"]

    if not tablero or not all(isinstance(fila, list) for fila in tablero):
        raise ValueError("El tablero debe ser una matriz válida.")

    columnas = len(tablero[0])
    if any(len(fila) != columnas for fila in tablero):
        raise ValueError("Todas las filas del tablero deben tener el mismo tamaño.")

    return tablero


def buscar_posicion(tablero, simbolo):
    posiciones = []

    for i, fila in enumerate(tablero):
        for j, celda in enumerate(fila):
            if celda == simbolo:
                posiciones.append((i, j))

    if len(posiciones) == 0:
        raise ValueError(f"No se encontró el símbolo '{simbolo}' en el tablero.")

    if len(posiciones) > 1:
        raise ValueError(f"Se encontró más de un símbolo '{simbolo}' en el tablero.")

    return posiciones[0]


def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def es_transitable(tablero, fila, col):
    return tablero[fila][col] in {".", "!", "B"}


def obtener_vecinos(tablero, nodo):
    fila, col = nodo
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    vecinos = []

    for df, dc in movimientos:
        nf, nc = fila + df, col + dc

        if 0 <= nf < len(tablero) and 0 <= nc < len(tablero[0]):
            if es_transitable(tablero, nf, nc):
                vecinos.append((nf, nc))

    return vecinos


def reconstruir_camino(padres, actual):
    camino = [actual]

    while actual in padres:
        actual = padres[actual]
        camino.append(actual)

    camino.reverse()
    return camino


def a_estrella(tablero, inicio, meta):
    abiertos = []
    heapq.heappush(abiertos, (heuristica(inicio, meta), 0, inicio))

    padres = {}
    costo_g = {inicio: 0}
    cerrados = set()

    while abiertos:
        _, g_actual, actual = heapq.heappop(abiertos)

        if actual in cerrados:
            continue

        if actual == meta:
            return reconstruir_camino(padres, actual)

        cerrados.add(actual)

        for vecino in obtener_vecinos(tablero, actual):
            nuevo_g = g_actual + 1

            if vecino not in costo_g or nuevo_g < costo_g[vecino]:
                costo_g[vecino] = nuevo_g
                padres[vecino] = actual
                f = nuevo_g + heuristica(vecino, meta)
                heapq.heappush(abiertos, (f, nuevo_g, vecino))

    return None


def marcar_camino(tablero, camino):
    for fila, col in camino:
        if tablero[fila][col] not in {"B", "!"}:
            tablero[fila][col] = "*"


def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))


tablero = leer_tablero("tablero.json")
inicio = buscar_posicion(tablero, "B")
meta = buscar_posicion(tablero, "!")

camino = a_estrella(tablero, inicio, meta)

if camino is None:
    print("No existe un camino desde Boome hasta la bomba.")
else:
    marcar_camino(tablero, camino)
    print("\nSimbologia\nB = posicion de Boome e inicio \n! = bomba/meta\n# = obstáculo \n. = espacio libre")
    print("\n--------------------------------------")
    print("Camino encontrado:")
    imprimir_tablero(tablero)
    print("\n--------------------------------------")
    print(f"Pasos: {len(camino) - 1}")