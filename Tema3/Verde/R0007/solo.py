movs=[[(2,4),(3,6)],[(4,7),(5,9)],[(5,8),(6,10)],
        [(2,1),(5,6),(7,11),(8,13)],[(8,12),(9,14)],
        [(3,1),(5,4),(9,13),(10,15)],[(4,2),(8,9)],
        [(5,3),(9,10)],[(5,2),(8,7)],[(6,3),(9,8)],[(7,4),(12,13)],
        [(8,5),(13,14)],[(8,4),(9,6),(12,11),(14,15)],[(9,5),(13,12)],[(10,6),(14,13)]]

#     1
#    2 3
#   4 5 6
#  7 8 9 A
# B C D E F 

def tablero():
    tablero=[]
    c=1
    for fila in range(5):
        tablero.append([])
        for columna in range(fila+1):
            if c==10:
                tablero[fila].append('A')
            elif c==11:
                tablero[fila].append('B')
            elif c==12:
                tablero[fila].append('C')
            elif c==13:
                tablero[fila].append('D')
            elif c==14:
                tablero[fila].append('E')
            elif c==15:
                tablero[fila].append('F')
            else:
                tablero[fila].append(str(c))
            c+=1
    return tablero

def imprimir(tablero):
    for fila in tablero:
        print("{:^22}".format(str(fila)))

def peones(pin):
    pines = [1]*15
    pines[pin] = 0
    return pines

def movimiento(movs, inicio):
    p=peones(inicio)
    camino=backtracking(p, movs, [0]*13, 0)
    return camino

def backtracking(pines, movs, pila, cont):
    if sum(pines)==1:
        return pila
    movimientos=avanzar(pines.copy(), movs)
    for i in movimientos:
        nueva_pila = pila.copy()
        nueva_pila[cont] = i
        camino = backtracking(modificar(pines.copy(), i), movs, nueva_pila, cont+1)
        if camino:
            return camino
    return False

def avanzar(pines, movs):
    movimientos=[]
    for fila in range(len(pines)):
        for columna in movs[fila]:
            if pines[fila] and pines[columna[0]-1] and not pines[columna[1]-1]:
                movimientos.append((fila, columna[0]-1, columna[1]-1))
    return movimientos

def modificar(pines, movimiento):
    pines[movimiento[0]]=0
    pines[movimiento[1]]=0
    pines[movimiento[2]]=1
    return pines

def pines_a_tablero(pines):
    tablero=[]
    c=0
    for fila in range(5):
        tablero.append([])
        for columna in range(fila+1):
            tablero[fila].append(pines[c])
            c+=1
    return tablero

def mostrar_solucion(pines, movimientos):
    print("\nEstado inicial:")
    imprimir(pines_a_tablero(pines))

    for i, mov in enumerate(movimientos):
        print(f"\nMovimiento {i+1}: {mov[0]+1} salta {mov[1]+1} y llega al {mov[2]+1}")
        pines = modificar(pines, mov)
        imprimir(pines_a_tablero(pines))

imprimir(tablero())
conversion = {'1':1, '2':2, '3':3,'4':4, '5':5, '6':6,'7':7, '8':8, '9':9,
    'A':10, 'B':11, 'C':12,'D':13, 'E':14, 'F':15}
entrada=input("Selecciona la pieza a retirar: ").upper()
pin=conversion[entrada]-1
#tab=juego(pin)
#imprimir(tab)
r=movimiento(movs,pin)
print("-----------------Solucion-----------------")
pines_inicial = peones(pin)
mostrar_solucion(pines_inicial, r)