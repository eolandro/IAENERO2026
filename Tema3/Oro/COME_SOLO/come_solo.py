import time

class Color:
    VERDE = '\033[92m'
    ROJO = '\033[91m'
    AMARILLO = '\033[93m'
    BLANCO = '\033[97m'
    GRIS = '\033[90m'
    RESET = '\033[0m'

POSICIONES = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
CHAR_A_INDICE = {c: i for i, c in enumerate(POSICIONES)}
INDICE_A_CHAR = {i: c for i, c in enumerate(POSICIONES)}

def indice_de_coordenada(fila, columna):
    return (fila * (fila + 1)) // 2 + columna

def generar_movimientos_validos():
    movimientos = []
    for fila in range(5):
        for columna in range(fila + 1):
            origen = indice_de_coordenada(fila, columna)
            direcciones = [
                (0, 1, 0, 2),
                (0, -1, 0, -2),
                (-1, 0, -2, 0),
                (-1, -1, -2, -2),
                (1, 0, 2, 0),
                (1, 1, 2, 2),
                (1, -1, 2, -2),
                (-1, 1, -2, 2),
            ]
            for df_i, dc_i, df_d, dc_d in direcciones:
                f_i = fila + df_i
                c_i = columna + dc_i
                f_d = fila + df_d
                c_d = columna + dc_d
                if (0 <= f_i < 5 and 0 <= c_i <= f_i and
                    0 <= f_d < 5 and 0 <= c_d <= f_d):
                    intermedio = indice_de_coordenada(f_i, c_i)
                    destino = indice_de_coordenada(f_d, c_d)
                    movimientos.append((origen, intermedio, destino))
    return movimientos

MOVIMIENTOS = generar_movimientos_validos()

def imprimir_tablero_con_resaltado(tablero_actual, tablero_anterior=None,
                                   origen=None, destino=None, comido=None):
    FICHA = 'O'
    VACIO = '.'
    simbolos = []
    for i in range(15):
        if tablero_actual[i] == 1:
            if i == destino:
                simbolos.append(f"{Color.AMARILLO}{FICHA}{Color.RESET}")
            else:
                simbolos.append(f"{Color.BLANCO}{FICHA}{Color.RESET}")
        else:
            if tablero_anterior is not None:
                if i == origen and tablero_anterior[i] == 1:
                    simbolos.append(f"{Color.VERDE}{VACIO}{Color.RESET}")
                elif i == comido and tablero_anterior[i] == 1:
                    simbolos.append(f"{Color.ROJO}{VACIO}{Color.RESET}")
                else:
                    simbolos.append(f"{Color.GRIS}{VACIO}{Color.RESET}")
            else:
                simbolos.append(f"{Color.GRIS}{VACIO}{Color.RESET}")

    print(f"      {simbolos[0]}")
    print(f"     {simbolos[1]} {simbolos[2]}")
    print(f"    {simbolos[3]} {simbolos[4]} {simbolos[5]}")
    print(f"   {simbolos[6]} {simbolos[7]} {simbolos[8]} {simbolos[9]}")
    print(f"  {simbolos[10]} {simbolos[11]} {simbolos[12]} {simbolos[13]} {simbolos[14]}")

def imprimir_tablero_simple(tablero):
    FICHA = 'O'
    VACIO = '.'
    simbolos = []
    for i in range(15):
        if tablero[i] == 1:
            simbolos.append(f"{Color.BLANCO}{FICHA}{Color.RESET}")
        else:
            simbolos.append(f"{Color.GRIS}{VACIO}{Color.RESET}")

    print(f"      {simbolos[0]}")
    print(f"     {simbolos[1]} {simbolos[2]}")
    print(f"    {simbolos[3]} {simbolos[4]} {simbolos[5]}")
    print(f"   {simbolos[6]} {simbolos[7]} {simbolos[8]} {simbolos[9]}")
    print(f"  {simbolos[10]} {simbolos[11]} {simbolos[12]} {simbolos[13]} {simbolos[14]}")

def mostrar_leyenda_colores():
    print("\nLEYENDA DE COLORES:")
    print(f"  {Color.VERDE}.{Color.RESET} = Origen del salto")
    print(f"  {Color.ROJO}.{Color.RESET} = Ficha comida")
    print(f"  {Color.AMARILLO}O{Color.RESET} = Destino del salto")
    print(f"  {Color.BLANCO}O{Color.RESET} = Ficha normal")
    print(f"  {Color.GRIS}.{Color.RESET} = Espacio vacio")

def tablero_inicial(vacia):
    tablero = [1] * 15
    tablero[CHAR_A_INDICE[vacia.upper()]] = 0
    return tablero

def contar_fichas(tablero):
    return sum(tablero)

def es_movimiento_valido(tablero, origen, intermedio, destino):
    return (tablero[origen] == 1 and
            tablero[intermedio] == 1 and
            tablero[destino] == 0)

def ejecutar_salto(tablero, origen, intermedio, destino):
    tablero[origen] = 0
    tablero[intermedio] = 0
    tablero[destino] = 1

def deshacer_salto(tablero, origen, intermedio, destino):
    tablero[origen] = 1
    tablero[intermedio] = 1
    tablero[destino] = 0

def resolver(tablero, secuencia_actual=None):
    if secuencia_actual is None:
        secuencia_actual = []

    if contar_fichas(tablero) == 1:
        return secuencia_actual

    for origen, intermedio, destino in MOVIMIENTOS:
        if es_movimiento_valido(tablero, origen, intermedio, destino):
            ejecutar_salto(tablero, origen, intermedio, destino)
            secuencia_actual.append((origen, intermedio, destino))

            resultado = resolver(tablero, secuencia_actual)
            if resultado is not None:
                return resultado

            secuencia_actual.pop()
            deshacer_salto(tablero, origen, intermedio, destino)

    return None

def main():
    print("=" * 50)
    print("COME SOLO".center(50))
    print("=" * 50)
    print("\nPosiciones disponibles:")
    print("       1")
    print("      2 3")
    print("     4 5 6")
    print("    7 8 9 A")
    print("   B C D E F")

    mostrar_leyenda_colores()

    vacia = input("\nQue posicion comienza vacia? (ej: 1, A, F): ").strip().upper()
    while vacia not in CHAR_A_INDICE:
        print("Posicion invalida. Use un caracter de la lista.")
        vacia = input("Posicion vacia: ").strip().upper()

    tablero = tablero_inicial(vacia)

    print("\n--- ESTADO INICIAL ---")
    imprimir_tablero_simple(tablero)
    print(f"   Fichas: {contar_fichas(tablero)} | Vacio inicial: {vacia}")

    print("\nBuscando solucion...")
    tiempo_inicio = time.time()
    solucion = resolver(tablero)
    tiempo_fin = time.time()

    if solucion is None:
        print("\n[X] No se encontro solucion desde esa posicion inicial.")
    else:
        print("\n[OK] SOLUCION ENCONTRADA!")
        print(f"Tiempo: {tiempo_fin - tiempo_inicio:.3f} segundos")
        print(f"Total de movimientos: {len(solucion)}")
        print("\n" + "=" * 50)
        print("           SECUENCIA DE MOVIMIENTOS")
        print("=" * 50)

        tablero = tablero_inicial(vacia)
        print("\n--- ESTADO INICIAL ---")
        imprimir_tablero_simple(tablero)

        for i, (origen, intermedio, destino) in enumerate(solucion, 1):
            tablero_anterior = tablero.copy()
            ejecutar_salto(tablero, origen, intermedio, destino)
            print(f"\nMovimiento {i}: {INDICE_A_CHAR[origen]} -> {INDICE_A_CHAR[destino]} (come {INDICE_A_CHAR[intermedio]})")
            imprimir_tablero_con_resaltado(tablero, tablero_anterior, origen, destino, intermedio)

        print("\n" + "=" * 50)
        print("               RESUMEN FINAL")
        print("=" * 50)

        ficha_final = next(INDICE_A_CHAR[i] for i in range(15) if tablero[i] == 1)
        print(f"Ficha final en posicion: {ficha_final}")
        print(f"Movimientos realizados: {len(solucion)}")

if __name__ == "__main__":
    main()
