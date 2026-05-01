ETIQUETAS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

# Tabla de movimientos válidos
MOVIMIENTOS = {
    0:  [(1, 3), (2, 5)],
    1:  [(3, 6), (4, 8)],
    2:  [(4, 7), (5, 9)],
    3:  [(1, 0), (4, 5), (6, 10), (7, 12)],
    4:  [(7, 11), (8, 13)],
    5:  [(2, 0), (4, 3), (8, 12), (9, 14)],
    6:  [(3, 1), (7, 8)],
    7:  [(4, 2), (8, 9)],
    8:  [(4, 1), (7, 6)],
    9:  [(5, 2), (8, 7)],
    10: [(6, 3), (11, 12)],
    11: [(7, 4), (12, 13)],
    12: [(7, 3), (8, 5), (11, 10), (13, 14)],
    13: [(8, 4), (12, 11)],
    14: [(9, 5), (13, 12)],
}


def simbolo(tablero, i):
    """Devuelve la etiqueta si hay ficha, o '.' si está vacía"""
    return ETIQUETAS[i] if tablero[i] else '.'


def mostrar_tablero(tablero):
    """Muestra el tablero con el estado actual"""
    s = lambda i: simbolo(tablero, i)
    lineas = [
        "            " + s(0),
        "           / \\",
        "          " + s(1) + "   " + s(2),
        "         / \\ / \\",
        "        " + s(3) + "   " + s(4) + "   " + s(5),
        "       / \\ / \\ / \\",
        "      " + s(6) + "   " + s(7) + "   " + s(8) + "   " + s(9),
        "     / \\ / \\ / \\ / \\",
        "    " + s(10) + "   " + s(11) + "   " + s(12) + "   " + s(13) + "   " + s(14),
    ]
    for linea in lineas:
        print("  " + linea)


def mostrar_tablero_etiquetas():
    """Muestra el tablero con todas las etiquetas de referencia"""
    tablero_lleno = [True] * 15
    mostrar_tablero(tablero_lleno)


def obtener_movimientos_validos(tablero):
    """Devuelve lista de movimientos válidos: (origen, intermedia, destino)"""
    validos = []
    for origen in range(15):
        # Solo se mueven fichas presentes
        if not tablero[origen]:
            continue
        for intermedia, destino in MOVIMIENTOS[origen]:
            # La intermedia debe tener ficha y el destino estar vacío
            if tablero[intermedia] and not tablero[destino]:
                validos.append((origen, intermedia, destino))
    return validos


def contar_fichas(tablero):
    """Cuenta cuántas fichas quedan en el tablero"""
    return sum(tablero)


def resolver(tablero, pasos):
    """Resuelve el puzzle con backtracking recursivo"""
    # Verificar si queda solo una ficha
    if contar_fichas(tablero) == 1:
        return True

    # Obtener movimientos válidos
    movimientos = obtener_movimientos_validos(tablero)

    # Sin movimientos = callejón sin salida
    if not movimientos:
        return False

    # Probar cada movimiento
    for origen, intermedia, destino in movimientos:
        # Copiar tablero para no corromper el estado
        nuevo_tablero = tablero[:]

        # Aplicar movimiento
        nuevo_tablero[origen] = False
        nuevo_tablero[intermedia] = False
        nuevo_tablero[destino] = True

        # Registrar paso
        pasos.append((origen, intermedia, destino))

        # Intentar resolver recursivamente
        if resolver(nuevo_tablero, pasos):
            return True

        # Backtrack: deshacer el paso
        pasos.pop()

    return False


def etiqueta(indice):
    """Convierte índice interno (0-14) a etiqueta (1-F)"""
    return ETIQUETAS[indice]


def imprimir_solucion_texto(pasos):
    """Imprime la lista de movimientos en formato texto"""
    print("  ┌──────────────────────────────────────┐")
    print("  │       LISTA DE MOVIMIENTOS            │")
    print("  ├──────────────────────────────────────┤")
    for i, (origen, intermedia, destino) in enumerate(pasos, 1):
        e_o = etiqueta(origen)
        e_i = etiqueta(intermedia)
        e_d = etiqueta(destino)
        print(f"  │  Paso {i:2d}: {e_o} salta {e_i} -> {e_d}            │")
    print("  └──────────────────────────────────────┘")


def imprimir_solucion_grafica(pasos, posicion_vacia):
    """Muestra la secuencia gráfica de cada movimiento"""
    print("  ╔══════════════════════════════════════╗")
    print("  ║       SECUENCIA GRAFICA              ║")
    print("  ╚══════════════════════════════════════╝")
    print()

    # Estado inicial
    tablero_actual = [True] * 15
    tablero_actual[posicion_vacia] = False

    print("  ~~~ Estado inicial ~~~")
    mostrar_tablero(tablero_actual)
    print()

    # Mostrar cada paso
    for i, (origen, intermedia, destino) in enumerate(pasos, 1):
        # Aplicar movimiento
        tablero_actual[origen] = False
        tablero_actual[intermedia] = False
        tablero_actual[destino] = True

        fichas = contar_fichas(tablero_actual)
        e_o = etiqueta(origen)
        e_d = etiqueta(destino)

        print(f"  ~~~ Paso {i}: {e_o} -> {e_d}  (quedan {fichas} fichas) ~~~")
        mostrar_tablero(tablero_actual)
        print()

    print("  ** Queda 1 ficha. Puzzle resuelto. **")


def main():
    """Función principal del programa"""
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║    COME SOLO                         ║")
    print("  ║    Tablero Triangular (15 posiciones)║")
    print("  ╚══════════════════════════════════════╝")
    print()

    # Mostrar tablero de referencia
    print("  Posiciones del tablero:")
    print()
    mostrar_tablero_etiquetas()
    print()

    # Pedir posición vacía al usuario
    while True:
        entrada = input("  Cual posicion estara vacia? (1-F): ").strip().upper()
        if len(entrada) == 1 and entrada in '123456789ABCDEF':
            # Convertir hex a índice 0-14
            posicion_vacia = int(entrada, 16) - 1
            break
        print("  Entrada no valida. Usa un caracter del 1 al F.")

    print()
    print(f"  Posicion vacia seleccionada: {ETIQUETAS[posicion_vacia]}")
    print("  Resolviendo con backtracking...")
    print()

    # Crear tablero inicial
    tablero = [True] * 15
    tablero[posicion_vacia] = False

    # Resolver 
    pasos = []
    if resolver(tablero, pasos):
        print("  SOLUCION ENCONTRADA!")
        print()

        # Parte 1: Lista de movimientos en texto
        imprimir_solucion_texto(pasos)
        print()

        # Parte 2: Secuencia gráfica 
        imprimir_solucion_grafica(pasos, posicion_vacia)
    else:
        print("  No se encontro solucion para esa posicion.")

    print()
    print("  ══ Fin del programa ══")
    print()


# Punto de entrada
if __name__ == "__main__":
    main()
