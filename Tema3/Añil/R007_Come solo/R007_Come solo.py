tablero = [
    [1],
    [1, 1],
    [1, 0, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1, 1]
]

estados = []  

def mostrar(tab):
    for i in range(len(tab)):
        print(" " * (5 - i), end="")
        for j in range(len(tab[i])):
            if tab[i][j] == 1:
                print("●", end=" ")
            else:
                print("○", end=" ")
        print()
    print("-------------------")

def copiar(tab):
    nuevo = []
    for fila in tab:
        nueva_fila = []
        for celda in fila:
            nueva_fila.append(celda)
        nuevo.append(nueva_fila)
    return nuevo

def contar():
    total = 0
    for fila in tablero:
        for celda in fila:
            if celda == 1:
                total += 1
    return total

def resolver():
    if contar() == 1:
        estados.append(copiar(tablero))
        return True

    for i in range(len(tablero)):
        for j in range(len(tablero[i])):

            if tablero[i][j] == 1:

                movimientos = [
                    (-2, 0), (-2, -2),
                    (2, 0), (2, 2),
                    (0, -2), (0, 2)
                ]

                for mov in movimientos:
                    ni = i + mov[0]
                    nj = j + mov[1]
                    mi = i + mov[0] // 2
                    mj = j + mov[1] // 2

                    if ni >= 0 and ni < len(tablero):
                        if nj >= 0 and nj < len(tablero[ni]):

                            if tablero[ni][nj] == 0 and tablero[mi][mj] == 1:

                                tablero[i][j] = 0
                                tablero[mi][mj] = 0
                                tablero[ni][nj] = 1

                                estados.append(copiar(tablero))

                                if resolver():
                                    return True

                                tablero[i][j] = 1
                                tablero[mi][mj] = 1
                                tablero[ni][nj] = 0
                                estados.pop()

    return False

print("ESTADO INICIAL: ")
mostrar(tablero)

estados.append(copiar(tablero))

if resolver():
    print("EJECUCION EXITOSA \n")

    for i, estado in enumerate(estados):
        print(f"PASO # {i}:")
        mostrar(estado)
else:
    print("SIN SOLUCION")