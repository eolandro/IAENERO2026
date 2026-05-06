import json
from pathlib import Path


def leer_grafo(nombre):
    ruta = Path(nombre)
    if not ruta.exists():
        print("No se encontro", nombre)
        return None

    with ruta.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("grafo", data)


def dfs(grafo, inicio, meta, visitados=None, camino=None):
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []

    visitados.add(inicio)
    camino.append(inicio)

    if inicio == meta:
        return camino[:]

    for vecino in sorted(grafo[inicio].keys()):
        if vecino not in visitados:
            resultado = dfs(grafo, vecino, meta, visitados, camino)
            if resultado is not None:
                return resultado

    camino.pop()
    return None


def main():
    grafo = leer_grafo("grafo1.json")
    if grafo is None:
        return

    meta = input("meta? (ej ACC): ").strip().upper()
    if meta not in grafo:
        print("Ese nodo no existe.")
        return

    camino = dfs(grafo, "A", meta)
    if camino:
        print("Ruta DFS: [" + ", ".join(camino) + "]")
        print("longitud:", len(camino) - 1)
    else:
        print("No se encontro nada.")


if __name__ == "__main__":
    main()
