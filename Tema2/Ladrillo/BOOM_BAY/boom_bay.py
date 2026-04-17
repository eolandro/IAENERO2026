import random
import yaml

# ---------------------------------
# SENSOR PROBABILISTICO
# ---------------------------------
def sensor_ruidoso(real):
    if real == 1:
        return 1 if random.random() < 0.85 else 0
    else:
        return 1 if random.random() < 0.15 else 0

# ---------------------------------
# ACTUALIZACION BAYESIANA
# ---------------------------------
def actualizar_creencia(prior, evidencia):
    p_det_si = 0.85
    p_det_no = 0.15

    if evidencia == 1:
        num = p_det_si * prior
        den = (p_det_si * prior) + (p_det_no * (1 - prior))
    else:
        num = (1 - p_det_si) * prior
        den = ((1 - p_det_si) * prior) + ((1 - p_det_no) * (1 - prior))

    return num / den if den != 0 else 0

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
# FIX: propagar evidencia negativa a vecinos cuando
#      una celda confirmada no tiene objetivo
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
# ---------------------------------
def mostrar_matriz(filas, columnas, actual, visitadas, confirmadas, falsas):
    print()
    for i in range(filas):
        fila_txt = ""
        for j in range(columnas):
            if (i, j) == actual:
                fila_txt += " R "
            elif (i, j) in confirmadas:
                fila_txt += " X "   # objetivo confirmado
            elif (i, j) in falsas:
                fila_txt += " ! "   # falsa alarma
            elif (i, j) in visitadas:
                fila_txt += " . "   # explorada, sin objetivo
            else:
                fila_txt += " - "
        print(fila_txt)
    print()

# ---------------------------------
# ANALISIS DE CELDA
# ---------------------------------
def evaluar_posicion(real, prior, umbral, iteraciones, coord):
    prob = prior
    x, y = coord

    print(f"\nPosicion ({x},{y})")
    print(f"Probabilidad inicial = {prob:.6f}")

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
    print("SISTEMA DE DECISION BAYESIANO")
    print("=" * 50)

    tablero = cargar_mapa("tablero.yaml")

    filas = len(tablero)
    columnas = len(tablero[0])

    total_celdas = filas * columnas
    total_objetivos = sum(sum(f) for f in tablero)

    print(f"Dimensiones: {filas} x {columnas}")
    print(f"Objetivos reales: {total_objetivos}")

    # Probabilidad inicial global
    prior_global = total_objetivos / total_celdas

    creencias = inicializar_creencias(filas, columnas, prior_global)

    visitadas  = set()
    confirmadas = set()   # FIX: rastrear celdas con objetivo confirmado
    falsas      = set()   # FIX: rastrear falsas alarmas
    aciertos   = 0
    errores    = 0
    intervenciones = 0

    # FIX: limite separado por tipo
    # El agente puede explorar todo el tablero pero solo interviene
    # cuando la probabilidad supera el umbral; no hay tope artificial.
    umbral = 0.6
    max_intervenciones = total_celdas  # tope de seguridad, no restrictivo

    print("\nInicio del analisis...\n")

    # FIX: condicion de parada correcta:
    #   - seguir mientras queden celdas sin visitar
    #   - y no se hayan encontrado todos los objetivos
    while len(visitadas) < total_celdas and aciertos < total_objetivos:

        x, y = seleccionar_celda(creencias, visitadas)

        # Guardia: no deberia ocurrir, pero evita crash si el tablero se agota
        if x == -1:
            break

        visitadas.add((x, y))

        mostrar_matriz(filas, columnas, (x, y), visitadas, confirmadas, falsas)

        prior = creencias[x][y]
        real  = tablero[x][y]

        posterior = evaluar_posicion(real, prior, umbral, 3, (x, y))

        creencias[x][y] = posterior

        if posterior >= umbral:
            intervenciones += 1
            print(f"Decision: intervenir (P = {posterior:.6f})")

            if real == 1:
                aciertos += 1
                confirmadas.add((x, y))
                print(f"Resultado: objetivo confirmado en ({x},{y})")
                # FIX: propagar ligera reduccion a vecinos (objetivo encontrado,
                #      reduce probabilidad de que los vecinos inmediatos
                #      tambien sean objetivos si el mapa es disperso)
                actualizar_vecinos(creencias, visitadas, x, y,
                                   filas, columnas, factor=0.8)
            else:
                errores += 1
                falsas.add((x, y))
                print(f"Resultado: falsa alarma en ({x},{y})")
                # FIX: falsa alarma -> reducir creencia en vecinos cercanos
                actualizar_vecinos(creencias, visitadas, x, y,
                                   filas, columnas, factor=0.6)
        else:
            print(f"Decision: no intervenir (P = {posterior:.6f})")
            # FIX: evidencia negativa -> reducir creencia en vecinos
            actualizar_vecinos(creencias, visitadas, x, y,
                               filas, columnas, factor=0.85)

    # ---------------------------------
    # RESUMEN FINAL
    # ---------------------------------
    print("\n" + "=" * 50)
    print("RESULTADOS FINALES")
    print("=" * 50)

    print(f"Objetivos totales    : {total_objetivos}")
    print(f"Aciertos             : {aciertos}")
    print(f"Falsas alarmas       : {errores}")
    print(f"Celdas exploradas    : {len(visitadas)}/{total_celdas}")
    print(f"Total intervenciones : {intervenciones}")

    if aciertos == total_objetivos:
        print("Resultado global: COMPLETO - todos los objetivos encontrados")
    else:
        print(f"Resultado global: INCOMPLETO - objetivos restantes: {total_objetivos - aciertos}")


# ---------------------------------
# MAIN
# ---------------------------------
if __name__ == "__main__":
    simulador()