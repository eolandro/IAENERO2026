N = 8

movimientos = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def es_valido(fila, columna, tablero):
    return 0 <= fila < N and 0 <= columna < N and tablero[fila][columna] == -1

def contar_salidas(fila, columna, tablero):
    salidas = 0
    for df, dc in movimientos:
        nueva_fila = fila + df
        nueva_columna = columna + dc
        if es_valido(nueva_fila, nueva_columna, tablero):
            salidas += 1
    return salidas

def obtener_movimientos_ordenados(fila, columna, tablero):
    opciones = []

    for df, dc in movimientos:
        nueva_fila = fila + df
        nueva_columna = columna + dc

        if es_valido(nueva_fila, nueva_columna, tablero):
            salidas = contar_salidas(nueva_fila, nueva_columna, tablero)
            opciones.append((salidas, nueva_fila, nueva_columna))

    opciones.sort()
    return opciones

def recorrido_caballo(fila, columna, paso, tablero):
    if paso == N * N:
        return True

    siguientes = obtener_movimientos_ordenados(fila, columna, tablero)

    for _, nueva_fila, nueva_columna in siguientes:
        tablero[nueva_fila][nueva_columna] = paso

        if recorrido_caballo(nueva_fila, nueva_columna, paso + 1, tablero):
            return True

        tablero[nueva_fila][nueva_columna] = -1

    return False

def imprimir_tablero_ajedrez(tablero):
    columnas = ["A", "B", "C", "D", "E", "F", "G", "H"]

    print("-------- RECORRIDO DEL CABALLO --------")
    print("       " + "".join(f"{col:^6}" for col in columnas))
    print("    +" + "------" * N + "+")

    for fila in range(N):
        numero_fila = 8 - fila
        print(f" {numero_fila}  |", end="")

        for columna in range(N):
            print(f"{tablero[fila][columna]:^6}", end="")

        print("|")
        print("    +" + "------" * N + "+")

    print("       " + "".join(f"{col:^6}" for col in columnas))
    print()

def convertir_a_indices(posicion):
    columna_letra = posicion[0].upper()
    fila_numero = int(posicion[1])

    columna = ord(columna_letra) - ord('A')
    fila = 8 - fila_numero

    return fila, columna

def main():
    tablero = [[-1 for _ in range(N)] for _ in range(N)]

    print("PROBLEMA DEL CABALLO CON HEURÍSTICA DE WARNSDORFF")
    print("Escribe la posición inicial como en ajedrez, por ejemplo: A1, C5, H8")

    posicion = input("Ingresa la posición inicial del caballo: ").strip()

    if len(posicion) != 2:
        print("Entrada inválida.")
        return

    columna_letra = posicion[0].upper()
    fila_caracter = posicion[1]

    if columna_letra < 'A' or columna_letra > 'H' or fila_caracter < '1' or fila_caracter > '8':
        print("Posición inválida.")
        return

    fila, columna = convertir_a_indices(posicion)
    tablero[fila][columna] = 0

    if recorrido_caballo(fila, columna, 1, tablero):
        imprimir_tablero_ajedrez(tablero)
    else:
        print("No se encontró solución desde esa posición.")

if __name__ == "__main__":
    main()