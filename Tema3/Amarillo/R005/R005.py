# R005: 4 Caballos (Intercambio 6x6 con Mensajes y Etiquetas)
from collections import deque

def intercambio_caballos():
    print("\n=== R005: Intercambio de 4 Caballos en 6x6 ===")
    movs = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
    
    def bfs_ruta(inicio, meta):
        cola = deque([[inicio]])
        visitados = {inicio}
        while cola:
            camino = cola.popleft()
            x, y = camino[-1]
            if (x, y) == meta:
                return camino
            for dx, dy in movs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 6 and 0 <= ny < 6 and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    cola.append(camino + [(nx, ny)])
        return []

    # Diccionario con un "id" para identificar a cada caballo en el tablero
    piezas = {
        "Blanco 1": {"id": "B1", "ini": (0, 0), "meta": (5, 5)},
        "Blanco 2": {"id": "B2", "ini": (0, 5), "meta": (5, 0)},
        "Negro 1":  {"id": "N1", "ini": (5, 0), "meta": (0, 5)},
        "Negro 2":  {"id": "N2", "ini": (5, 5), "meta": (0, 0)}
    }

    for nombre, datos in piezas.items():
        ruta = bfs_ruta(datos["ini"], datos["meta"])
        
        # Crear matriz vacía
        matriz = [["--" for _ in range(6)] for _ in range(6)]
        
        # Rellenar la matriz con las etiquetas correspondientes
        for paso, (x, y) in enumerate(ruta):
            if paso == 0:
                matriz[x][y] = datos["id"]  # Etiqueta de inicio (ej. N2)
            elif paso == len(ruta) - 1:
                matriz[x][y] = "ME"         # Etiqueta de Meta (Destino final)
            else:
                matriz[x][y] = f"{paso:02d}" # Número de salto
                
        # Imprimir el mensaje descriptivo y la leyenda
        print(f"\n{'-'*35}")
        print(f" Ruta de {nombre}")
        print(f"{'-'*35}")
        print(f" Mensaje: El caballo [{datos['id']}] viaja desde la coordenada {datos['ini']} hasta {datos['meta']}.")
        print(f" Leyenda: '{datos['id']}' = Inicio | 'ME' = Meta | Saltos totales: {len(ruta)-1}\n")
        
        # Imprimir la matriz
        for fila in matriz:
            print("    " + "  ".join(fila))

intercambio_caballos()