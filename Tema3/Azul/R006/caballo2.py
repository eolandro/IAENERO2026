# Tamaño del tablero
N = 8

# Los 8 movimientos posibles del caballo en forma de "L"
MOVIMIENTOS = [
    (-2, -1), (-2, 1),
    (-1, -2), (-1, 2),
    ( 1, -2), ( 1, 2),
    ( 2, -1), ( 2, 1)
]

def crear_tablero():
    """Crea un tablero N x N inicializado en ceros."""
    tablero = []
    for i in range(N):
        fila = []
        for j in range(N):
            fila.append(0)
        tablero.append(fila)
    return tablero


def es_valida(fila, columna, tablero):
    """Verifica si una posicion esta dentro del tablero y no ha sido visitada."""
    if 0 <= fila < N and 0 <= columna < N and tablero[fila][columna] == 0:
        return True
    return False


def contar_salidas(fila, columna, tablero):
    """Cuenta cuantos movimientos validos tiene el caballo desde una posicion dada."""
    contador = 0
    for df, dc in MOVIMIENTOS:
        nueva_fila = fila + df
        nueva_columna = columna + dc
        if es_valida(nueva_fila, nueva_columna, tablero):
            contador += 1
    return contador


def obtener_siguientes_movimientos(fila, columna, tablero):
    """lista de movimientos validos """
    candidatos = []
    for df, dc in MOVIMIENTOS:
        nueva_fila = fila + df
        nueva_columna = columna + dc
        if es_valida(nueva_fila, nueva_columna, tablero):
            # Contar las salidas desde la casilla candidata
            grado = contar_salidas(nueva_fila, nueva_columna, tablero)
            candidatos.append((grado, nueva_fila, nueva_columna))

    candidatos.sort(key=lambda x: x[0])

    resultado = []
    for grado, f, c in candidatos:
        resultado.append((f, c))
    return resultado


def resolver(tablero, fila, columna, paso):
    """Cada estado es el tablero parcialmente lleno con el caballo en una posicion.
    Los operadores son los 8 movimientos validos del caballo."""

    # Caso base: si ya se visitaron todas las casillas
    if paso > N * N:
        return True

    siguientes = obtener_siguientes_movimientos(fila, columna, tablero)

    # Explorar cada movimiento candidato
    for nueva_fila, nueva_columna in siguientes:
        # Marcar la casilla con el numero de paso actual
        tablero[nueva_fila][nueva_columna] = paso

        # Llamada recursiva para el siguiente paso
        if resolver(tablero, nueva_fila, nueva_columna, paso + 1):
            return True

        # Backtracking: desmarcar la casilla si no llevo a solucion
        tablero[nueva_fila][nueva_columna] = 0

    # No se encontro solucion desde esta posicion
    return False


def imprimir_tablero(tablero):
    """Imprime el tablero como una cuadricula de numeros alineados."""
    # Calcular el ancho necesario para alinear los numeros
    ancho = len(str(N * N)) + 1

    for fila in tablero:
        linea = ""
        for valor in fila:
            linea += str(valor).rjust(ancho)
        print(linea)


def pedir_posicion_inicial():
    """Pide al usuario la fila y columna iniciales del caballo."""
    print("=== Problema del Recorrido del Caballo ===")
    print(f"Tablero de {N}x{N} casillas\n")

    while True:
        try:
            fila = int(input("Ingrese la fila inicial (1 a {}): ".format(N)))
            columna = int(input("Ingrese la columna inicial (1 a {}): ".format(N)))

            # Convertir a indices base 0
            fila -= 1
            columna -= 1

            if 0 <= fila < N and 0 <= columna < N:
                return fila, columna
            else:
                print("Error: los valores deben estar entre 1 y {}\n".format(N))
        except ValueError:
            print("Error: ingrese numeros enteros validos.\n")


def principal():
    """Funcion principal del programa."""
    # Pedir posicion inicial al usuario
    fila_inicial, columna_inicial = pedir_posicion_inicial()

    # Crear el tablero vacio
    tablero = crear_tablero()

    # Marcar la posicion inicial como paso 1
    tablero[fila_inicial][columna_inicial] = 1

    # Intentar resolver desde la posicion inicial
    if resolver(tablero, fila_inicial, columna_inicial, 2):
        print("¡Solucion encontrada!\n")
        imprimir_tablero(tablero)
    else:
        print("\nNo se encontro solucion desde la posicion ({}, {}).".format(
            fila_inicial + 1, columna_inicial + 1))

if __name__ == "__main__":
    principal()
