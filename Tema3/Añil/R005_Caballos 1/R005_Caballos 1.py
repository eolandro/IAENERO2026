estado_inicial = ((0, 0), (0, 5), (5, 0), (5, 5))
estado_meta = ((5, 0), (5, 5), (0, 0), (0, 5))

def dibujar_tablero(estado):
    matriz = []
    i = 0
    while i < 6:
        fila = []
        
        j = 0
        while j < 6:
            fila.append(".")
            j = j + 1
        
        matriz.append(fila)
        i = i + 1
    matriz[estado[0][0]][estado[0][1]] = "1"
    matriz[estado[1][0]][estado[1][1]] = "2"
    matriz[estado[2][0]][estado[2][1]] = "3"
    matriz[estado[3][0]][estado[3][1]] = "4"

    print("\n      TABLERO (6x6)")
    print("    A   B   C   D   E   F")
    print("  +---+---+---+---+---+---+")
    for i in range(6):
        linea = str(i + 1) + " |"
        for j in range(6):
            linea += " " + matriz[i][j] + " |"
        print(linea)
        print("  +---+---+---+---+---+---+")

def obtener_movimientos(posicion):
    f, c = posicion
    posibles = [
        (f+2, c+1), (f+2, c-1), (f-2, c+1), (f-2, c-1),
        (f+1, c+2), (f+1, c-2), (f-1, c+2), (f-1, c-2)
    ]
    validos = []
    for nf, nc in posibles:
        if 0 <= nf < 6 and 0 <= nc < 6:
            validos.append((nf, nc))
    return validos

def resolver():
    cola = [[estado_inicial, []]]
    visitados = {estado_inicial}

    print("esperando solucion")

    while cola:
        actual, camino = cola.pop(0)
        if actual == estado_meta:
            return camino + [actual]
        for i in range(4):
            pos_caballo = actual[i]
            for nueva_pos in obtener_movimientos(pos_caballo):
                if nueva_pos not in actual:
                    nuevo_estado = list(actual)
                    nuevo_estado[i] = nueva_pos
                    nuevo_estado = tuple(nuevo_estado)

                    if nuevo_estado not in visitados:
                        visitados.add(nuevo_estado)
                        cola.append([nuevo_estado, camino + [actual]])
    return None

pasos_solucion = resolver()

if pasos_solucion:
    for i, paso in enumerate(pasos_solucion):
        print(f"\nMOVIMIENTO #{i}")
        dibujar_tablero(paso)
    print("nms funciono")
else:
    print("SIN SOLUCION")