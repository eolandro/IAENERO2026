"""
El problema del caballo (recorrido del caballo) se resuelve utilizando el índice 
de accesibilidad a través de la regla o algoritmo de Warnsdorff. Este método heurístico 
busca, en cada movimiento, elegir la casilla que tenga el menor número de movimientos de 
seguimiento posibles (menor accesibilidad) hacia casillas aún no visitadas. 
"""

tablero = [[0]*8 for _ in range(8)]

def imprimir_tablero(tablero):
    print("\n  +" + "----+"*8)
    for fila in tablero:
        fila_str = "  |"
        for celda in fila:
            if celda == 0:
                fila_str += "    |"
            else:
                fila_str += f" {celda:2} |"
        print(fila_str)
        print("  +" + "----+"*8)
    print()

def siguiente_casilla(f,c,tablero):
    movimientos = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    destinos = []
    lista_a = []

    # Calcular destinos posibles a partir de la casilla
    for i in range(len(movimientos)):
        f_nueva = f + movimientos[i][0]
        c_nueva = c  + movimientos[i][1]
        
        if (f_nueva<= 7 and f_nueva>=0) and (c_nueva<= 7 and c_nueva>=0) and (tablero[f_nueva][c_nueva]==0):
            destinos.append((f_nueva,c_nueva))

    print(f"Destinos disponibles a partir de {f},{c}: {destinos}")
    
    if not destinos:
        return None

    else:
        # Calcular la accesibilidad dinamica a partir de los destinos posibles
        for candidato in range((len(destinos))):
            contador_ceros = 0
            for m in range(len(movimientos)):

                f_nueva = destinos[candidato][0]  + movimientos[m][0]
                c_nueva = destinos[candidato][1]  + movimientos[m][1]
            
                if (f_nueva<= 7 and f_nueva>=0) and (c_nueva<= 7 and c_nueva>=0) and (tablero[f_nueva][c_nueva]==0):
                    contador_ceros += 1
            lista_a.append(contador_ceros)

        menor = min(lista_a)
        posicion = lista_a.index(menor)
            
        return destinos[posicion][0],destinos[posicion][1]

print("\n * * * PROBLEMA DEL RECORRIDO DEL CABALLO * * * \n")

c = input("¿Cual sera la casilla inicial del caballo (por ejemplo 0,0) ? ")
c = c.replace(" ", "").split(",")
tablero[int(c[0])][int(c[1])] = 1
contador = 1
f_actual = int(c[0])
c_actual = int(c[1])

while contador < 64:

    resultado = siguiente_casilla(f_actual, c_actual, tablero)

    if resultado is None:
        print("No se puede completar el recorrido")
        break
    else:
        f_sig, c_sig = resultado
        contador += 1
        tablero[f_sig][c_sig] = contador
        f_actual, c_actual = f_sig, c_sig


imprimir_tablero(tablero)