from __future__ import annotations

import heapq
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ruamel.yaml import YAML

# ═══════════════════════════════════════════════════════════════════════════════
#  Tipos y constantes
# ═══════════════════════════════════════════════════════════════════════════════

Celda   = tuple[int, int]          # (fila, columna)
Tablero = list[list[int]]

# Movimientos en 4 direcciones: arriba, abajo, izquierda, derecha
MOVIMIENTOS_4: list[Celda] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Movimientos en 8 direcciones (incluye diagonales)
MOVIMIENTOS_8: list[Celda] = [
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1),
]

# Costo de movimiento diagonal (√2 ≈ 1.414)
COSTO_DIAGONAL = 1.414

# Representación visual de cada tipo de celda (emojis de ancho doble)
SIMBOLOS: dict[int, str] = {
    0: "  ",   # libre         (2 espacios para igualar ancho emoji)
    1: "🟥",   # obstáculo
    2: "🤖",   # inicio (Boome)
    3: "🚩",   # destino / fin
    4: "🟡",   # camino encontrado
}


# ═══════════════════════════════════════════════════════════════════════════════
#  Nodo de búsqueda
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(order=True)
class Nodo:
    """Nodo utilizado en la cola de prioridad del algoritmo A*.

    El campo ``f`` (f = g + h) es el único usado para comparación,
    lo que permite ordenar eficientemente en el heap.

    Atributos:
        f       : Coste total estimado (g + h). Determina la prioridad.
        pos     : Posición (fila, columna) en el tablero.
        g       : Coste real acumulado desde el inicio hasta este nodo.
        padre   : Referencia al nodo predecesor (para reconstruir el camino).
    """
    f:      float         = field(compare=True)
    pos:    Celda         = field(compare=False)
    g:      float         = field(compare=False, default=0.0)
    padre:  Optional["Nodo"] = field(compare=False, default=None, repr=False)


# ═══════════════════════════════════════════════════════════════════════════════
#  Carga del tablero
# ═══════════════════════════════════════════════════════════════════════════════

def cargar_tablero(ruta: str | Path) -> Tablero:
    """Carga la cuadrícula desde un archivo YAML.

    El archivo debe contener una clave ``grid`` con una lista de listas
    de enteros.

    Args:
        ruta: Ruta al archivo ``.yaml`` o ``.yml``.

    Returns:
        Tablero como lista de listas de enteros.

    Raises:
        FileNotFoundError : Si el archivo no existe.
        KeyError          : Si el YAML no contiene la clave ``grid``.
        ValueError        : Si el tablero está vacío o mal formado.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"¿Que paso master :|? Archivo no encontrado :c '{ruta}'")

    parser = YAML()
    datos = parser.load(ruta)

    if "grid" not in datos:
        raise KeyError("¿Que paso master? :| El archivo YAML no contiene la clave 'grid'.")

    tablero: Tablero = datos["grid"]

    if not tablero or not tablero[0]:
        raise ValueError("No hay NADA en el tablero, solo polvo.")

    # Verificar que todas las filas tienen el mismo ancho
    ancho = len(tablero[0])
    for i, fila in enumerate(tablero):
        if len(fila) != ancho:
            raise ValueError(
                f"Fila {i} tiene {len(fila)} columnas; "
                f"se esperaban {ancho}."
            )

    return tablero


# ═══════════════════════════════════════════════════════════════════════════════
#  Localización de celdas especiales
# ═══════════════════════════════════════════════════════════════════════════════

def localizar_celda(tablero: Tablero, objetivo: int) -> Optional[Celda]:
    """Devuelve las coordenadas (fila, col) de la primera celda con ``objetivo``.

    Args:
        tablero : Cuadrícula a buscar.
        objetivo: Valor entero a localizar (p. ej. 2 para inicio, 3 para fin).

    Returns:
        Tupla ``(fila, columna)`` o ``None`` si no se encontró.
    """
    for fila_idx, fila in enumerate(tablero):
        for col_idx, valor in enumerate(fila):
            if valor == objetivo:
                return (fila_idx, col_idx)
    return None


# ═══════════════════════════════════════════════════════════════════════════════
#  Heurísticas
# ═══════════════════════════════════════════════════════════════════════════════

def heuristica_manhattan(a: Celda, b: Celda) -> float:
    """Distancia Manhattan. Admisible para movimientos en 4 direcciones."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristica_chebyshev(a: Celda, b: Celda) -> float:
    """Distancia Chebyshev. Admisible para movimientos en 8 direcciones."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def heuristica_euclidea(a: Celda, b: Celda) -> float:
    """Distancia Euclidea. Más precisa pero puede sobreestimar en grillas enteras."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# ═══════════════════════════════════════════════════════════════════════════════
#  Exploración de vecinos
# ═══════════════════════════════════════════════════════════════════════════════

def vecinos_validos(
    pos: Celda,
    tablero: Tablero,
    diagonal: bool = False,
) -> list[tuple[Celda, float]]:
    """Devuelve las celdas adyacentes transitables con su costo de movimiento.

    Args:
        pos      : Posición actual (fila, columna).
        tablero  : Cuadrícula del mapa.
        diagonal : Si es True, incluye las 4 diagonales además de los 4 ejes.

    Returns:
        Lista de tuplas ``(celda_vecina, costo)``.
    """
    filas, cols = len(tablero), len(tablero[0])
    movimientos = MOVIMIENTOS_8 if diagonal else MOVIMIENTOS_4
    resultado: list[tuple[Celda, float]] = []

    for df, dc in movimientos:
        nf, nc = pos[0] + df, pos[1] + dc
        if 0 <= nf < filas and 0 <= nc < cols and tablero[nf][nc] != 1:
            costo = COSTO_DIAGONAL if (df != 0 and dc != 0) else 1.0
            resultado.append(((nf, nc), costo))

    return resultado


# ═══════════════════════════════════════════════════════════════════════════════
#  Algoritmo A*
# ═══════════════════════════════════════════════════════════════════════════════

def buscar_ruta(
    tablero: Tablero,
    origen:  Celda,
    destino: Celda,
    diagonal: bool = False,
    heuristica = heuristica_manhattan,
) -> Optional[list[Celda]]:
    """Ejecuta A* y devuelve la lista ordenada de celdas del camino óptimo.

    Implementación con:
      • ``heapq``       → cola de prioridad O(log n) en lugar de list + min O(n).
      • Conjunto cerrado → evita reprocesar nodos ya visitados.
      • Nodo padre      → reconstrucción O(k) del camino (k = longitud del camino).

    Args:
        tablero    : Cuadrícula del mapa.
        origen     : Celda de inicio.
        destino    : Celda objetivo.
        diagonal   : Si se permiten movimientos en diagonal.
        heuristica : Función h(a, b) → float. Por defecto Manhattan.

    Returns:
        Lista de celdas desde ``origen`` hasta ``destino`` (inclusivos),
        o ``None`` si no existe camino.

    Complejidad:
        Tiempo : O(E log V)  — E aristas, V vértices (celdas libres).
        Espacio: O(V)        — para el heap y los diccionarios de costes.
    """
    nodo_inicio = Nodo(
        f=heuristica(origen, destino),
        pos=origen,
        g=0.0,
    )

    # Cola de prioridad (min-heap por f = g + h)
    heap: list[Nodo] = [nodo_inicio]

    # Mejor coste-g conocido para cada celda
    mejor_g: dict[Celda, float] = {origen: 0.0}

    # Conjunto cerrado: nodos ya expandidos
    visitados: set[Celda] = set()

    while heap:
        actual = heapq.heappop(heap)

        # Ignorar entradas obsoletas en el heap (lazy deletion)
        if actual.pos in visitados:
            continue
        visitados.add(actual.pos)

        # ¡Llegamos al destino!
        if actual.pos == destino:
            return _reconstruir_ruta(actual)

        # Expandir vecinos
        for vecino_pos, costo_mov in vecinos_validos(actual.pos, tablero, diagonal):
            if vecino_pos in visitados:
                continue

            nuevo_g = actual.g + costo_mov

            # Solo agregar si encontramos un camino más corto
            if nuevo_g < mejor_g.get(vecino_pos, float("inf")):
                mejor_g[vecino_pos] = nuevo_g
                h = heuristica(vecino_pos, destino)
                nodo_vecino = Nodo(
                    f=nuevo_g + h,
                    pos=vecino_pos,
                    g=nuevo_g,
                    padre=actual,
                )
                heapq.heappush(heap, nodo_vecino)

    return None  # No existe camino


def _reconstruir_ruta(nodo_destino: Nodo) -> list[Celda]:
    """Reconstruye el camino remontando la cadena de padres.

    Args:
        nodo_destino: Nodo final con referencias al padre.

    Returns:
        Lista de celdas en orden inicio → destino.
    """
    ruta: list[Celda] = []
    nodo: Optional[Nodo] = nodo_destino
    while nodo is not None:
        ruta.append(nodo.pos)
        nodo = nodo.padre
    return ruta[::-1]


# ═══════════════════════════════════════════════════════════════════════════════
#  Visualización en consola
# ═══════════════════════════════════════════════════════════════════════════════

def dibujar_tablero(
    tablero: Tablero,
    ruta: Optional[list[Celda]] = None,
    mostrar_coords: bool = False,
) -> None:
    """Imprime el tablero con bordes Unicode y emojis.

    Los emojis tienen ancho visual doble (2 columnas de terminal), por lo que
    el separador de celda se ajusta a 4 caracteres para mantener alineacion.

    Si se provee ``ruta``, marca el camino sin modificar el tablero original.

    Args:
        tablero        : Cuadricula original.
        ruta           : Lista de celdas del camino (opcional).
        mostrar_coords : Si True, imprime encabezados de fila/columna.
    """
    if ruta:
        tablero_vis: Tablero = deepcopy(tablero)
        for paso in ruta[1:-1]:
            tablero_vis[paso[0]][paso[1]] = 4
    else:
        tablero_vis = tablero

    cols = len(tablero_vis[0])

    borde_top = "\u250c" + "\u2500\u2500\u2500\u2500\u252c" * (cols - 1) + "\u2500\u2500\u2500\u2500\u2510"
    borde_mid = "\u251c" + "\u2500\u2500\u2500\u2500\u253c" * (cols - 1) + "\u2500\u2500\u2500\u2500\u2524"
    borde_bot = "\u2514" + "\u2500\u2500\u2500\u2500\u2534" * (cols - 1) + "\u2500\u2500\u2500\u2500\u2518"

    if mostrar_coords:
        header = "     " + "".join(f"{c:^5}" for c in range(cols))
        print(header)

    print(borde_top)
    for r, fila in enumerate(tablero_vis):
        contenido = "\u2502".join(f" {SIMBOLOS[c]} " for c in fila)
        prefijo   = f"{r:2} " if mostrar_coords else ""
        print(f"{prefijo}\u2502{contenido}\u2502")
        if r < len(tablero_vis) - 1:
            print(("   " if mostrar_coords else "") + borde_mid)
    print(("   " if mostrar_coords else "") + borde_bot)


def imprimir_estadisticas(ruta: list[Celda]) -> None:
    """Imprime estadísticas básicas del camino encontrado.

    Args:
        ruta: Lista de celdas del camino.
    """
    pasos = len(ruta) - 1
    # Calcular costo real (diagonales valen √2)
    costo = 0.0
    for i in range(1, len(ruta)):
        df = abs(ruta[i][0] - ruta[i-1][0])
        dc = abs(ruta[i][1] - ruta[i-1][1])
        costo += COSTO_DIAGONAL if (df == 1 and dc == 1) else 1.0

    print(f"  Longitud del camino : {pasos} pasos")
    print(f"  Costo real          : {costo:.3f}")
    print(f"  Celdas recorridas   : {len(ruta)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  Punto de entrada
# ═══════════════════════════════════════════════════════════════════════════════

def main(archivo: str = "grid.yaml", diagonal: bool = False) -> None:
    """Función principal del programa.

    Args:
        archivo  : Ruta al archivo YAML con la cuadrícula.
        diagonal : Permite movimientos en diagonal si es True.
    """
    # ── Cargar tablero ────────────────────────────────────────────────────────
    try:
        tablero = cargar_tablero(archivo)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"[ERROR] Archivo mal formado — {e}")
        sys.exit(1)

    # ── Mapa original ─────────────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("  Estado Base")
    print("=" * 50)
    dibujar_tablero(tablero, mostrar_coords=True)
    print("\nLeyenda: 🤖=Inicio (Boome)  🚩=Destino  🟥=Obstáculo  🟡=Camino    =Libre")

    # ── Localizar inicio y fin ────────────────────────────────────────────────
    inicio  = localizar_celda(tablero, 2)
    destino = localizar_celda(tablero, 3)

    if inicio is None:
        print("\n[ERROR] No se encontró el punto de inicio (valor 2) en el tablero.")
        sys.exit(1)
    if destino is None:
        print("\n[ERROR] No se encontró el punto de destino (valor 3) en el tablero.")
        sys.exit(1)

    print(f"\n  Inicio  : fila {inicio[0]}, col {inicio[1]}")
    print(f"  Destino : fila {destino[0]}, col {destino[1]}")
    print(f"  Modo    : {'8 direcciones (diagonal)' if diagonal else '4 direcciones'}")

    # ── Seleccionar heurística según el modo ──────────────────────────────────
    h_func = heuristica_chebyshev if diagonal else heuristica_manhattan

    # ── Ejecutar A* ───────────────────────────────────────────────────────────
    ruta = buscar_ruta(tablero, inicio, destino, diagonal=diagonal, heuristica=h_func)

    # ── Mostrar resultado ─────────────────────────────────────────────────────
    if ruta:
        print("\n" + "=" * 50)
        print("  ¡¡¡Tierra a la vista!!! RUTA ENCONTRADA")
        print("=" * 50)
        dibujar_tablero(tablero, ruta, mostrar_coords=True)

        print("\nLeyenda: 🤖=Inicio  🚩=Destino  🟥=Obstáculo  🟡=Camino")

        print("\n── Estadísticas ─────────────────────────────────")
        imprimir_estadisticas(ruta)

        print("\n── Coordenadas del camino ───────────────────────")
        for i, coord in enumerate(ruta):
            etiqueta = " ← INICIO" if i == 0 else (" ← FIN" if i == len(ruta) - 1 else "")
            print(f"  [{i:2}]  ({coord[0]:2}, {coord[1]:2}){etiqueta}")
    else:
        print("\n[INFO] Ni modo boome se rindio. No existe camino válido entre los puntos.")


# ═══════════════════════════════════════════════════════════════════════════════
#  Ejecución directa
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Puedes cambiar diagonal=True para permitir movimientos en diagonal
    main(archivo="grid.yaml", diagonal=False)