import random
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Es el tablero estandar del ajedres, un 8 x 8, siendo 64 casillas las disponibles para los movimientos.
TAMANO = 8

# Estos son los movimientos posibles del caballo.
MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

# Conversión de posiciones
def conversion(pos):
    # Nota: pos es la cadena a convertir.
    # Este es un conversor generico, por lo que convierte todas las letras.
    col = ord(pos[0].upper()) - ord('A')
    fila = int(pos[1]) - 1
    return col, fila

# Validación de movimientos

# Esta función verifica si la casilla (x, y) está dentro del tablero y no ha sido visitada.
def cas_disponible(x, y, tablero):
    return 0 <= x < TAMANO and 0 <= y < TAMANO and tablero[y][x] == 0

# Esta función cuenta cuántos movimientos válidos tiene el caballo desde la posición (x, y) en el tablero actual.
def grado(x, y, tablero):
    count = 0
    # dx, dy = Cambios de movimiento.
    for dx, dy in MOVES:
        # nx, ny = Nueva posición después de aplicar el movimiento.
        nx, ny = x + dx, y + dy
        if cas_disponible(nx, ny, tablero):
            count += 1
    return count

# Backtracking

# El backtracking en un algoritmo de busqueda que busca las soluciones posibles
# al crearlas de manera recursiva, abandonando a los candidatos mediante una poda.
# Utiliza recursividad, busqueda en profundidad; Este algoritmo es conocido por ser de fuerza bruta. 
"""
def Resolver (row, col, counter):
    global TAMANO
    global numSol
    for i in [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]:
        new_x = row + i[0]
        new_y = col + i[1]
        if new_x < TAMANO and new_x >= 0 and new_y < TAMANO and new_y >= 0 and tablero[new_x][new_y] == 0:
            tablero[new_x][new_y] = counter
            if counter >= TAMANO * TAMANO:
                numSol += 1
                print("------------------------------------------------------")
                print("#", numSol ,", tiempo:", time.time() - tiempo)
                print(tablero)
            else:
                Resolver(new_x, new_y, counter + 1)
            tablero[new_x][new_y] = 0
"""

# Warnsdorff

# Es un algoritmo de búsqueda heurística, que basicamente es:
# "inicia en cualquier casilla e ir siempre a una casilla que tenga la menor cantidad de casillas vecinas no visitadas"
# Este algoritmo/regla es muy especifico para resolver el problema del caballo de manera eficiente.
# Nota: Corroborado que si funciona demasiado bien, creanme.

def Resolver(col, fila):
    # Se crea el tablero con ceros.
    # dtype=np.int32 es para que los números sean enteros de 32 bits (4 bytes).
    # En resumen: Es una optimización para ahorrar memoria.
    tablero = np.zeros((TAMANO, TAMANO), dtype=np.int32)

    x, y = col, fila
    # Inicia en 1
    tablero[y][x] = 1

    # Este bucle controla el movimiento del caballo.
    for paso in range(2, TAMANO * TAMANO + 1):
        candidatos = []

        # Se calculan los movimientos posibles del caballo
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            # Verifica si la nueva posición es válida y no ha sido visitada.
            if cas_disponible(nx, ny, tablero):
                candidatos.append((grado(nx, ny, tablero), nx, ny))

        # Si no hay candidatos disponibles, significa que el caballo no puede continuar su recorrido.
        if not candidatos:
            return None

        # Esta parte ordena a los candidatos por "grado" (Las casillas donde quedan menos movimientos disponibles).
        candidatos.sort(key=lambda t: t[0])

        # Se selecciona al candidato con menor grado.
        min_deg = candidatos[0][0]
        # Filtra a los candidatos y solo quedan los que empatan en el mejor valor.
        mejores = [c for c in candidatos if c[0] == min_deg]

        # Se elige de manera aleatoria a un candidato.
        # _ = Grado (que no se usa).
        # x = Nueva posición de x.
        # y = Nueva posición de y.
        _, x, y = random.choice(mejores)
        # Marca el paso actual en el tablero.
        tablero[y][x] = paso

    return tablero

# Gráfica

# Esta función busca la posición del valor dado en el tablero y devuelve sus coordenadas.
def buscarCaballo(valor, tablero):
    for fila in range(TAMANO):
        for col in range(TAMANO):
            if tablero[fila][col] == valor:
                return fila, col

# Esta función solo crea el tablero de manera gráfica ... y ya, esta no es ciencia de cohete.
def pintarTableroGraf(tablero):
    for x in range(TAMANO + 1):
        plt.plot([0, TAMANO], [x, x], color='gray')
        plt.plot([x, x], [0, TAMANO], color='gray')

    X = []
    Y = []

    for i in range(1, TAMANO * TAMANO + 1):
        fila, col = buscarCaballo(i, tablero)
        X.append(col + 0.5)
        Y.append(fila + 0.5)
        plt.text(col + 0.5, fila + 0.5, str(i))

    plt.plot(X, Y)
    plt.suptitle("Horse's Tour (Knight's Tour)", fontsize=15)
    plt.xticks(
        [i + 0.5 for i in range(TAMANO)],
        [chr(ord('A') + i) for i in range(TAMANO)]
    )

    plt.yticks(
        [i + 0.5 for i in range(TAMANO)],
        [str(i + 1) for i in range(TAMANO)]
    )

    plt.gca().set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.savefig('horsetour.png') 
    plt.show()

# Muestra a la Golshi.
def golshi():
    img = mpimg.imread('horsetour/golshi.jpeg')
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# Función main, donde ocurre la orquesta.
def main():
    while True:
        try:
            print("Bienvenido/a al Horse's Tour, elige la posición inicial del caballo")
            print("Formato: Letra (A-H) seguida de número (1-8), por ejemplo: A1, B4, H8")
            pos = input("Introduce posición inicial: ").strip().upper()

            # El input debe tener exactamente 2 caracteres: una letra y un número.
            if len(pos) != 2:
                raise ValueError("Formato inválido")

            col_letra = pos[0]
            fila_num = pos[1]

            # Validar rango A-H y 1-8
            if col_letra < 'A' or col_letra > 'H':
                raise ValueError("Columna fuera de rango")
            if fila_num < '1' or fila_num > '8':
                raise ValueError("Fila fuera de rango")

            x, y = conversion(pos)
            break 

        except Exception as e:
            print(f"Entrada inválida: {e}. Intenta de nuevo.\n")

    # Mide el tiempo de ejecución del algoritmo.
    inicio = time.time()
    resultado = Resolver(x, y)
    fin = time.time()

    # Si resultado no es None, se encontró una solución y se muestra el tablero y el tiempo.
    # De lo contrario, se indica que no se encontró solución.
    # Nota: La regla de Warnsdorff deberia se capaz de encontrar la solución en la mayoría de los casos.
    if resultado is not None:
        print("\nTablero solución:\n")
        print(resultado)
        print(f"\nTiempo: {fin - inicio:.6f} segundos")
        pintarTableroGraf(resultado)
        golshi()
    else:
        print("No se encontró solución (intenta de nuevo)")

if __name__ == "__main__":
    main()