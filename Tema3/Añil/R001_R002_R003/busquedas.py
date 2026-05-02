#  Actividad 1: Búsqueda Local
#  R001 : Primero en Profundidad  (DFS)
#  R002 : Primero en Anchura      (BFS)
#  R003 : Subir la Colina         (Hill Climbing)

import json
from collections import deque

def cargar_grafo(ruta):
    """
    Carga un grafo desde un archivo JSON.

    El archivo puede contener:
      - Grafo sin pesos : { "A": ["B", "C"], ... }
      - Grafo con pesos : { "A": {"B": 1, "C": 5}, ... }

    Parámetros:
        ruta (str): ruta al archivo .json

    Retorna:
        dict: grafo cargado, o None si hubo error.
    """
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            grafo = json.load(f)
        print(f"Grafo cargado desde '{ruta}' — {len(grafo)} nodos.")
        return grafo
    except FileNotFoundError:
        print(f"No se encontró el archivo '{ruta}'.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error de formato JSON en '{ruta}': {e}")
        return None


def mostrar_grafo(grafo):
    """Imprime el grafo de forma legible en consola."""
    print()
    for nodo, vecinos in grafo.items():
        if isinstance(vecinos, dict):
            if vecinos:
                conexiones = ",  ".join(f"{v} (peso {p})" for v, p in vecinos.items())
            else:
                conexiones = "(sin salida — nodo hoja)"
        else:
            conexiones = " → ".join(vecinos) if vecinos else "(nodo hoja)"
        print(f"  {nodo:<12} →  {conexiones}")
    print()


def separador(titulo=""):
    """Imprime una línea separadora con título opcional."""
    linea = "─" * 55
    if titulo:
        print(f"\n┌{linea}┐")
        print(f"│  {titulo:<53}│")
        print(f"└{linea}┘")
    else:
        print(f"  {linea}")


#  R001 — DFS: Búsqueda Primero en Profundidad

def dfs(grafo, objetivo, inicio="A"):
    """
    Búsqueda Primero en Profundidad (Depth-First Search).

    Explora tan profundo como sea posible por cada rama antes
    de retroceder. Usa una pila (LIFO) de forma explícita.

    Parámetros:
        grafo    (dict) : grafo cargado desde JSON (sin pesos).
        objetivo (str)  : nodo que se desea encontrar.
        inicio   (str)  : nodo de partida (default "A").

    Retorna:
        list : camino desde inicio hasta objetivo,
               o None si no existe.
    """
    separador(f"R001 · DFS  |  '{inicio}' ──▶ '{objetivo}'")

    if inicio not in grafo:
        print(f"El nodo de inicio '{inicio}' no existe en el grafo.")
        return None
    if objetivo not in grafo:
        print(f" El nodo objetivo '{objetivo}' no existe en el grafo.")
        return None

    # Pila: cada elemento es (nodo_actual, camino_hasta_aquí)
    pila     = [(inicio, [inicio])]
    visitados = set()
    paso     = 1

    print(f"  {'Paso':<6} {'Nodo actual':<14} {'Camino recorrido'}")
    print(f"  {'─'*6} {'─'*14} {'─'*30}")

    while pila:
        nodo, camino = pila.pop()          # LIFO — último en entrar, primero en salir

        if nodo in visitados:
            continue

        visitados.add(nodo)
        print(f"  {paso:<6} {nodo:<14} {' → '.join(camino)}")
        paso += 1

        if nodo == objetivo:
            print(f"\n ¡Objetivo '{objetivo}' encontrado!")
            print(f"     Camino : {' → '.join(camino)}")
            print(f"     Pasos  : {len(camino) - 1}")
            return camino

        # Obtener vecinos (lista o claves de dict con pesos)
        vecinos = grafo.get(nodo, [])
        if isinstance(vecinos, dict):
            vecinos = list(vecinos.keys())

        # Invertimos para mantener orden izquierda→derecha en la pila
        for vecino in reversed(vecinos):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))

    print(f"\n  El objetivo '{objetivo}' no fue encontrado.")
    return None


#  R002 — BFS: Búsqueda Primero en Anchura

def bfs(grafo, objetivo, inicio="A"):
    """
    Búsqueda Primero en Anchura (Breadth-First Search).

    Explora todos los nodos del nivel actual antes de pasar
    al siguiente. Usa una cola (FIFO). Garantiza el camino
    más corto en número de saltos.

    Parámetros:
        grafo    (dict) : grafo cargado desde JSON (sin pesos).
        objetivo (str)  : nodo que se desea encontrar.
        inicio   (str)  : nodo de partida (default "A").

    Retorna:
        list : camino desde inicio hasta objetivo,
               o None si no existe.
    """
    separador(f"R002 · BFS  |  '{inicio}' ──▶ '{objetivo}'")

    if inicio not in grafo:
        print(f"  El nodo de inicio '{inicio}' no existe en el grafo.")
        return None
    if objetivo not in grafo:
        print(f"  El nodo objetivo '{objetivo}' no existe en el grafo.")
        return None

    # Cola: cada elemento es (nodo_actual, camino_hasta_aquí)
    cola      = deque([(inicio, [inicio])])
    visitados = set([inicio])
    paso      = 1

    print(f"  {'Paso':<6} {'Nodo actual':<14} {'Camino recorrido'}")
    print(f"  {'─'*6} {'─'*14} {'─'*30}")

    while cola:
        nodo, camino = cola.popleft()      # FIFO — primero en entrar, primero en salir

        print(f"  {paso:<6} {nodo:<14} {' → '.join(camino)}")
        paso += 1

        if nodo == objetivo:
            print(f"\n  ¡Objetivo '{objetivo}' encontrado!")
            print(f"     Camino : {' → '.join(camino)}")
            print(f"     Pasos  : {len(camino) - 1}")
            return camino

        vecinos = grafo.get(nodo, [])
        if isinstance(vecinos, dict):
            vecinos = list(vecinos.keys())

        for vecino in vecinos:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))

    print(f"\n El objetivo '{objetivo}' no fue encontrado.")
    return None


#  R003 — Hill Climbing: Subir la Colina

def hill_climbing(grafo, inicio, fin):
    """
    Búsqueda Subir la Colina (Hill Climbing).

    En cada paso elige el vecino con MENOR peso (costo),
    avanzando siempre hacia la opción localmente más prometedora.

    Limitación: puede quedar atascado en mínimos locales
        (nodos sin salida o sin vecinos no visitados).

    Parámetros:
        grafo  (dict) : grafo con pesos cargado desde JSON.
        inicio (str)  : nodo de partida.
        fin    (str)  : nodo destino.

    Retorna:
        (list, int) : camino encontrado y peso total acumulado,
                      o (None, None) si no llegó al destino.
    """
    separador(f"R003 · Hill Climbing  |  '{inicio}' ──▶ '{fin}'")

    if inicio not in grafo:
        print(f"  El nodo de inicio '{inicio}' no existe en el grafo.")
        return None, None
    if fin not in grafo:
        print(f"  El nodo destino '{fin}' no existe en el grafo.")
        return None, None

    nodo_actual  = inicio
    camino       = [inicio]
    peso_total   = 0
    visitados    = set([inicio])
    paso         = 1

    print(f"  {'Paso':<6} {'Nodo actual':<14} {'Mejor vecino':<14} {'Peso paso':<12} {'Acumulado'}")
    print(f"  {'─'*6} {'─'*14} {'─'*14} {'─'*12} {'─'*10}")

    while nodo_actual != fin:
        vecinos = grafo.get(nodo_actual, {})

        # Filtramos vecinos ya visitados
        opciones = {v: p for v, p in vecinos.items() if v not in visitados}

        if not opciones:
            print(f"\n  Atascado en '{nodo_actual}' — sin vecinos disponibles.")
            print("     Hill Climbing terminó en un MÍNIMO LOCAL.")
            print(f"     Camino hasta aquí : {' → '.join(camino)}")
            print(f"     Peso acumulado    : {peso_total}")
            return None, None

        # Elegimos el vecino de menor peso (decisión greedy local)
        mejor   = min(opciones, key=lambda v: opciones[v])
        peso_mv = opciones[mejor]

        print(f"  {paso:<6} {nodo_actual:<14} {mejor:<14} {peso_mv:<12} {peso_total + peso_mv}")
        paso += 1

        peso_total   += peso_mv
        nodo_actual   = mejor
        camino.append(nodo_actual)
        visitados.add(nodo_actual)

    print(f"\n  ¡Destino '{fin}' alcanzado!")
    print(f"     Camino      : {' → '.join(camino)}")
    print(f"     Peso total  : {peso_total}")
    return camino, peso_total


#  MENÚ PRINCIPAL

def menu():
    grafo_simple = None    # Para DFS y BFS (grafo.json)
    grafo_pesos  = None    # Para Hill Climbing (grafo_pesos.json)

    print("\n╔══════════════════════════════════════════════╗")
    print("║       Actividad 1 — Búsqueda Local           ║")
    print("║  R001: DFS  |  R002: BFS  |  R003: HillClimb ║")
    print("╚══════════════════════════════════════════════╝")

    while True:
        print("\n  ┌─────────────────────────────────────────┐")
        print("  │               MENÚ PRINCIPAL            │")
        print("  ├─────────────────────────────────────────┤")
        print("  │  1. Cargar grafo simple  (DFS / BFS)    │")
        print("  │  2. Cargar grafo pesos   (Hill Climbing)│")
        print("  │  3. Ver grafo cargado                   │")
        print("  ├─────────────────────────────────────────┤")
        print("  │  4. R001 — DFS   (Primero Profundidad)  │")
        print("  │  5. R002 — BFS   (Primero Anchura)      │")
        print("  │  6. R003 — Hill Climbing                │")
        print("  ├─────────────────────────────────────────┤")
        print("  │  7. Salir                               │")
        print("  └─────────────────────────────────────────┘")

        opcion = input("\n  > ").strip()

        # ── Cargar grafos ──────────────────────────────────────
        if opcion == "1":
            ruta = input("  Ruta del archivo (Enter = grafo.json): ").strip()
            if not ruta:
                ruta = "grafo.json"
            grafo_simple = cargar_grafo(ruta)

        elif opcion == "2":
            ruta = input("  Ruta del archivo (Enter = grafo_pesos.json): ").strip()
            if not ruta:
                ruta = "grafo_pesos.json"
            grafo_pesos = cargar_grafo(ruta)

        # ── Ver grafo ──────────────────────────────────────────
        elif opcion == "3":
            if grafo_simple:
                separador("Grafo simple — DFS / BFS")
                mostrar_grafo(grafo_simple)
            if grafo_pesos:
                separador("Grafo con pesos — Hill Climbing")
                mostrar_grafo(grafo_pesos)
            if not grafo_simple and not grafo_pesos:
                print(" No hay grafos cargados. Usa las opciones 1 y 2.")

        # ── R001 DFS ───────────────────────────────────────────
        elif opcion == "4":
            if not grafo_simple:
                print("  Primero carga el grafo simple (opción 1).")
                continue
            inicio   = input("  Nodo inicio   (Enter = A): ").strip().upper() or "A"
            objetivo = input("  Nodo objetivo : ").strip().upper()
            dfs(grafo_simple, objetivo, inicio)

        # ── R002 BFS ───────────────────────────────────────────
        elif opcion == "5":
            if not grafo_simple:
                print("  Primero carga el grafo simple (opción 1).")
                continue
            inicio   = input("  Nodo inicio   (Enter = A): ").strip().upper() or "A"
            objetivo = input("  Nodo objetivo : ").strip().upper()
            bfs(grafo_simple, objetivo, inicio)

        # ── R003 Hill Climbing ─────────────────────────────────
        elif opcion == "6":
            if not grafo_pesos:
                print("  Primero carga el grafo con pesos (opción 2).")
                continue
            inicio = input("  Nodo inicio   : ").strip().upper()
            fin    = input("  Nodo destino  : ").strip().upper()
            hill_climbing(grafo_pesos, inicio, fin)

        # ── Salir ──────────────────────────────────────────────
        elif opcion == "7":
            print("\n  ¡Hasta luego!\n")
            break

        else:
            print(" Opción no válida, intenta de nuevo.")


#  PUNTO DE ENTRADA

if __name__ == "__main__":
    menu()
