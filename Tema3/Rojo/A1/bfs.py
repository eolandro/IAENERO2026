import json
from collections import deque
from pathlib import Path


def leer_grafo(nombre):
    ruta = Path(nombre)
    if not ruta.exists():
        print("No se encontro", nombre)
        return None

    with ruta.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("grafo", data)


def bfs(grafo, inicio, meta):
    cola = deque([inicio])
    padre = {inicio: None}

    while cola:
        actual = cola.popleft()
        if actual == meta:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            camino.reverse()
            return camino

        for vecino in sorted(grafo[actual].keys()):
            if vecino not in padre:
                padre[vecino] = actual
                cola.append(vecino)

    return None


def main():
    grafo = leer_grafo("grafo1.json")
    if grafo is None:
        return

    meta = input("meta? (ej ACC): ").strip().upper()
    if meta not in grafo:
        print("Ese nodo no existe.")
        return

    camino = bfs(grafo, "A", meta)
    if camino:
        print("Ruta BFS: [" + ", ".join(camino) + "]")
        print("pasos:", len(camino) - 1)
    else:
        print("No se encontro nada.")


if __name__ == "__main__":
    main()
