import random
import yaml

# ---------------------------------
# PARAMETROS DEL SENSOR (MODELO)
# ---------------------------------
P_DET_SI = 0.90   # P(sensor=1 | bomba=1)
P_DET_NO = 0.20   # P(sensor=1 | bomba=0)

# ---------------------------------
# SENSOR RUIDOSO (BINARIO)
# ---------------------------------
def sensor_ruidoso(real):
    if real == 1:
        return 1 if random.random() < P_DET_SI else 0
    else:
        return 1 if random.random() < P_DET_NO else 0

# ---------------------------------
# BAYES CON MULTIPLES EVIDENCIAS
# P(H|E) ∝ P(H) Π P(ei|H)
# ---------------------------------
def actualizar_conjunto(prior, evidencias):

    p1 = prior
    p0 = 1 - prior

    for e in evidencias:
        if e == 1:
            p1 *= P_DET_SI
            p0 *= P_DET_NO
        else:
            p1 *= (1 - P_DET_SI)
            p0 *= (1 - P_DET_NO)

    if (p1 + p0) == 0:
        return 0

    return p1 / (p1 + p0)

# ---------------------------------
# DESACTIVAR BOMBA
# ---------------------------------
def desactivar_bomba(coord, exito_base=0.90):
    x, y = coord
    print(f"\n{'*' * 40}")
    print(f"  INICIANDO DESACTIVACION en ({x},{y})")

    exito = random.random() < exito_base

    if exito:
        print(f"  [OK] Bomba DESACTIVADA")
    else:
        print(f"  [!!] FALLO - bomba sigue activa")

    print(f"{'*' * 40}\n")
    return exito

# ---------------------------------
# CARGAR MAPA
# ---------------------------------
def cargar_mapa(ruta):
    with open(ruta, "r") as f:
        data = yaml.safe_load(f)
    return data["mapa"]

# ---------------------------------
# INICIALIZAR CREENCIAS
# ---------------------------------
def inicializar_creencias(filas, columnas, valor):
    return [[valor for _ in range(columnas)] for _ in range(filas)]

# ---------------------------------
# SELECCIONAR CELDA MAX PROB
# ---------------------------------
def seleccionar_celda(creencias, visitadas):
    mejor = (-1, -1)
    max_valor = -1

    for i in range(len(creencias)):
        for j in range(len(creencias[0])):
            if (i, j) not in visitadas:
                if creencias[i][j] > max_valor:
                    max_valor = creencias[i][j]
                    mejor = (i, j)

    return mejor

# ---------------------------------
# ACTUALIZAR VECINOS
# ---------------------------------
def actualizar_vecinos(creencias, visitadas, x, y, filas, columnas, factor):
    direcciones = [(-1,0),(1,0),(0,-1),(0,1),
                   (-1,-1),(-1,1),(1,-1),(1,1)]

    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < filas and 0 <= ny < columnas and (nx, ny) not in visitadas:
            creencias[nx][ny] = max(0.0, min(1.0, creencias[nx][ny] * factor))

# ---------------------------------
# MOSTRAR TABLERO
# ---------------------------------
def mostrar_matriz(filas, columnas, actual, visitadas, falsas,
                   desactivadas=None, fallidas=None):

    if desactivadas is None:
        desactivadas = set()
    if fallidas is None:
        fallidas = set()

    print("\nTABLERO\n")

    for i in range(filas):
        for j in range(columnas):
            if (i, j) == actual:
                print(" R ", end="")
            elif (i, j) in desactivadas:
                print("[X]", end="")
            elif (i, j) in fallidas:
                print("[B]", end="")
            elif (i, j) in falsas:
                print(" ! ", end="")
            elif (i, j) in visitadas:
                print(" . ", end="")
            else:
                print(" - ", end="")
        print()
    print()

# ---------------------------------
# EVALUAR CELDA (USANDO BAYES CORRECTO)
# ---------------------------------
def evaluar_posicion(real, prior, iteraciones, coord):

    evidencias = []
    x, y = coord

    print(f"\nPosicion ({x},{y})")
    print(f"Prior = {prior:.4f}")

    for _ in range(iteraciones):
        lectura = sensor_ruidoso(real)
        evidencias.append(lectura)

    posterior = actualizar_conjunto(prior, evidencias)

    print(f"Evidencias: {evidencias}")
    print(f"Posterior = {posterior:.4f}")

    return posterior

# ---------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------
def simulador():

    tablero = cargar_mapa("tablero.yaml")

    filas = len(tablero)
    columnas = len(tablero[0])

    total_celdas = filas * columnas
    total_bombas = sum(sum(fila) for fila in tablero)

    prior_global = total_bombas / total_celdas

    creencias = inicializar_creencias(filas, columnas, prior_global)

    visitadas = set()
    falsas = set()
    desactivadas = set()
    fallidas = set()

    aciertos = 0
    errores = 0

    umbral = 0.60

    while len(visitadas) < total_celdas and aciertos < total_bombas:

        x, y = seleccionar_celda(creencias, visitadas)

        if x == -1:
            break

        visitadas.add((x, y))

        mostrar_matriz(filas, columnas, (x, y), visitadas, falsas,
                       desactivadas, fallidas)

        real = tablero[x][y]
        prior = creencias[x][y]

        posterior = evaluar_posicion(real, prior, 3, (x, y))
        creencias[x][y] = posterior

        if posterior >= umbral:
            print("DECISION: INTERVENIR")

            if real == 1:
                aciertos += 1
                print("BOMBA REAL")

                exito = desactivar_bomba((x, y))

                if exito:
                    desactivadas.add((x, y))
                else:
                    fallidas.add((x, y))

                actualizar_vecinos(creencias, visitadas, x, y,
                                   filas, columnas, 0.8)

            else:
                errores += 1
                falsas.add((x, y))
                print("FALSA ALARMA")

                actualizar_vecinos(creencias, visitadas, x, y,
                                   filas, columnas, 0.6)
        else:
            print("DECISION: NO INTERVENIR")

            actualizar_vecinos(creencias, visitadas, x, y,
                               filas, columnas, 0.85)

    print("\nRESULTADOS")
    print(f"Bombas reales: {total_bombas}")
    print(f"Aciertos: {aciertos}")
    print(f"Errores: {errores}")
    print(f"Desactivadas: {len(desactivadas)}")
    print(f"Fallidas: {len(fallidas)}")


# ---------------------------------
# MAIN
# ---------------------------------
if __name__ == "__main__":
    simulador()
