"""Búsqueda en grafos jerárquicos — DFS y BFS.

Carga un grafo desde un archivo YAML (árbol jerárquico) y permite
ejecutar consultas interactivas con los algoritmos DFS y BFS.

Uso: python busqueda.py grafo.yaml
"""

import argparse
from collections import deque
from ruamel.yaml import YAML

# Grafo global cargado desde el archivo YAML
grafo = {}


def cargar_grafo(archivo):
    """Carga y retorna un grafo desde un archivo YAML."""
    yaml = YAML()
    with open(archivo) as f:
        return yaml.load(f)


def buscar_subarbol(arbol, nodo):
    """Busca un nodo en el árbol y retorna su subárbol {nodo: hijos}.

    Recorre recursivamente el árbol jerárquico hasta encontrar
    la clave que coincida con el nodo buscado.
    Retorna None si el nodo no existe en el árbol.
    """
    # Caso base: el nodo es una clave directa del nivel actual
    if nodo in arbol:
        return {nodo: arbol[nodo] or {}}

    # Caso recursivo: buscar en los hijos de cada nodo
    for clave, hijos in arbol.items():
        if hijos:
            resultado = buscar_subarbol(hijos, nodo)
            if resultado is not None:
                return resultado
    return None


def dfs(inicio, destino):
    """Búsqueda en profundidad (DFS) — explora rama por rama.

    Usa una pila (LIFO) para recorrer el árbol desde el nodo inicio.
    Retorna True si el nodo destino es alcanzable, False en caso contrario.
    """
    # Localizar el subárbol del nodo de inicio
    subarbol = buscar_subarbol(grafo, inicio)
    if subarbol is None:
        print(f"  Nodo '{inicio}' no encontrado en el grafo.")
        return False

    # Pila con tuplas (nombre_nodo, diccionario_hijos)
    pila = [(inicio, subarbol[inicio])]

    while pila:
        # Sacar el último elemento agregado (profundidad primero)
        nodo, hijos = pila.pop()
        print(f"  Visitando: {nodo}")

        # Verificar si llegamos al destino
        if nodo == destino:
            return True

        # Agregar hijos a la pila (en reversa para visitar en orden natural)
        if hijos:
            for hijo in reversed(list(hijos.keys())):
                pila.append((hijo, hijos[hijo] or {}))

    return False


def bfs(inicio, destino):
    """Búsqueda en anchura (BFS) — explora nivel por nivel.

    Usa una cola (FIFO) para recorrer el árbol desde el nodo inicio.
    Retorna True si el nodo destino es alcanzable, False en caso contrario.
    """
    # Localizar el subárbol del nodo de inicio
    subarbol = buscar_subarbol(grafo, inicio)
    if subarbol is None:
        print(f"  Nodo '{inicio}' no encontrado en el grafo.")
        return False

    # Cola con tuplas (nombre_nodo, diccionario_hijos)
    cola = deque([(inicio, subarbol[inicio])])

    while cola:
        # Sacar el primer elemento agregado (anchura primero)
        nodo, hijos = cola.popleft()
        print(f"  Visitando: {nodo}")

        # Verificar si llegamos al destino
        if nodo == destino:
            return True

        # Agregar hijos al final de la cola
        if hijos:
            for hijo, subhijos in hijos.items():
                cola.append((hijo, subhijos or {}))

    return False


def main():
    """Punto de entrada: carga el grafo e inicia el ciclo interactivo."""
    global grafo

    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Búsqueda DFS y BFS en grafos jerárquicos YAML"
    )
    parser.add_argument("archivo", help="Archivo YAML con el grafo")
    args = parser.parse_args()

    # Cargar el grafo desde el archivo
    grafo = cargar_grafo(args.archivo)
    print(f"Grafo cargado desde: {args.archivo}")
    print("Funciones: dfs(inicio, destino), bfs(inicio, destino)")
    print("Escribe 'salir' para terminar.\n")

    # Ciclo interactivo — evalúa expresiones del usuario
    while True:
        try:
            entrada = input(">>> ").strip()

            if entrada.lower() == "salir":
                print("Fin del programa.")
                break
            if not entrada:
                continue

            # Evaluar la expresión ingresada (ej: dfs("A", "D"))
            resultado = eval(entrada)
            print(f"Resultado: {resultado}\n")

        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
