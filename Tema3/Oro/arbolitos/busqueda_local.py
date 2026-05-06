import json
from collections import deque

def cargar_json(nombre):
    try:
        with open(nombre, 'r') as f:
            return json.load(f) 
    except FileNotFoundError:
        print("Error, archivo no encontrado")
        return {} 

arbol = cargar_json('arbolito.json')



def trepador_profundo(data, objetivo, nodo_actual=None, visitados=None, ruta=None):
    if visitados is None:
        visitados = set()
    if ruta is None:
        ruta = []
    if nodo_actual is None:
        nodo_actual = next(iter(data))

    visitados.add(nodo_actual)
    ruta.append(nodo_actual)

    print(f"Visitando: {nodo_actual}")

    if nodo_actual == objetivo:
        print(f"¡Objetivo '{objetivo}' encontrado!")
        return True

    for vecino in data.get(nodo_actual, []):
        if vecino not in visitados:
            encontrado = trepador_profundo(data, objetivo, vecino, visitados, list(ruta))
            if encontrado:
                return True
    return False



def trepador_ancho(data, objetivo, inicio=None):
    if inicio is None:
        inicio = next(iter(data))

    cola = deque([(inicio, [inicio])])
    visitados = set([inicio])

    while cola:
        nodo_actual, ruta = cola.popleft()
        print(f"Visitando: {nodo_actual}")

        if nodo_actual == objetivo:
            print(f"¡Objetivo '{objetivo}' encontrado!")
            return

        for vecino in data.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, ruta + [vecino]))




colina = cargar_json('colina.json')

def subir_colina(inicio, fin):
    caminos = []
    
    def explorar(nodo, camino_actual, costo_actual, visitados):
        if nodo == fin:
            caminos.append((camino_actual, costo_actual))
            return
            
        visitados.add(nodo)
        
        # ordena los nodos por peso
        vecinos = sorted(colina.get(nodo, {}).items(), key=lambda x: x[1])
        
        for vecino, peso in vecinos:
            if vecino not in visitados:
                explorar(vecino, camino_actual + [vecino], costo_actual + peso, set(visitados))
                
    explorar(inicio, [inicio], 0, set())
    
    if not caminos:
        print("No se encontraron caminos posibles.")
        return []
        
    # Ordenamos todos los caminos encontrados por su costo total para sacar los dos mejores
    caminos.sort(key=lambda x: x[1])
    
    mejor_camino = caminos[0]
    print(f"Camino más corto: \n{' -> '.join(mejor_camino[0])} | Peso total: {mejor_camino[1]} \n")
    
    if len(caminos) > 1:
        segundo_camino = caminos[1]
        print(f"Segundo camino más corto: \n{' -> '.join(segundo_camino[0])} | Peso total: {segundo_camino[1]} \n")
    else:
        print("No hay un segundo camino para comparar.")
        
    return caminos[:2]




G = None

def profundo(objetivo):
    global G
    G = trepador_profundo(arbol, objetivo)

def ancho(objetivo):
    global G
    G = trepador_ancho(arbol, objetivo)


if __name__ == "__main__":
    print("REPL de Búsqueda Iniciado.")
    print("Comandos útiles:")
    print("- profundo('AC')  # Ejecuta busqueda en profundidad hacia 'AC'")
    print("- ancho('AC')     # Ejecuta busqueda en anchura hacia 'AC'")
    print("- subir_colina('A', 'J') # Encuentra el camino más corto en el grafo de colina")

    while True:
        try:
            print()
            R = input(">")
            
            if R == 'salir':
                break
            
            T = eval(R)
            
            if T is not None:
                print(T)

        except Exception as e:
            print("Error!!! ", e)

