"""
El problema de las 4 reinas se resuelve matemáticamente colocando 4 reinas en un tablero 
sin que se ataquen (misma fila, columna o diagonal). La solución se encuentra usando 
algoritmos de búsqueda con retroceso (backtracking), 
probando posiciones y descartando las que generan conflictos, 
resultando en dos soluciones principales. 

 Podemos representarlo mejor en una permutacion asi
 De esta manera cada posicion corresponde a una fila
 y el numero dentro de ellas representa la columna
 reinas = (1,3,2,4)
 
 Se comparan dos reinas en posiciones (f1,c1) y (f2,c2)
 Condicion de no amenaza |c1-c2| != |f1-f2|
 En nuestro caso |1-4| = |1-4| se amenazan o estan en la misma columna 
"""


VERDE = "\033[92m"
ROJO  = "\033[91m"
RESET = "\033[0m"

tablero =  [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0,],
    [0,0,0,0,]
]



def imprimir_tablero(tablero, array_reinas, solucion=False, fallo=False):
    reinas_nombres = ["R1", "R2", "R3", "R4"]
    ancho = 5
    separador = "  +" + ("-" * ancho + "+") * 4
    
    if solucion:
        color = VERDE
    elif fallo:
        color = ROJO
    else:
        color = ""

    print(color + separador)
    for fila in range(4):
        fila_str = "  |"
        for col in range(4):
            if fila < len(array_reinas) and array_reinas[fila] - 1 == col:
                texto = reinas_nombres[fila]
            else:
                texto = "."
            fila_str += texto.center(ancho) + "|"
        print(fila_str)
        print(separador)
    print(RESET)

def es_factible(array_reinas):

    f2 = len(array_reinas)-1
    c2 = array_reinas[f2]

    for fila  in range (len(array_reinas)-1):
        f1 = fila
        c1 = array_reinas[f1]

        if  (abs(f1 - f2) == abs(c1-c2)) or  (c1==c2):
            return False
    
    return True

def posicionar_reinas(array_reinas):
    if len(array_reinas) == 4:
        print(VERDE + " *** SOLUCIÓN ENCONTRADA ***" + RESET)
        imprimir_tablero(tablero, array_reinas, solucion=True)
        return

    for numero in [1, 2, 3, 4]:
        array_reinas.append(numero)

        if es_factible(array_reinas):
            imprimir_tablero(tablero, array_reinas)
            posicionar_reinas(array_reinas)
        else:
            print(ROJO + " !!! CONFLICTO, RETROCEDIENDO !!!" + RESET)
            imprimir_tablero(tablero, array_reinas, fallo=True)  

        array_reinas.pop()

print("\n * * *  PROBLEMA DE LAS 4 REINAS \n")
posicionar_reinas([])










