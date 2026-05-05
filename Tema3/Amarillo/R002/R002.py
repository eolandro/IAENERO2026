import json, os, sys
from collections import deque

# Carga de archivo
ruta_json = os.path.join(os.path.dirname(__file__), "grafo.json")
try:
    with open(ruta_json, encoding="utf-8") as f: g = json.load(f)
except Exception:
    sys.exit("Error: no se encontró el archivo 'grafo.json'.")

# Impresión del Banner y Grafo
print("\n=== R002 - Búsqueda Primero en Anchura ===\nGrafo cargado:\n" + "-"*36)
for n, v in sorted(g.items()): print(f"  {n}  -->  {', '.join(v) if v else '(sin conexiones)'}")

ini = sorted(g)[0]
print(f"{'-'*36}\n Nodos disponibles: {', '.join(g)}\n Nodo de inicio: {ini}")

# Función BFS compacta (almacena la ruta en la cola)
def bfs(inicio, meta):
    cola = deque([[inicio]]) # La cola guarda listas de caminos, no solo nodos
    vis = {inicio}
    
    while cola:
        cam = cola.popleft() # Sacamos el primer camino de la cola
        nodo = cam[-1]       # El nodo actual es el último elemento del camino
        
        if nodo == meta: 
            return cam
            
        for vec in g.get(nodo, []):
            if vec not in vis:
                vis.add(vec)
                cola.append(cam + [vec]) # Agregamos el nuevo camino a la cola
                
    return None

# Bucle principal
while True:
    dst = input(f"\n{'-'*44}\n  ¿A qué nodo quieres llegar? (S para salir)\n  R = ").strip().upper()
    
    if dst == "S": 
        print("\nSaliendo... ¡hasta luego!\n")
        break
    if dst not in g:
        if dst: print("  Escribe un nodo válido o 'S' para salir.")
        continue
    
    print(f"\nEjecutando BFS desde '{ini}' --> '{dst}'...")
    
    c = bfs(ini, dst)
    if c:
        print(f"\nCamino encontrado (más corto):\n  {' -> '.join(c)}\n  Pasos: {len(c)-1}  |  Nodos: {len(c)}\n")
    else:
        print(f"\nNo se encontró camino hasta '{dst}'.\n")