import json
from collections import deque
from pathlib import Path


# ***************** Usar el grafo ****************
def cargar_grafo(nombre_archivo):
    ruta = Path(nombre_archivo)

    if not ruta.exists():
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        return None

    with ruta.open("r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("grafo", data)


# ***************** Encontra el camino con primero profundida ****************
def camino_con_primero_profundidad(grafo, inicio, meta, visitados=None, camino=None):
    if visitados is None:
        visitados = set()
    
    if camino is None:
        camino = []
    
    visitados.add(inicio)
    camino.append(inicio)
    
    if inicio == meta:
        return camino.copy()
    
    for vecino in sorted(grafo[inicio].keys()):
        if vecino not in visitados:
            resultado = camino_con_primero_profundidad(grafo, vecino, meta, visitados, camino)
            if resultado is not None:
                return resultado
    camino.pop()
    return None


# ***************** Encontra el camino con primero archura ****************
def camino_con_primero_anchura(grafo, inicio, meta):
    cola = deque([inicio])
    visitados = {inicio}
    padres = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == meta:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]

        for vecino in sorted(grafo[actual].keys()):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)

    return None


# ***************** Encontra el camino con Subir la colina ****************
def subir_colina(grafo, inicio, meta, heuristica):
    actual = inicio
    camino = [actual]

    while actual != meta:
        vecinos = grafo.get(actual, {})
        mejor_vecino = None
        mejor_valor = -1

        for vecino in vecinos:
            if vecino not in camino:
                if heuristica.get(vecino, 0) > mejor_valor:
                    mejor_valor = heuristica.get(vecino, 0)
                    mejor_vecino = vecino

        if mejor_vecino is None or mejor_valor <= heuristica.get(actual, 0):
            return camino

        actual = mejor_vecino
        camino.append(actual)

    return camino


# ***************** Imprimir el grafo ****************
def imprimir_grafo(grafo):
    print(f"\n--------------- GRAFO UTILIZADO ---------------")
    for nodo in sorted(grafo.keys()):
        conexiones = []
        for vecino, peso in sorted(grafo[nodo].items()):
            conexiones.append(f"{vecino}({peso})")
        print(f"{nodo} -> " + ", ".join(conexiones))
    print("------------------------------------------------\n")


# ***************** Heurísticas por meta para grafo2 ****************
heuristicas = {
    "J": {"A": 1, "B": 2, "C": 2, "D": 3, "E": 3, "F": 4, "G": 8, "H": 6, "I": 3, "J": 10},
    "G": {"A": 2, "B": 3, "C": 3, "D": 5, "E": 4, "F": 8, "G": 10, "H": 7, "I": 4, "J": 9},
    "E": {"A": 2, "B": 8, "C": 8, "D": 7, "E": 10, "F": 4, "G": 2, "H": 1, "I": 5, "J": 1},
    "F": {"A": 1, "B": 2, "C": 3, "D": 3, "E": 4, "F": 10, "G": 8, "H": 6, "I": 5, "J": 7}
}


# ***************** Cargar ambos grafos ****************
grafo1 = cargar_grafo("grafo1.json")
grafo2 = cargar_grafo("grafo2.json")

if grafo1 is None:
    print("\nERROR! El archivo grafo1.json no está o está vacío.")
    exit()

if grafo2 is None:
    print("\nERROR! El archivo grafo2.json no está o está vacío.")
    exit()


# ***************** Menú Principal ****************
while True:
    print("\n------ OPCIONES DE BUSQUEDA ------\n")
    opcion = input("\n1. Primero en Profundidad \n2. Primero en Anchura \n3. Subir la Colina \n4. Salir\n> ")
    match opcion:
        case "1": #Primero en profunidad
            imprimir_grafo(grafo1)
            meta = input("¿A qué nodo quieres llegar desde A?> ").upper()
            if meta not in grafo1:
                print("El nodo no existe en el grafo1.")
            else:
                camino = camino_con_primero_profundidad(grafo1, "A", meta)
                if camino:
                    print("\nCamino encontrado con Primero en Profundidad:", " -> ".join(camino))
                else:
                    print("\nNo se encontró camino con Primero en Profundidad")

        case "2":#Primero en anchura
            imprimir_grafo(grafo1)
            meta = input("¿A qué nodo quieres llegar desde A?> ").upper()
            if meta not in grafo1:
                print("El nodo no existe en el grafo1.")
            else:
                camino = camino_con_primero_anchura(grafo1, "A", meta)
                if camino:
                    print("\nCamino encontrado con Primero en Anchura:", " -> ".join(camino))
                else:
                    print("\nNo se encontró camino con Primero en Anchura.")

        case "3":#Subir la colina
            imprimir_grafo(grafo2)
            meta = input("¿A qué nodo quieres llegar desde A?> ").upper()
            if meta not in grafo2:
                print("El nodo no existe en el grafo2.")
            elif meta not in heuristicas:
                print("No hay heurística definida para ese nodo meta.")
            else:
                camino = subir_colina(grafo2, "A", meta, heuristicas[meta])
                print("\nCamino encontrado con Subir la colina:", " -> ".join(camino))
                if camino[-1] != meta:
                    print("Subir la colina no llegó a la meta")

        case "4":
            print("\nPrograma finalizado.\nBye bye Kya!!!")
            break

        case _:
            print("\nERROR! OPCION NO DISPONIBLE")