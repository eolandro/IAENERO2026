tablero = []
for i in range(8):
    fila_nueva = [".", ".", ".", ".", ".", ".", ".", "."]
    tablero.append(fila_nueva)

mov_f = [2, 1, -1, -2, -2, -1, 1, 2]
mov_c = [1, 2, 2, 1, -1, -2, -2, -1]

def dibujar_tablero(paso_actual):
    print("\n      RECORRIDO: PASO #", paso_actual)
    print("    A   B   C   D   E   F   G   H")
    print("  +---+---+---+---+---+---+---+---+")
    
    for i in range(8):
        linea = str(i + 1) + " |"
        for j in range(8):
            valor = tablero[i][j]
            if valor == ".":
                linea = linea + " . |"
            else:
                if valor < 10:
                    linea = linea + " " + str(valor) + " |"
                else:
                    linea = linea + str(valor) + " |"
        
        print(linea)
        print("  +---+---+---+---+---+---+---+---+")
        
def contar_movimientos(f, c):
    contador = 0
    for i in range(8):
        nf = f + mov_f[i]
        nc = c + mov_c[i]
        if nf >= 0 and nf < 8 and nc >= 0 and nc < 8:
            if tablero[nf][nc] == ".":
                contador = contador + 1
    return contador

#BACKTRACKING
def recorrer(f_actual, c_actual, pasos_dados):
    tablero[f_actual][c_actual] = pasos_dados
    dibujar_tablero(pasos_dados)
    if pasos_dados == 64:
        return True
    
    mejor_f = -1
    mejor_c = -1
    min_opciones = 9

    for i in range(8):
        nf = f_actual + mov_f[i]
        nc = c_actual + mov_c[i]

        if nf >= 0 and nf < 8 and nc >= 0 and nc < 8:
            if tablero[nf][nc] == ".":
                opciones = contar_movimientos(nf, nc)
                if opciones < min_opciones:
                    min_opciones = opciones
                    mejor_f = nf
                    mejor_c = nc

    if mejor_f != -1:
        if recorrer(mejor_f, mejor_c, pasos_dados + 1):
            return True
    tablero[f_actual][c_actual] = "."
    return False
dibujar_tablero(0)
columna_input = input("Ingresa columna (A-H): ")
fila_input = input("Ingresa fila (1-8): ")
letras = "ABCDEFGH"
c_inicial = -1
for i in range(8):
    if letras[i] == columna_input.upper():
        c_inicial = i

f_inicial = int(fila_input) - 1

if c_inicial != -1 and f_inicial >= 0 and f_inicial < 8:

    if recorrer(f_inicial, c_inicial, 1):
        print("Recorrido completo, 64 casillas.")
    else:
        print("\nNo hay solucion.")
else:
    print("fuera de posicion.")