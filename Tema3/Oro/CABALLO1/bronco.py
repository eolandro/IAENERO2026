tablero =  [
    ['C1', '0', 'C2'],
    ['0', '0', '0'],
    ['C3', '0', 'C4'],
]

movimientos = {
    (0,0): {'d': (1,2), 'i': (2,1)},
    (0,2): {'d': (2,1), 'i': (1,0)},
    (2,0): {'d': (0,1), 'i': (1,2)},
    (2,2): {'d': (1,0), 'i': (0,1)},
    (1,0): {'d': (0,2), 'i': (2,2)},
    (1,2): {'d': (2,0), 'i': (0,0)},
    (0,1): {'d': (2,2), 'i': (2,0)},
    (2,1): {'d': (0,0), 'i': (0,2)},
}

def giro(f,c,dir):
    movimiento = movimientos.get((f,c))
    movimiento = movimiento.get(dir)
    return movimiento[0],movimiento[1]

def imprimir_tablero(tablero):
    ancho = 6
    separador = "  +" + ("-" * ancho + "+") * 3
    print(separador)
    for fila in tablero:
        fila_str = "  |"
        for celda in fila:
            texto = " " if celda == "0" else celda
            fila_str += texto.center(ancho) + "|"
        print(fila_str)
        print(separador)
    print()

def buscar_caballo(tablero,target):
    f = 0
    while True:
        if target in tablero[f]:
            c = tablero[f].index(target)
            return f,c
        else:
            f += 1
        
def moverCaballos(tablero,dir):

    caballos = ["C1","C2","C3","C4"]
    for i in range(4):
        for target in caballos:
            f,c = buscar_caballo(tablero,target)
            fn,cn = giro(f,c,dir)
            tablero[fn][cn] = target
            tablero[f][c]= "0"
        imprimir_tablero(tablero)

        
print("\n * * *  PROBLEMA DEL CABALLO 1 \n")
print("\n * * *  TABLERO INICIAL * * * \n")
imprimir_tablero(tablero)
res = input(" Indica en que direccion se va a mover I(Izq), D(Der) -> ").lower()
moverCaballos(tablero,res)