import json
import heapq
import os

def cargar(ruta):
    with open(ruta, "r") as f:
        return json.load(f)

def obtener_grid(data):
    # Para soportar ambos formatos
    if isinstance(data, dict):
        return data["grid"]
    return data

def localizar(mapa, valor):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == valor:
                return (i, j)
    return None

def preparar_mapa(data):
    resultado = []
    for fila in data:
        nueva = []
        for celda in fila:
            if celda == 1:
                nueva.append(1)
            else:
                nueva.append(0)
        resultado.append(nueva)
    return resultado

def vecinos(pos, mapa):
    direcciones = [
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(-1,1),(1,-1),(1,1)
    ]

    resultado = []

    for dx, dy in direcciones:
        x = pos[0] + dx
        y = pos[1] + dy

        if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):
            if mapa[x][y] == 0:
                costo = 14 if dx != 0 and dy != 0 else 10
                resultado.append(((x, y), costo))

    return resultado

def heuristica(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return 10 * (dx + dy)


def reconstruir(came_from, actual):
    ruta = [actual]
    while actual in came_from:
        actual = came_from[actual]
        ruta.append(actual)
    return ruta[::-1]

def a_star(mapa, inicio, fin):
    open_heap = []
    heapq.heappush(open_heap, (0, inicio))

    came_from = {}

    g_score = {inicio: 0}
    f_score = {inicio: heuristica(inicio, fin)}

    cerrados = set()

    while open_heap:
        _, actual = heapq.heappop(open_heap)

        if actual == fin:
            return reconstruir(came_from, actual), g_score[actual]

        cerrados.add(actual)

        for vecino, costo in vecinos(actual, mapa):
            if vecino in cerrados:
                continue

            nuevo_g = g_score[actual] + costo

            if vecino not in g_score or nuevo_g < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = nuevo_g
                f_score[vecino] = nuevo_g + heuristica(vecino, fin)

                heapq.heappush(open_heap, (f_score[vecino], vecino))

    return None, None

def imprimir_mapa_con_ruta(grid, ruta):
    copia = [fila[:] for fila in grid]

    for x, y in ruta:
        if copia[x][y] == 0:
            copia[x][y] = "*"

    print("\nMAPA CON RUTA:\n")
    for fila in copia:
        print(" ".join(str(c) for c in fila))

# ----------------------------------------- MAIN -----------------------------------------#

ruta_json = os.path.join(os.path.dirname(__file__), "tablero.json")
data = cargar(ruta_json)
grid = obtener_grid(data)
inicio = localizar(grid, "I")
fin = localizar(grid, "F")

if inicio is None or fin is None:
    print("Error: No se encontró 'I' o 'F' en el tablero")
    exit()

mapa = preparar_mapa(grid)
ruta, costo = a_star(mapa, inicio, fin)

print("\n" + "="*60)

if ruta:
    print("RUTA OPTIMA ENCONTRADA\n")

    for i, p in enumerate(ruta):
        print(f"[{i}] -> {p}")

    print("\n--- DETALLES ---")
    print(f"Total pasos: {len(ruta)-1}")
    print(f"Costo acumulado: {costo}")

    imprimir_mapa_con_ruta(grid, ruta)

else:
    print("No existe ruta posible")

print("="*60)