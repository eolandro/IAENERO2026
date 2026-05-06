N = 8
MOVS = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def es_valido(fila, col, tablero):
    return 0 <= fila < N and 0 <= col < N and tablero[fila][col] == -1


def contar_salidas(fila, col, tablero):
    total = 0
    for df, dc in MOVS:
        nf, nc = fila + df, col + dc
        if es_valido(nf, nc, tablero):
            total += 1
    return total


def movimientos_ordenados(fila, col, tablero):
    opciones = []
    for df, dc in MOVS:
        nf, nc = fila + df, col + dc
        if es_valido(nf, nc, tablero):
            opciones.append((contar_salidas(nf, nc, tablero), nf, nc))
    opciones.sort()
    return opciones


def recorrer(fila, col, paso, tablero):
    if paso == N * N:
        return True

    for _, nf, nc in movimientos_ordenados(fila, col, tablero):
        tablero[nf][nc] = paso
        if recorrer(nf, nc, paso + 1, tablero):
            return True
        tablero[nf][nc] = -1
    return False


def imprimir_tablero(tablero):
    letras = ["A", "B", "C", "D", "E", "F", "G", "H"]
    print("\nRecorrido completo 0..63")
    print("    " + " | ".join(letras))
    print("   " + "-" * (N * 4))
    for f in range(N):
        fila_num = 8 - f
        linea = ["%2d" % fila_num]
        for c in range(N):
            linea.append("%2d" % tablero[f][c])
        print(" | ".join(linea))
    print()


def convertir(pos):
    col = ord(pos[0].upper()) - ord("A")
    fila = 8 - int(pos[1])
    return fila, col


def main():
    tablero = [[-1 for _ in range(N)] for _ in range(N)]
    print("Recorrido del caballo")
    pos = input("inicio (ej A1): ").strip()

    if len(pos) != 2 or pos[0].upper() not in "ABCDEFGH" or pos[1] not in "12345678":
        print("Entrada no valida.")
        return

    fila, col = convertir(pos)
    tablero[fila][col] = 0

    if recorrer(fila, col, 1, tablero):
        imprimir_tablero(tablero)
    else:
        print("No se encontro recorrido completo.")


if __name__ == "__main__":
    main()