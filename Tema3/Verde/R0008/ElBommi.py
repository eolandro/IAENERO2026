from pathlib import Path
import json
import argparse

# ==========================================
# LECTURA DE DATOS
# ==========================================
# Esta función se encarga de recibir el archivo desde la línea de comandos,
# verificar que exista, leer su contenido en formato JSON y extraer
# específicamente la matriz del "mapa" para devolverla.
def mapa():
    parser = argparse.ArgumentParser()
    parser.add_argument("Archivo", help="Archivo: ", type=Path)
    args = parser.parse_args()

    if args.Archivo.exists():
        print("Grafo encontrado")
        with args.Archivo.open('r') as arch_json:
            datos = json.load(arch_json)
            Mapa = datos["mapa"]
            return Mapa
    else:
        print("Archivo no encontrado")

# ==========================================
# ALGORITMOS DE BÚSQUEDA Y LÓGICA ESPACIAL
# ==========================================

# Heurística: Calcula la distancia Manhattan entre dos puntos.
# Sirve para estimar qué tan lejos estamos del objetivo de forma rápida.
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Busca en toda la matriz del mapa dónde está el punto de inicio ("B" - bomie)
# y dónde está el punto final o destino (2 - bomba), retornando ambas coordenadas.
def recorrido(Mapa):
    b_bomie = None
    b_bomba = None
    for fila in range(len(Mapa)):
        for columna in range(len(Mapa[0])):
            if Mapa[fila][columna] == "B":
                b_bomie = (fila, columna)
            elif Mapa[fila][columna] == 2:
                b_bomba = (fila, columna)
    
    return b_bomie, b_bomba

# Obtiene todas las casillas vecinas válidas a las que se puede mover (arriba, abajo, izq, der).
# Filtra los movimientos que se salen de los límites del mapa o que son paredes (1).
def adyacentes(Mapa, casilla):
    filas = len(Mapa)
    columnas = len(Mapa[0])
    encontrados = []

    direcciones = [(0,1), (0,-1), (1,0), (-1,0)]

    for mx, my in direcciones:
        c_filas = casilla[0] + mx
        c_columnas = casilla[1] + my

        # Validaciones de límites de mapa y obstáculos
        if c_filas < 0:
            continue
        if c_filas >= filas:
            continue
        if c_columnas < 0:
            continue
        if c_columnas >= columnas:
            continue
        if Mapa[c_filas][c_columnas] == 1:
            continue

        encontrados.append((c_filas, c_columnas))
    return encontrados

# Función principal de búsqueda (implementa una variación de A*).
# Utiliza una cola priorizada para explorar primero los caminos que 
# la heurística indica que están más cerca del objetivo.
def buscar(Mapa):
    inicio, fin = recorrido(Mapa)
    if not inicio or not fin:
        return False 

    # La cola guarda tuplas con: (posición_actual, camino_recorrido, costo_acumulado)
    cola = [(inicio, [inicio], 0)]
    visitados = []

    while cola:
        # Extraemos el nodo más prometedor (el primero tras ordenar la cola)
        actual, camino, valor = cola[0]
        cola = cola[1:]

        # Condición de éxito: Si llegamos a la bomba, mostramos el camino y terminamos
        if actual == fin:
            mostrar(Mapa, camino)
            return True

        visitados.append(actual)
        
        # Exploración de vecinos: por cada vecino no visitado, calculamos
        # su nuevo costo usando la heurística y lo agregamos a la cola.
        vecinos = adyacentes(Mapa, actual)
        for v in vecinos:
            if v not in visitados:
                h = heuristica(v, fin)
                cola.append((v, camino + [v], valor + 1 + h))
                
                # Ordenamos la cola para que el nodo con menor costo quede al principio
                cola.sort(key=lambda x: x[2])

    print("Sin camino pa")
    return False

# ==========================================
# SALIDA Y REPRESENTACIÓN DE DATOS
# ==========================================
# Toma el camino exitoso, dibuja asteriscos ("*") sobre los espacios libres (0) 
# de una copia del mapa para visualizar la ruta y exporta el resultado a un JSON.
def mostrar(Mapa, camino):
    print("\nCamino encontrado:\n")
    nuevo = [fila[:] for fila in Mapa]
    
    for (x, y) in camino:
        if nuevo[x][y] == 0:
            nuevo[x][y] = "*"
            
    for fila in nuevo:
        print(" ".join(str(x) for x in fila))
    
    #salida = {
    #    "valores": camino,
    #    "mapa": nuevo
    #}

    #3with open("resultado.json", "w") as archivo:
    #   json.dump(salida, archivo, separators=(',', ':'))

# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
# Orquesta el programa: carga el mapa inicial, lo imprime en pantalla 
# tal como entra y luego dispara el algoritmo de búsqueda.
def main():
    Mapa = mapa()
    if not Mapa:
        return
        
    for fila in Mapa:
        print(fila)

    buscar(Mapa)

if __name__ == "__main__":
    main()