tablero = [
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."]
]

def dibujar_tablero(matriz):
    print("TABLERO (4 REINAS)")
    print("    A   B   C   D")
    print("  +---+---+---+---+")
    
    for i in range(4):
        linea = str(i + 1) + " |"
        
        for j in range(4):
            linea = linea + " " + matriz[i][j] + " |"
        
        print(linea)
        print("  +---+---+---+---+")

def es_seguro(tablero, fila, columna):
    i = 0
    while i < fila:
        if tablero[i][columna] == "R":
            return False
        i = i + 1

    i = fila - 1
    j = columna - 1
    while i >= 0 and j >= 0:
        if tablero[i][j] == "R":
            return False
        i = i - 1
        j = j - 1

    i = fila - 1
    j = columna + 1
    while i >= 0 and j < 4:
        if tablero[i][j] == "R":
            return False
        i = i - 1
        j = j + 1

    return True
soluciones = []

def resolver(tablero, fila):
    if fila == 4:
        copia = []
        i = 0
        while i < 4:
            fila_copia = []
            j = 0
            while j < 4:
                fila_copia.append(tablero[i][j])
                j = j + 1
            copia.append(fila_copia)
            i = i + 1
        
        soluciones.append(copia)
        return

    columna = 0
    while columna < 4:
        if es_seguro(tablero, fila, columna):
            tablero[fila][columna] = "R"
            resolver(tablero, fila + 1)
            tablero[fila][columna] = "."
        columna = columna + 1

print("IMPRIMIENDO POSIBLES SOLUCIONES")

resolver(tablero, 0)

print("Total de soluciones:", len(soluciones))

i = 0
while i < len(soluciones):
    print("solucion", i + 1)
    dibujar_tablero(soluciones[i])
    i = i + 1