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


def subir_colina(grafo, inicio, meta, h):
    actual = inicio
    camino = [actual]

    while actual != meta:
        vecinos = grafo.get(actual, {})
        mejor = None
        mejor_valor = -1

        for vecino in vecinos:
            if vecino in camino:
                continue
            valor = h.get(vecino, 0)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor = vecino

        if mejor is None or mejor_valor <= h.get(actual, 0):
            return camino

        actual = mejor
        camino.append(actual)

    return camino


def main():
    grafo = leer_grafo("grafo2.json")
    if grafo is None:
        return

    heuristicas = {
        "J": {"A": 1, "B": 2, "C": 2, "D": 3, "E": 3, "F": 4, "G": 8, "H": 6, "I": 3, "J": 10},
        "G": {"A": 2, "B": 3, "C": 3, "D": 5, "E": 4, "F": 8, "G": 10, "H": 7, "I": 4, "J": 9},
        "E": {"A": 2, "B": 8, "C": 8, "D": 7, "E": 10, "F": 4, "G": 2, "H": 1, "I": 5, "J": 1},
        "F": {"A": 1, "B": 2, "C": 3, "D": 3, "E": 4, "F": 10, "G": 8, "H": 6, "I": 5, "J": 7}
    }

    meta = input("meta? (ej J): ").strip().upper()
    if meta not in grafo:
        print("Ese nodo no existe.")
        return
    if meta not in heuristicas:
        print("No hay heuristica para esa meta.")
        return

    camino = subir_colina(grafo, "A", meta, heuristicas[meta])
    print("Ruta: [" + ", ".join(camino) + "]")
    if camino[-1] == meta:
        print("Listo, llegue.")
    else:
        print("Se paro en:", camino[-1])


if __name__ == "__main__":
    main()
