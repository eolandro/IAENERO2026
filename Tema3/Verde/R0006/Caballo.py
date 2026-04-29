import os
import time

N = 8

movimientos_x = [2, 1, -1, -2, -2, -1, 1, 2]
movimientos_y = [1, 2, 2, 1, -1, -2, -2, -1]


# ===============================
# LIMPIAR PANTALLA
# ===============================
def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')


# ===============================
# CONVERTIR A NOTACIÓN AJEDREZ
# ===============================
def convertir_posicion(pos):
    pos = pos.upper()
    col = ord(pos[0]) - ord('A')
    fila = int(pos[1]) - 1
    return fila, col


# ===============================
# VALIDAR MOVIMIENTO
# ===============================
def es_valido(x, y, tablero):
    return 0 <= x < N and 0 <= y < N and tablero[x][y] == -1


# ===============================
# HEURÍSTICA (WARNDORFF)
# ===============================
def grado(x, y, tablero):
    count = 0
    for i in range(8):
        nx = x + movimientos_x[i]
        ny = y + movimientos_y[i]
        if es_valido(nx, ny, tablero):
            count += 1
    return count


# ===============================
# IMPRIMIR TABLERO BONITO
# ===============================
def imprimir_tablero(tablero):
    print("   A  B  C  D  E  F  G  H")
    for i in range(N):
        print(f"{i+1} ", end="")
        for j in range(N):
            if tablero[i][j] == -1:
                print(" . ", end="")
            else:
                print(f"{tablero[i][j]:2}", end=" ")
        print()
    print()


# ===============================
# RESOLVER CON ANIMACIÓN
# ===============================
def resolver_caballo(tablero, x, y, mov):
    if mov == N * N:
        return True

    candidatos = []
    for i in range(8):
        nx = x + movimientos_x[i]
        ny = y + movimientos_y[i]
        if es_valido(nx, ny, tablero):
            candidatos.append((grado(nx, ny, tablero), nx, ny))

    candidatos.sort(key=lambda x: x[0])

    for _, nx, ny in candidatos:
        tablero[nx][ny] = mov

        limpiar()
        imprimir_tablero(tablero)
        time.sleep(0.05)  # velocidad de animación

        if resolver_caballo(tablero, nx, ny, mov + 1):
            return True

        tablero[nx][ny] = -1  

    return False


# ===============================
# MAIN
# ===============================
def recorrido_caballo():
    print(" Recorrido del Caballo")
    print("Ingresa posición tipo A1, B2, H8\n")

    while True:
        try:
            print("   A  B  C  D  E  F  G  H")
            print("1")
            print("2")
            print("3")
            print("4")
            print("5")
            print("6")
            print("7")
            print("8")
            entrada = input("Posición inicial: ")
            x, y = convertir_posicion(entrada)

            if 0 <= x < 8 and 0 <= y < 8:
                break
            else:
                print("Fuera de rango")
        except:
            print("Formato inválido (ej: A1)")

    tablero = [[-1 for _ in range(N)] for _ in range(N)]
    tablero[x][y] = 0

    if resolver_caballo(tablero, x, y, 1):
        print("\n Recorrido completo:\n")
        imprimir_tablero(tablero)
    else:
        print("❌ No hay solución")


# Ejecución
recorrido_caballo()