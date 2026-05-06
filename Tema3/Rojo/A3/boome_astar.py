import json
import heapq
from pathlib import Path


def leer_tablero(nombre="boome_tablero.json"):
    ruta = Path(nombre)
    if not ruta.exists():
        print("No se encontro", nombre)
        return None

    with ruta.open("r", encoding="utf-8") as archivo:
        data = json.load(archivo)

    return data.get("tablero")


def buscar(tablero, simbolo):
    for i, fila in enumerate(tablero):
        for j, celda in enumerate(fila):
            if celda == simbolo:
                return (i, j)
    return None


def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def vecinos(tablero, nodo):
    fila, col = nodo
    movs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    res = []
    for df, dc in movs:
        nf, nc = fila + df, col + dc
        if 0 <= nf < len(tablero) and 0 <= nc < len(tablero[0]):
            if tablero[nf][nc] in {".", "B", "!"}:
                res.append((nf, nc))
    return res


def a_estrella(tablero, inicio, meta):
    abiertos = [(heuristica(inicio, meta), 0, inicio)]
    padre = {}
    costo = {inicio: 0}
    cerrados = set()

    while abiertos:
        _, g, actual = heapq.heappop(abiertos)
        if actual in cerrados:
            continue
        if actual == meta:
            return reconstruir(padre, actual)
        cerrados.add(actual)

        for v in vecinos(tablero, actual):
            nuevo_g = g + 1
            if v not in costo or nuevo_g < costo[v]:
                costo[v] = nuevo_g
                padre[v] = actual
                f = nuevo_g + heuristica(v, meta)
                heapq.heappush(abiertos, (f, nuevo_g, v))

    return None


def reconstruir(padre, actual):
    camino = [actual]
    while actual in padre:
        actual = padre[actual]
        camino.append(actual)
    camino.reverse()
    return camino


def marcar(tablero, camino):
    for f, c in camino:
        if tablero[f][c] not in {"B", "!"}:
            tablero[f][c] = "*"


def imprimir(tablero):
    cols = len(tablero[0])
    print("   " + " ".join(str(i) for i in range(cols)))
    for i, fila in enumerate(tablero):
        print("%2d " % i + " ".join(fila))


def main():
    tablero = leer_tablero("boome_tablero.json")
    if not tablero:
        return

    inicio = buscar(tablero, "B")
    meta = buscar(tablero, "!")
    if inicio is None or meta is None:
        print("Falta B o ! en el tablero.")
        return

    camino = a_estrella(tablero, inicio, meta)
    if camino is None:
        print("No hay camino.")
        return

    marcar(tablero, camino)
    print("Leyenda:")
    print("B inicio, ! meta, # muro, . libre, * camino")
    imprimir(tablero)
    print("Pasos:", len(camino) - 1)


if __name__ == "__main__":
    main()