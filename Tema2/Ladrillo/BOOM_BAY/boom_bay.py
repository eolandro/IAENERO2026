import random
import yaml

# ---------------------------------
# SENSOR PROBABILISTICO
# 90% de deteccion si hay bomba
# 20% de falso positivo si NO hay bomba
# ---------------------------------
def sensor_ruidoso(real):
    if real == 1:
        return 1 if random.random() < 0.90 else 0   # 90% detecta correctamente
    else:
        return 1 if random.random() < 0.20 else 0   # 20% falso positivo

# ---------------------------------
# ACTUALIZACION BAYESIANA
# Consistente con las probabilidades del sensor
# ---------------------------------
def actualizar_creencia(prior, evidencia):
    p_det_si = 0.90   # P(sensor=1 | bomba presente)
    p_det_no = 0.20   # P(sensor=1 | bomba ausente)

    if evidencia == 1:
        num = p_det_si * prior
        den = (p_det_si * prior) + (p_det_no * (1 - prior))
    else:
        num = (1 - p_det_si) * prior
        den = ((1 - p_det_si) * prior) + ((1 - p_det_no) * (1 - prior))

    return num / den if den != 0 else 0

# ---------------------------------
# DESACTIVADOR DE BOMBA
# Simula el proceso de desactivacion con resultado aleatorio
# segun la habilidad del equipo (exito_base entre 0 y 1)
# ---------------------------------
def desactivar_bomba(coord, exito_base=0.90):
    """
    Intenta desactivar la bomba en la celda indicada.

    Parametros
    ----------
    coord       : tupla (fila, columna) de la celda con la bomba
    exito_base  : probabilidad base de desactivacion exitosa (default 0.90)

    Retorna
    -------
    True  -> bomba desactivada con exito
    False -> fallo en la desactivacion (bomba sigue activa)
    """
    x, y = coord
    print(f"\n{'*' * 40}")
    print(f"  INICIANDO DESACTIVACION en ({x},{y})")
    print(f"  Probabilidad de exito: {exito_base * 100:.0f}%")

    exito = random.random() < exito_base

    if exito:
        print(f"  [OK] Bomba DESACTIVADA correctamente en ({x},{y})")
    else:
        print(f"  [!!] FALLO en la desactivacion en ({x},{y}) - bomba sigue activa")

    print(f"{'*' * 40}\n")
    return exito

# ---------------------------------
# CARGAR YAML
# ---------------------------------
def cargar_mapa(ruta):
    with open(ruta, "r") as f:
        data = yaml.safe_load(f)
    return data["mapa"]

# ---------------------------------
# CREAR MATRIZ DE PROBABILIDADES
# ---------------------------------
def inicializar_creencias(filas, columnas, valor):
    return [[valor for _ in range(columnas)] for _ in range(filas)]

# ---------------------------------
# SELECCION DE CELDA (MAX PROB)
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
# ACTUALIZAR CELDAS VECINAS
# ---------------------------------
def actualizar_vecinos(creencias, visitadas, x, y, filas, columnas, factor):
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < filas and 0 <= ny < columnas and (nx, ny) not in visitadas:
            creencias[nx][ny] = max(0.0, min(1.0, creencias[nx][ny] * factor))

# ---------------------------------
# MOSTRAR TABLERO
# Leyenda:
#   [R] -> posicion actual del agente (robot/boomber)
#   [X] -> bomba confirmada y desactivada
#   [B] -> bomba confirmada, desactivacion fallida
#   [!] -> falsa alarma intervenida
#   [.] -> celda explorada sin objetivo
#   [-] -> celda sin explorar
# ---------------------------------
def mostrar_matriz(filas, columnas, actual, visitadas, confirmadas, falsas,
                   desactivadas=None, fallidas=None):
    if desactivadas is None:
        desactivadas = set()
    if fallidas is None:
        fallidas = set()

    ancho_col = 4
    separador = "+" + ("-" * ancho_col + "+") * columnas

    print()
    print("  ", end="")
    for j in range(columnas):
        print(f"  {j:2}", end="")
    print()
    print("  " + separador)

    for i in range(filas):
        print(f"{i:2}|", end="")
        for j in range(columnas):
            if (i, j) == actual:
                simbolo = " R  "        # agente en esta posicion
            elif (i, j) in desactivadas:
                simbolo = "[X] "        # bomba desactivada con exito
            elif (i, j) in fallidas:
                simbolo = "[B] "        # bomba detectada, desactivacion fallida
            elif (i, j) in falsas:
                simbolo = " !  "        # falsa alarma
            elif (i, j) in visitadas:
                simbolo = " .  "        # explorada sin objetivo
            else:
                simbolo = " -  "        # sin explorar
            print(f"{simbolo}|", end="")
        print()
        print("  " + separador)

    print()
    print("  LEYENDA:  R=agente  [X]=bomba desactivada  [B]=bomba activa  "
          "!=falsa alarma  .=explorada  -=sin explorar")
    print()

# ---------------------------------
# ANALISIS DE CELDA
# ---------------------------------
def evaluar_posicion(real, prior, umbral, iteraciones, coord):
    prob = prior
    x, y = coord

    print(f"\nPosicion ({x},{y})")
    print(f"  Probabilidad inicial = {prob:.6f}")

    for k in range(iteraciones):
        lectura = sensor_ruidoso(real)
        prob = actualizar_creencia(prob, lectura)

        if lectura == 1:
            print(f"  Lectura positiva -> Probabilidad actual = {prob:.6f}")
        else:
            print(f"  Lectura negativa -> Probabilidad actual = {prob:.6f}")

        if prob >= umbral:
            break

    return prob

# ---------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------
def simulador():

    print("=" * 50)
    print("  SISTEMA DE DECISION BAYESIANO - BOOM BAY")
    print("=" * 50)

    tablero = cargar_mapa("tablero.yaml")

    filas    = len(tablero)
    columnas = len(tablero[0])

    total_celdas    = filas * columnas
    total_objetivos = sum(sum(f) for f in tablero)

    print(f"\nDimensiones : {filas} x {columnas}")
    print(f"Bombas reales: {total_objetivos}")

    prior_global = total_objetivos / total_celdas
    creencias    = inicializar_creencias(filas, columnas, prior_global)

    visitadas   = set()
    confirmadas = set()   # celdas con bomba confirmada (intervenidas)
    falsas      = set()   # falsas alarmas
    desactivadas = set()  # bombas desactivadas con exito
    fallidas     = set()  # bombas donde fallo la desactivacion

    aciertos       = 0
    errores        = 0
    intervenciones = 0

    umbral = 0.60

    print("\nInicio del analisis...\n")

    while len(visitadas) < total_celdas and aciertos < total_objetivos:

        x, y = seleccionar_celda(creencias, visitadas)

        if x == -1:
            break

        visitadas.add((x, y))

        mostrar_matriz(filas, columnas, (x, y), visitadas, confirmadas, falsas,
                       desactivadas, fallidas)

        prior = creencias[x][y]
        real  = tablero[x][y]

        posterior = evaluar_posicion(real, prior, umbral, 3, (x, y))
        creencias[x][y] = posterior

        if posterior >= umbral:
            intervenciones += 1
            print(f"  Decision: INTERVENIR (P = {posterior:.6f})")

            if real == 1:
                aciertos += 1
                confirmadas.add((x, y))
                print(f"  Resultado: bomba detectada en ({x},{y})")

                # Intentar desactivar la bomba
                exito = desactivar_bomba((x, y))
                if exito:
                    desactivadas.add((x, y))
                else:
                    fallidas.add((x, y))

                actualizar_vecinos(creencias, visitadas, x, y,
                                   filas, columnas, factor=0.8)
            else:
                errores += 1
                falsas.add((x, y))
                print(f"  Resultado: falsa alarma en ({x},{y})")
                actualizar_vecinos(creencias, visitadas, x, y,
                                   filas, columnas, factor=0.6)
        else:
            print(f"  Decision: no intervenir (P = {posterior:.6f})")
            actualizar_vecinos(creencias, visitadas, x, y,
                               filas, columnas, factor=0.85)

    # ---------------------------------
    # ESTADO FINAL DEL TABLERO
    # ---------------------------------
    mostrar_matriz(filas, columnas, (-1, -1), visitadas, confirmadas, falsas,
                   desactivadas, fallidas)

    # ---------------------------------
    # RESUMEN FINAL
    # ---------------------------------
    print("\n" + "=" * 50)
    print("  RESULTADOS FINALES")
    print("=" * 50)
    print(f"  Bombas totales       : {total_objetivos}")
    print(f"  Bombas detectadas    : {aciertos}")
    print(f"  Bombas desactivadas  : {len(desactivadas)}")
    print(f"  Desactivaciones fail : {len(fallidas)}")
    print(f"  Falsas alarmas       : {errores}")
    print(f"  Celdas exploradas    : {len(visitadas)}/{total_celdas}")
    print(f"  Total intervenciones : {intervenciones}")

    if aciertos == total_objetivos:
        print("\n  Resultado: COMPLETO - todas las bombas encontradas")
    else:
        print(f"\n  Resultado: INCOMPLETO - bombas sin encontrar: {total_objetivos - aciertos}")

    if len(desactivadas) == total_objetivos:
        print("  Estado final: ZONA SEGURA - todas las bombas desactivadas")
    elif len(fallidas) > 0:
        print(f"  Estado final: PELIGRO - {len(fallidas)} bomba(s) siguen activas")


# ---------------------------------
# MAIN
# ---------------------------------
if __name__ == "__main__":
    simulador()
