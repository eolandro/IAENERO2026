import json
import argparse
import random


# Carga el grafo desde un archivo JSON y lo retorna como diccionario
def cargar_grafo(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        grafo = json.load(archivo)
    return grafo


# Obtiene los vecinos del nodo actual con sus pesos
def obtener_vecinos(grafo, nodo):
    if nodo in grafo:
        return grafo[nodo]
    return {}

def subir_colina(grafo, inicio, objetivo):
    nodo_actual = inicio
    visitados_recientes = []  # Últimos 2 nodos visitados para evitar ciclos

    print(f"\n--- Inicio de búsqueda Hill Climbing ---")
    print(f"    Nodo inicio: {inicio}")
    print(f"    Nodo objetivo: {objetivo}\n")

    while True:
        print(f"  Nodo actual: {nodo_actual}")

        # Si llegamos al objetivo, terminamos con éxito
        if nodo_actual == objetivo:
            print(f"\n  ¡Objetivo '{objetivo}' alcanzado!\n")
            return True

        # Obtener vecinos del nodo actual
        vecinos = obtener_vecinos(grafo, nodo_actual)

        if not vecinos:
            print(f"  El nodo '{nodo_actual}' no tiene vecinos. Búsqueda terminada.\n")
            return None

        # Filtrar vecinos que estén en los últimos 2 visitados (evitar ciclos)
        vecinos_disponibles = {
            nodo: peso
            for nodo, peso in vecinos.items()
            if nodo not in visitados_recientes
        }

        if not vecinos_disponibles:
            print(f"  Todos los vecinos ya fueron visitados recientemente. Búsqueda terminada.\n")
            return None

        # Mostrar vecinos disponibles
        print(f"  Vecinos disponibles: {vecinos_disponibles}")

        # Encontrar el peso máximo entre los vecinos disponibles
        peso_maximo = max(vecinos_disponibles.values())

        # Obtener todos los vecinos que tienen el peso máximo (por si hay empate)
        mejores = [
            nodo for nodo, peso in vecinos_disponibles.items()
            if peso == peso_maximo
        ]

        # Si hay empate, elegir al azar; si no, tomar el único mejor
        if len(mejores) > 1:
            elegido = random.choice(mejores)
            print(f"  Empate entre {mejores}, se eligió al azar: {elegido} (peso: {peso_maximo})")
        else:
            elegido = mejores[0]
            print(f"  Elegido: {elegido} (peso: {peso_maximo})")

        # Actualizar la lista de visitados recientes (máximo 2)
        visitados_recientes.append(nodo_actual)
        if len(visitados_recientes) > 2:
            visitados_recientes.pop(0)

        # Avanzar al nodo elegido
        nodo_actual = elegido
        print()


# Muestra los nodos disponibles en el grafo
def mostrar_nodos(grafo):
    print(f"\nNodos del grafo: {list(grafo.keys())}\n")


# Bucle interactivo para que el usuario ejecute consultas con eval()
def bucle_interactivo(grafo):
    print("\n")
    print("Funciones disponibles:")
    print("  subir_colina(grafo, 'inicio', 'objetivo')")
    print("  obtener_vecinos(grafo, 'nodo')")
    print("  mostrar_nodos(grafo)")
    print("Escribe 'salir' para terminar.\n")

    while True:
        try:
            entrada = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if entrada.strip().lower() == "salir":
            print("¡Hasta luego!")
            break

        if not entrada.strip():
            continue

        try:
            resultado = eval(entrada)
            if resultado is not None:
                print(f"Resultado: {resultado}")
        except Exception as error:
            print(f"Error: {error}")


# Punto de entrada principal
def main():
    # Configurar argparse para recibir el archivo JSON como argumento
    parser = argparse.ArgumentParser(
        description="Búsqueda local: Subir la colina (Hill Climbing) en un grafo dirigido ponderado."
    )
    parser.add_argument(
        "archivo",
        help="Ruta al archivo JSON que contiene el grafo."
    )
    args = parser.parse_args()

    # Cargar el grafo
    grafo = cargar_grafo(args.archivo)
    print(f"Grafo cargado desde: {args.archivo}")
    mostrar_nodos(grafo)

    # Iniciar el bucle interactivo
    bucle_interactivo(grafo)


if __name__ == "__main__":
    main()
