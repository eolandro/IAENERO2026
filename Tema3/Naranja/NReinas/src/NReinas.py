import matplotlib.pyplot as plt

# La cantidad de reinas a colocar en el tablero.
n = 4

# Estructuras de control
columna = [False]*n
diag_izq = [False]*(2*n)
diag_der = [False]*(2*n)

soluciones = []
tablero = [-1]*n  # Columna donde está la reina

"""
#función recursiva
def backtrack(y,n,contador):
    if(y==n):
        #retorna
        return contador + 1
    
    for x in range(n):
        
        global columna
        global diag_izq
        global diag_der
        
        if(columna[x] or diag_izq[x+y] or diag_der[x-y+n-1]): 
            continue
        #colocamos una reina
        columna[x] = diag_izq[x+y] = diag_der[x-y+n-1] = True
        #enviamos la fila siguiente
        contador = backtrack(y+1,n,contador)
        #quitamos la reina para probar otras posibilidades
        columna[x] = diag_izq[x+y] = diag_der[x-y+n-1] = False
        
    return contador
"""
# Backtracking

# El backtracking en un algoritmo de busqueda que busca las soluciones posibles
# al crearlas de manera recursiva, abandonando a los candidatos mediante una poda.
# Utiliza recursividad, busqueda en profundidad; Este algoritmo es conocido por ser de fuerza bruta.

def backtrack(fila):
    if fila == n:
        imprtablero("Recorrido completo")
        # Se guarda la solución completa encontrada.
        soluciones.append(tablero.copy())
        return
    
    movs = False
    
    for col in range(n):
        if columna[col] or diag_izq[fila+col] or diag_der[fila-col+n-1]:
            continue

        movs = True
        
        # Este paso permite colocar a una reina en la posición actual y marcar las columnas y diagonales como atacadas.
        tablero[fila] = col
        columna[col] = diag_izq[fila+col] = diag_der[fila-col+n-1] = True
        imprtablero(f"Colocando reina en fila {fila + 1}, columna {col + 1}")

        backtrack(fila+1)
        
        # Este proceso es el paso de retroceso, donde se quita la reina colocada previamente y se desmarcan las columnas y diagonales para probar otras posibilidades.
        tablero[fila] = -1
        columna[col] = diag_izq[fila+col] = diag_der[fila-col+n-1] = False
        imprtablero(f"Quitando reina de fila {fila + 1}, columna {col + 1}")
    
    if not movs:
        imprtablero("No hay movimientos válidos, retrocediendo...")

# Esta funcion imprime el recorrido en consola.
# Nota: Este tablero si me gusto xd.
def imprtablero(mensaje=None):
    for fila in range(n):
        linea = []
        for col in range(n):
            if tablero[fila] == col:
                linea.append("Q")
            else:
                atacada = False
                for f in range(n):
                    c = tablero[f]
                    if c == -1:
                        continue
                    if (c == col or f == fila or (f + c == fila + col) or (f - c == fila - col)):
                        atacada = True
                        break
                if atacada:
                    linea.append("x")
                else:
                    linea.append(".")
        print(" ".join(linea))
    
    if mensaje:
        print(mensaje)
    
    print("-"*12)

# Esta función dibuja SOLO las soluciones completas encontradas.
# Nota: En mi mente se veia mas bonito.
def dibujar_tablero(sol):
    fig, ax = plt.subplots()

    # Colores para cada reina
    colores = ['blue', 'green', 'red']
    
    for i in range(n+1):
        ax.plot([0, n], [i, i], color='black')
        ax.plot([i, i], [0, n], color='black')

    # Matriz para evitar sobreescribir ataques
    ataques = [[None for _ in range(n)] for _ in range(n)]
    
    """
    for fila in range(n):
        col = sol[fila]
        ax.text(col+0.5, fila+0.5, 'Q', fontsize=20, ha='center', va='center')
    """
    # Marcar ataques por cada reina
    for fila in range(n):
        col = sol[fila]
        color = colores[fila % len(colores)]
        
        for f in range(n):
            for c in range(n):
                
                if f == fila and c == col:
                    continue
                
                # condiciones de ataque
                if (c == col or f == fila or (f + c == fila + col) or (f - c == fila - col)):
                    if ataques[f][c] is None:
                        ataques[f][c] = color
    
    # Dibujar ataques
    for f in range(n):
        for c in range(n):
            if ataques[f][c] is not None:
                ax.text(c+0.5, f+0.5, 'x', color=ataques[f][c], fontsize=14, ha='center', va='center')
    
    # Dibujar reinas encima
    for fila in range(n):
        col = sol[fila]
        ax.text(col+0.5, fila+0.5, 'Q', fontsize=20, ha='center', va='center', color='black')
        
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.invert_yaxis()
    # Guardar la imagen de cada solución
    plt.savefig(f'solucion_{sol}.png')
    plt.show()


# ejecutar
backtrack(0)

print(f"Total de soluciones: {len(soluciones)}")

# graficar cada solución
for sol in soluciones:
    dibujar_tablero(sol)

# print(backtrack(0,n,contador))