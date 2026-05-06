# Representación del tablero triangular de 15 posiciones:
#       0
#      1 2
#     3 4 5
#    6 7 8 9
#  10 11 12 13 14

MOVIMIENTOS = [
    (0, 1, 3), (0, 2, 5), (1, 3, 6), (1, 4, 8), (2, 4, 7), (2, 5, 9),
    (3, 1, 0), (3, 4, 5), (3, 6, 10), (3, 7, 12), (4, 7, 11), (4, 8, 13),
    (5, 2, 0), (5, 4, 3), (5, 8, 12), (5, 9, 14), (6, 3, 1), (6, 7, 8),
    (7, 4, 2), (7, 8, 9), (8, 4, 1), (8, 7, 6), (9, 5, 2), (9, 8, 7),
    (10, 6, 3), (10, 11, 12), (11, 7, 4), (11, 12, 13), (12, 7, 3),
    (12, 8, 5), (12, 11, 10), (12, 13, 14), (13, 8, 4), (13, 12, 11),
    (14, 9, 5), (14, 13, 12)
]


def tablero_a_texto(tablero):
    simbolos = {0: "_", 1: "o"}
    idx = 0
    filas = 5
    lineas = []
    for i in range(1, filas + 1):
        linea = "r%d: " % i
        for _ in range(i):
            if idx < len(tablero):
                linea += simbolos.get(tablero[idx], " ") + " "
                idx += 1
        lineas.append(linea.rstrip())
    return "\n".join(lineas)


def imprimir_tablero(tablero):
    print(tablero_a_texto(tablero))
    print()


def guardar_en_txt(texto, modo="a"):
    with open("comesolo_salida.txt", modo, encoding="utf-8") as archivo:
        archivo.write(texto + "\n")


def es_solucion(tablero):
    return sum(tablero) == 1


def resolver(tablero, camino):
    if es_solucion(tablero):
        return camino

    for inicio, medio, fin in MOVIMIENTOS:
        if tablero[inicio] == 1 and tablero[medio] == 1 and tablero[fin] == 0:
            tablero[inicio], tablero[medio], tablero[fin] = 0, 0, 1
            solucion = resolver(tablero, camino + [(inicio, medio, fin)])
            if solucion:
                return solucion
            tablero[inicio], tablero[medio], tablero[fin] = 1, 1, 0
    return None


def aplicar(tablero, movimiento):
    inicio, medio, fin = movimiento
    tablero[inicio], tablero[medio], tablero[fin] = 0, 0, 1


def guardar_solucion(tablero_inicial, solucion):
    guardar_en_txt("JUEGO COME SOLO", "w")
    guardar_en_txt("\nInicio:\n", "a")
    guardar_en_txt(tablero_a_texto(tablero_inicial), "a")

    tablero_actual = tablero_inicial.copy()
    for i, movimiento in enumerate(solucion, start=1):
        inicio, medio, fin = movimiento
        aplicar(tablero_actual, movimiento)
        texto = "\nJugada %d\n" % i
        texto += "mov: %d -> %d (salto %d)\n\n" % (inicio, fin, medio)
        texto += tablero_a_texto(tablero_actual)
        guardar_en_txt(texto, "a")

    guardar_en_txt("\nFin", "a")


def mostrar_en_consola(tablero_inicial, solucion):
    print("\nInicio:\n")
    imprimir_tablero(tablero_inicial)
    tablero_actual = tablero_inicial.copy()
    for i, movimiento in enumerate(solucion, start=1):
        inicio, medio, fin = movimiento
        aplicar(tablero_actual, movimiento)
        print("Jugada", i)
        print("mov:", inicio, "->", fin, "(salto", medio, ")\n")
        imprimir_tablero(tablero_actual)


def main():
    print("Come solo")
    try:
        vacia = int(input("Casilla vacia (0-14): "))
        if not (0 <= vacia <= 14):
            raise ValueError
    except ValueError:
        print("Indice no valido.")
        return

    tablero = [1] * 15
    tablero[vacia] = 0
    tablero_inicial = tablero.copy()
    solucion = resolver(tablero, [])

    if solucion:
        print("Solucion encontrada.\n")
        mostrar_en_consola(tablero_inicial, solucion)
        guardar_solucion(tablero_inicial, solucion)
        print("Archivo -> comesolo_salida.txt")
    else:
        print("No se encontro solucion.")
        guardar_en_txt("No se encontro solucion.", "w")


if __name__ == "__main__":
    main()