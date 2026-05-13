# ============================================
# BUSQUEDA LOCAL - IMPLEMENTACIONES
# ============================================

"""
DESCRIPCIÓN GENERAL:
Este programa implementa tres algoritmos de búsqueda utilizados en Inteligencia Artificial:
1. Búsqueda en profundidad (DFS)
2. Búsqueda en anchura (BFS)
3. Subir la colina (Hill Climbing)

Se trabaja sobre un grafo, el cual representa un espacio de estados.
Cada nodo es un estado y cada conexión representa un posible movimiento.
"""

from collections import deque

# ============================================
# REPRESENTACIÓN DEL GRAFO
# ============================================

"""
El grafo está representado como un diccionario:
- La clave es un nodo (estado)
- El valor es una lista de nodos vecinos (posibles transiciones)

Ejemplo:
'A': ['B', 'C'] significa que desde A se puede ir a B o C
"""

grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# ============================================
# R001 - PRIMERO EN PROFUNDIDAD (DFS)
# ============================================

"""
DFS (Depth-First Search):
Explora el grafo yéndose lo más profundo posible antes de retroceder.

CARACTERÍSTICAS:
- Usa recursividad
- Puede no encontrar el camino más corto
- Utiliza un conjunto de visitados para evitar ciclos
"""

def dfs(grafo, inicio, objetivo, visitados=None):

    # Inicializa el conjunto de visitados si es la primera llamada
    if visitados is None:
        visitados = set()

    print(f"Visitando: {inicio}")

    # Caso base: si se encuentra el objetivo
    if inicio == objetivo:
        return True

    # Marca el nodo como visitado
    visitados.add(inicio)

    # Explora los vecinos
    for vecino in grafo[inicio]:
        if vecino not in visitados:
            # Llamada recursiva
            if dfs(grafo, vecino, objetivo, visitados):
                return True

    return False


# ============================================
# R002 - PRIMERO EN ANCHURA (BFS)
# ============================================

"""
BFS (Breadth-First Search):
Explora el grafo nivel por nivel.

CARACTERÍSTICAS:
- Usa una cola (FIFO)
- Garantiza el camino más corto en grafos no ponderados
- Evita ciclos con un conjunto de visitados
"""

def bfs(grafo, inicio, objetivo):

    visitados = set()

    # Cola para explorar nodos
    cola = deque([inicio])

    while cola:

        # Extrae el primer elemento (FIFO)
        nodo = cola.popleft()

        print(f"Visitando: {nodo}")

        # Si encuentra el objetivo
        if nodo == objetivo:
            return True

        # Si no ha sido visitado
        if nodo not in visitados:
            visitados.add(nodo)

            # Agrega los vecinos a la cola
            cola.extend(grafo[nodo])

    return False


# ============================================
# R003 - SUBIR LA COLINA (HILL CLIMBING)
# ============================================

"""
Hill Climbing:
Algoritmo de búsqueda local que selecciona siempre el mejor vecino
según una función heurística.

CARACTERÍSTICAS:
- No explora todos los caminos
- No garantiza encontrar la mejor solución global
- Puede quedarse en máximos locales
"""

# Función heurística (menor valor = mejor estado)
heuristica = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 6,
    'E': 2,
    'F': 0  # objetivo
}

def hill_climbing(grafo, inicio, objetivo):

    actual = inicio

    while True:

        print(f"Actual: {actual}")

        # Si llega al objetivo
        if actual == objetivo:
            print("Objetivo alcanzado")
            return True

        vecinos = grafo[actual]

        # Si no hay vecinos, se detiene
        if not vecinos:
            print("Sin vecinos, máximo local")
            return False

        # Selecciona el mejor vecino según heurística
        mejor = min(vecinos, key=lambda x: heuristica[x])

        """
        lambda x: heuristica[x]
        Es una función anónima que devuelve el valor heurístico de cada nodo.
        Se usa para comparar cuál vecino es mejor.
        """

        # Si no mejora, se queda en un máximo local
        if heuristica[mejor] >= heuristica[actual]:
            print("No hay mejora, máximo local")
            return False

        # Avanza al mejor vecino
        actual = mejor


# ============================================
# PRUEBAS
# ============================================

"""
Se ejecutan los tres algoritmos desde el nodo A hasta el nodo F
"""

print("\n--- DFS ---")
dfs(grafo, 'A', 'F')

print("\n--- BFS ---")
bfs(grafo, 'A', 'F')

print("\n--- HILL CLIMBING ---")
hill_climbing(grafo, 'A', 'F')