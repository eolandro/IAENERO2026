import json, os, sys

# Carga de archivo
ruta_json = os.path.join(os.path.dirname(__file__), "grafo.json")
try:
    with open(ruta_json, encoding="utf-8") as f: g = json.load(f)
except Exception:
    sys.exit("Error: no se encontró el archivo 'grafo.json'.")

# Impresión del Banner y Grafo
print("\n=== R003 - Búsqueda: Subir la Colina (Hill Climbing) ===\nGrafo cargado:\n" + "-"*45)
for n, d in sorted(g.items()): 
    print(f"  {n} (h={d['heuristica']:02d}) --> {', '.join(d['vecinos']) if d['vecinos'] else '(sin conexiones)'}")

ini = sorted(g)[0]
print(f"{'-'*45}\n Nodos disponibles: {', '.join(g)}\n Nodo de inicio: {ini}")

# Función Hill Climbing estricta leyendo el JSON
def hill_climbing(inicio, meta):
    cam = [inicio]
    nodo = inicio
    
    while nodo != meta:
        vecinos = g.get(nodo, {}).get("vecinos", [])
        if not vecinos: 
            print("  [!] Callejón sin salida.")
            break
        
        # Encontramos al vecino con el valor heurístico MÁS BAJO (más cerca a 0)
        mejor_v = min(vecinos, key=lambda x: g.get(x, {}).get("heuristica", float('inf')))
        
        h_actual = g[nodo]["heuristica"]
        h_mejor = g[mejor_v]["heuristica"]
        
        # Si el mejor vecino tiene una heurística mayor o igual, es un máximo local (atasco)
        if h_mejor >= h_actual:
            print(f"  [!] Atascado (Nodo: {nodo}, h={h_actual}). Ningún vecino es mejor.")
            break
            
        nodo = mejor_v
        cam.append(nodo)
        
    return cam

# Bucle principal
while True:
    dst = input(f"\n{'-'*45}\n  ¿A qué nodo quieres llegar? (S para salir)\n  R = ").strip().upper()
    
    if dst == "S": 
        print("\nSaliendo... ¡hasta luego!\n")
        break
    if dst not in g:
        if dst: print("  Escribe un nodo válido o 'S' para salir.")
        continue
    
    print(f"\nEjecutando Hill Climbing desde '{ini}' --> '{dst}'...")
    
    c = hill_climbing(ini, dst)
    
    if c[-1] == dst:
        print(f"\n¡Meta alcanzada!\n  {' -> '.join(c)}\n  Pasos: {len(c)-1}")
    else:
        print(f"\nBúsqueda detenida antes de la meta.\n  Camino recorrido: {' -> '.join(c)}")