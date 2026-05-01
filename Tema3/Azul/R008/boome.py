import json
import heapq
import sys

# Cargar el tablero desde un archivo json
def cargar_tablero(ruta_archivo):
    try:
        with open(ruta_archivo, "r") as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo '{ruta_archivo}'")
        sys.exit(1)

# Buscar la posicion de un caracter en el tablero
def buscar_posicion(tablero, caracter):
    for fila in range(len(tablero)):
        for col in range(len(tablero[fila])):
            if tablero[fila][col] == caracter:
                return (fila, col)
    return None

# Colocar inicio y destino en el tablero
def preparar_tablero(datos):
    tablero = datos["tablero"]
    pos_inicio = datos["posicion_inicio"]
    pos_destino = datos["posicion_destino"]
    tablero[pos_inicio[0]][pos_inicio[1]] = datos["inicio"]
    tablero[pos_destino[0]][pos_destino[1]] = datos["destino"]
    return tablero

# Imprimir el tablero en consola
def imprimir_tablero(tablero):
    print("    " + "  ".join(f"{c:2d}" for c in range(len(tablero[0]))))
    print("   " + "---" * len(tablero[0]))
    for i, fila in enumerate(tablero):
        print(f"{i:2d} | " + "  ".join(f"{celda:>2}" for celda in fila))
    print()

# Distancia estimada al destino
def heuristica_manhattan(nodo, destino):
    return abs(nodo[0] - destino[0]) + abs(nodo[1] - destino[1])

# Obtener vecinos validos (4 direcciones: arriba, abajo, izquierda, derecha)
def obtener_vecinos(tablero, nodo):
    filas = len(tablero)
    columnas = len(tablero[0])
    fila, col = nodo
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    vecinos = []
    for df, dc in direcciones:
        nf, nc = fila + df, col + dc
        # Verificar limites y que no sea pared
        if 0 <= nf < filas and 0 <= nc < columnas and tablero[nf][nc] != "[]":
            vecinos.append((nf, nc))
    return vecinos

# Reconstruir el camino desde el destino hasta el inicio
def reconstruir_camino(padres, actual):
    camino = [actual]
    while actual in padres:
        actual = padres[actual]
        camino.append(actual)
    camino.reverse()
    return camino

# Algoritmo A* para encontrar la ruta optima
def busqueda_a_estrella(tablero, inicio, destino):
    # Cola de prioridad: (f_score, nodo)
    conjunto_abierto = []
    heapq.heappush(conjunto_abierto, (0, inicio))

    # Nodos padre para reconstruir el camino
    padres = {}

    # g_score: costo real desde el inicio hasta cada nodo
    g_score = {}
    g_score[inicio] = 0

    # f_score: g_score + heuristica
    f_score = {}
    f_score[inicio] = heuristica_manhattan(inicio, destino)

    # Conjunto de nodos visitados para no revisitar
    visitados = set()

    while conjunto_abierto:
        # Obtener el nodo con menor f_score
        _, actual = heapq.heappop(conjunto_abierto)

        # Si ya fue visitado, saltar
        if actual in visitados:
            continue

        # Si llegamos al destino, reconstruir camino
        if actual == destino:
            return reconstruir_camino(padres, actual)

        # Marcar como visitado
        visitados.add(actual)

        # Explorar vecinos
        for vecino in obtener_vecinos(tablero, actual):
            if vecino in visitados:
                continue

            # Costo tentativo (cada movimiento cuesta 1)
            g_tentativo = g_score[actual] + 1

            # Si encontramos un camino mejor al vecino
            if g_tentativo < g_score.get(vecino, float("inf")):
                padres[vecino] = actual
                g_score[vecino] = g_tentativo
                f_score[vecino] = g_tentativo + heuristica_manhattan(vecino, destino)
                heapq.heappush(conjunto_abierto, (f_score[vecino], vecino))

    # No se encontro ruta
    return None

# Marcar el camino en el tablero con * 
def marcar_camino(tablero, camino, inicio, destino):
    # Copiar el tablero para no modificar el original
    tablero_marcado = [fila[:] for fila in tablero]
    for paso in camino:
        fila, col = paso
        if paso != inicio and paso != destino:
            tablero_marcado[fila][col] = "*"
    return tablero_marcado

# Imprimir las coordenadas de cada paso del camino
def imprimir_coordenadas(camino):
    print("Coordenadas del camino:")
    for i, paso in enumerate(camino):
        print(f"  Paso {i}: ({paso[0]}, {paso[1]})")
    print(f"\nTotal de pasos: {len(camino) - 1}")

def main():
    archivo_tablero = "tablero.json"

    print("=" * 25)
    print("  PATHFINDING A* - BOOME")
    print("=" * 25)
    datos = cargar_tablero(archivo_tablero)

    tablero = preparar_tablero(datos)

    inicio = buscar_posicion(tablero, datos["inicio"])
    destino = buscar_posicion(tablero, datos["destino"])

    if inicio is None:
        print("Error: No se encontro la posicion de inicio (B) en el tablero")
        sys.exit(1)
    if destino is None:
        print("Error: No se encontro la posicion de destino (1) en el tablero")
        sys.exit(1)

    print(f"Inicio encontrado en: ({inicio[0]}, {inicio[1]})")
    print(f"Destino encontrado en: ({destino[0]}, {destino[1]})")

    print("\n--- TABLERO INICIAL ---")
    imprimir_tablero(tablero)

    camino = busqueda_a_estrella(tablero, inicio, destino)

    if camino is None:
        print("No se encontro una ruta al destino.")
        sys.exit(0)

    print("Ruta encontrada!\n")

    tablero_marcado = marcar_camino(tablero, camino, inicio, destino)

    print("--- TABLERO CON RUTA ---")
    imprimir_tablero(tablero_marcado)

    imprimir_coordenadas(camino)

if __name__ == "__main__":
    main()
