import heapq
import json
from pathlib import Path


# Mapa
def col_mkr(ultimo):
    return [chr(x) for x in range(ord('A'), ord(ultimo) + 1)]


# Identificadores
identificadores = {
    0: ' ',  # Camino libre
    1: 'B',  # Boome
    2: 'x',  # Bomba yucateca
    3: '█',  # Caja/bloqueo/pared/etc...
    4: '·',  # Ruta trazada
}

# Configuración
cols = col_mkr('F')


class Mapa:
    def __init__(self, archivo_mapa='map.json'):
        self.archivo = archivo_mapa
        self.mapa = []

    def actualizar(self, mapa):
        self.mapa = mapa

    def cargar(self):
        archivo = Path(self.archivo)
        if archivo.exists():
            with open(archivo, encoding='utf-8') as info:
                self.mapa = json.load(info)
                return self.mapa
        return None

    def mostrar(self):
        print(' ' * 3 + ' '.join(cols))
        for i, fila in enumerate(self.mapa, start=1):
            linea = ' '.join(identificadores[fila[col]] for col in cols)
            print(f'{i:02} {linea}')


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def trazar_camino(nodo_padre, objetivo):
    camino = [objetivo]

    while camino[-1] in nodo_padre:
        camino.append(nodo_padre[camino[-1]])
    camino.reverse()

    return camino


class PathfinderA:
    def __init__(self, mapa, boome, bomba):
        self.mapa = mapa
        self.boome = boome
        self.bomba = bomba

    def obtener_parientes(self, nodo):
        f, c = nodo
        posiciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        parientes = []

        for df, dc in posiciones:
            nf, nc = f + df, c + dc
            if 0 <= nf < len(self.mapa) and 0 <= nc < len(cols):
                if self.mapa[nf][cols[nc]] in {0, 1, 2}:
                    parientes.append((nf, nc))

        return parientes

    def trazador_estrella(self):
        n_actuales = []
        n_vistos = set()
        n_padre = {}
        costo = {self.boome: 0}

        heapq.heappush(n_actuales, (heuristic(self.boome, self.bomba), 0, self.boome))

        while n_actuales:
            _, grafo, nodo = heapq.heappop(n_actuales)

            if nodo in n_vistos:
                continue

            if nodo == self.bomba:
                return trazar_camino(n_padre, nodo)

            n_vistos.add(nodo)

            for relativo in self.obtener_parientes(nodo):
                nodo_nuevo = grafo + 1

                if relativo not in costo or nodo_nuevo < costo[relativo]:
                    costo[relativo] = nodo_nuevo
                    n_padre[relativo] = nodo
                    f = nodo_nuevo + heuristic(relativo, self.bomba)
                    heapq.heappush(n_actuales, (f, nodo_nuevo, relativo))

        return None


def buscador(mapa, elemento):
    posiciones = []

    for i, fila in enumerate(mapa):
        for j, clave in enumerate(fila.keys()):
            if fila[clave] == elemento:
                posiciones.append((i, j))

    cantidad = len(posiciones)

    if cantidad == 0 or cantidad > 1:
        raise Exception(
            f'El elemento "{identificadores[elemento]}" no se encuentra o está duplicado.\n'
            f'{identificadores[elemento]}: {cantidad}'
        )

    return posiciones[0]


def main():
    """
    **Boome pathfinding**

    - Nombre: Pathfinding A*
    - Descripción: Realizar un programa que aplique A* en un escenario específico.
    - Notas: Último programa de boome lee el tablero desde un archivo y busca la bomba con A*.
    - Elementos Clave: Heurística, A*, pathfinding.
    - SEAES_CACEI: CD1-3,CD2-3,AE1,AE2, Compromiso con responsabilidad Social.

    **R008 - 15**

    - Descripción: Aplicación de pathfinding A*.
    - Restricciones: NA

    :return: None
    """
    mapa = Mapa(archivo_mapa='map.json')
    inicio = mapa.cargar()

    if inicio is None:
        raise Exception('No se encontró el archivo map.json')

    boome = buscador(inicio, 1)
    bomba = buscador(inicio, 2)

    print('Mapa original cargado:')
    mapa.mostrar()

    ruta = PathfinderA(inicio, boome, bomba)
    camino = ruta.trazador_estrella()

    if camino is None:
        print('No se encontró ruta.')
        return

    print('\nRuta encontrada:')
    mapa_ruta = [dict(fila) for fila in inicio]
    for f, c in camino[1:-1]:
        mapa_ruta[f][cols[c]] = 4

    print(' ' * 3 + ' '.join(cols))
    for i, fila in enumerate(mapa_ruta, start=1):
        linea = ' '.join(identificadores[fila[col]] for col in cols)
        print(f'{i:02} {linea}')

    print(f'Pasos realizados: {len(camino)}')


if __name__ == "__main__":
    main()
