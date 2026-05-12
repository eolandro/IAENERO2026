import json
import os
import sys


ruta_json = os.path.join(os.path.dirname(__file__), "grafo.json") 

try:
    # Abrimos y leemos el archivo JSON usando codificación UTF-8
    with open(ruta_json, encoding="utf-8") as f: 
        g = json.load(f)  # 'g' es el diccionario que representa el grafo
except Exception:
    # Si ocurre cualquier error, salimos del programa
    sys.exit("Error: no se encontró o no se pudo leer el archivo 'grafo.json'.")



print("\n=== R001 - Búsqueda Primero en Profundidad ===")
print("Grafo cargado:\n" + "-" * 36)

# Iteramos sobre el grafo ordenado alfabéticamente para imprimir sus conexiones
for nodo, vecinos in sorted(g.items()): 
    conexiones = ", ".join(vecinos) if vecinos else "(sin conexiones)"
    print(f"  {nodo}  -->  {conexiones}")

# Definimos el nodo de inicio, que será el primero del grafo ordenado
ini = sorted(g)[0]
print(f"{'-' * 36}")
print(f" Nodos disponibles: {', '.join(g)}")
print(f" Nodo de inicio: {ini}")



def dfs(nodo_actual, destino, visitados, camino):
    # Marcamos el nodo actual como visitado y lo agregamos al camino
    visitados.add(nodo_actual)
    camino.append(nodo_actual)
    print(f"  Visitando: {nodo_actual}")
    
    # Condición base: Si hemos llegado al destino, retornamos el camino
    if nodo_actual == destino: 
        return camino
        
    # Exploramos cada uno de los vecinos del nodo actual
    # g.get(nodo_actual, []) retorna la lista de vecinos, o [] si no tiene
    for vecino in g.get(nodo_actual, []):
        # Si el vecino no ha sido visitado, hacemos llamada recursiva
        if vecino not in visitados:
            resultado = dfs(vecino, destino, visitados, camino)
            # Si el llamado recursivo retorna un camino válido, lo propagamos
            if resultado: 
                return resultado
                
    # Backtracking: Si ninguno de los vecinos nos llevó al destino,
    # sacamos el nodo actual del camino porque no pertenece a la ruta correcta
    camino.pop() 
    return None



# Este bucle mantiene el programa en ejecución permitiendo múltiples búsquedas
while True:
    print(f"\n{'-' * 44}")
    # Solicitamos al usuario el nodo de destino, limpiando espacios y en mayúsculas
    dst = input("  ¿A qué nodo quieres llegar? (S para salir)\n  R = ").strip().upper()
    
    # Condición de salida del programa
    if dst == "S": 
        print("  ¡Hasta luego!")
        break
        
    # Validación de entrada: verificar que el nodo exista en el grafo
    if dst not in g:
        if dst: # Si el usuario no presionó Enter vacío
            print("  Escribe un nodo válido o 'S' para salir.")
        continue
    
    print(f"\nEjecutando DFS desde '{ini}' --> '{dst}'...")
    
    # Llamamos a la función dfs con un set vacío de visitados y una lista vacía para el camino
    resultado_camino = dfs(ini, dst, set(), [])
    
    # Mostramos los resultados según si se encontró o no un camino
    if resultado_camino:
        ruta_formateada = ' -> '.join(resultado_camino)
        pasos = len(resultado_camino) - 1
        nodos_totales = len(resultado_camino)
        print("\nCamino encontrado:")
        print(f"  {ruta_formateada}")
        print(f"  Pasos: {pasos}  |  Nodos: {nodos_totales}\n")
    else:
        print(f"\nNo se encontró camino hasta '{dst}'.\n")
