from pathlib import Path
import json
import random


UMBRAL_DESACTIVACION = 0.51
PRUEBAS_POR_CASILLA = 3
INTENTOS_MAXIMOS = 3
# SEMILLA = 42


def leer_tablero(nombre_archivo="tablero.json"):
    ruta_archivo = Path(__file__).resolve().parent / nombre_archivo
    with ruta_archivo.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_tablero(datos, nombre_archivo="tablero.json"):
    ruta_archivo = Path(__file__).resolve().parent / nombre_archivo
    with ruta_archivo.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def imprimir_tablero(tablero):
    print("Tablero:")
    for fila in tablero:
        print(fila)


def obtener_dimensiones(tablero):
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0
    return filas, columnas


def limpiar_bombas(tablero):
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j] == "!":
                tablero[i][j] = "0"


def colocar_bomba_azar(tablero):
    limpiar_bombas(tablero)
    filas, columnas = obtener_dimensiones(tablero)
    fila_bomba = random.randint(0, filas - 1)
    columna_bomba = random.randint(0, columnas - 1)
    tablero[fila_bomba][columna_bomba] = "!"
    return (fila_bomba, columna_bomba)


def buscar_bomba(tablero):
    for i, fila in enumerate(tablero):
        for j, celda in enumerate(fila):
            if celda == "!":
                return (i, j)
    return None


def bayes_positivo(prior, sensibilidad, falso_positivo):
    numerador = sensibilidad * prior
    denominador = numerador + falso_positivo * (1 - prior)
    if denominador == 0:
        return 0.0
    return numerador / denominador


def bayes_negativo(prior, sensibilidad, falso_positivo):
    p_neg_si_bomba = 1 - sensibilidad
    p_neg_si_vacia = 1 - falso_positivo
    numerador = p_neg_si_bomba * prior
    denominador = numerador + p_neg_si_vacia * (1 - prior)
    if denominador == 0:
        return 0.0
    return numerador / denominador


def sensor_boomy(hay_bomba, sensibilidad, falso_positivo):
    r = random.random()
    if hay_bomba:
        return "+" if r < sensibilidad else "-"
    else:
        return "+" if r < falso_positivo else "-"


def revisar_casilla(hay_bomba, prior_inicial, sensibilidad, falso_positivo):
    prior = prior_inicial
    historial = []

    for intento in range(1, PRUEBAS_POR_CASILLA + 1):
        lectura = sensor_boomy(hay_bomba, sensibilidad, falso_positivo)

        if lectura == "+":
            prior = bayes_positivo(prior, sensibilidad, falso_positivo)
        else:
            prior = bayes_negativo(prior, sensibilidad, falso_positivo)

        historial.append((intento, lectura, prior))

        if prior >= UMBRAL_DESACTIVACION:
            return prior, historial, True

    return prior, historial, False

def crear_mapa_visible(tablero, visitadas, posicion_actual):
    filas, columnas = obtener_dimensiones(tablero)
    mapa_visible = [["." for _ in range(columnas)] for _ in range(filas)]

    for i, j in visitadas:
        mapa_visible[i][j] = "x"

    fila_actual, columna_actual = posicion_actual
    mapa_visible[fila_actual][columna_actual] = "B"

    return mapa_visible


def imprimir_mapa_visible(mapa_visible):
    print("Representacion de Boome en el tablero:")
    for fila in mapa_visible:
        print(fila)


def recorrer_tablero(tablero, sensibilidad, falso_positivo):
    filas, columnas = obtener_dimensiones(tablero)
    casillas_restantes = filas * columnas
    intentos_desactivador = 0
    bomba_real = buscar_bomba(tablero)
    visitadas = set()

    if bomba_real is None:
        print("No hay bomba en el tablero")
        return

    for i in range(filas):
        for j in range(columnas):
            if casillas_restantes <= 0:
                print("\nNo hay mas casillas por revisar")
                return

            print("---------------------------------------------------------------------------------------")
            mapa_visible = crear_mapa_visible(tablero, visitadas, (i, j))
            imprimir_mapa_visible(mapa_visible)

            prior = 1 / casillas_restantes
            hay_bomba = tablero[i][j] == "!"

            posterior, historial, decidir_desactivar = revisar_casilla(
                hay_bomba,
                prior,
                sensibilidad,
                falso_positivo
            )

            print(f"\nCasilla ({i}, {j})")
            print(f"Prior inicial: {prior:.4f}")

            for num_prueba, lectura, prob in historial:
                if lectura == "+":
                    print(f"Prueba {num_prueba}: detector positivo -> P(bomba | positivo) = {prob:.6f}")

            visitadas.add((i, j))

            if decidir_desactivar:
                intentos_desactivador += 1
                print(f"Decision: DESACTIVAR ({intentos_desactivador}/{INTENTOS_MAXIMOS})")

                if hay_bomba:
                    print("Resultado: bomba real desactivada")
                    print(f"Bomba encontrada en: ({i}, {j})")
                    return
                else:
                    print("Resultado: falso positivo")

                    if intentos_desactivador >= INTENTOS_MAXIMOS:
                        print("Boomy se quedo sin intentos de desactivacion :(")
                        print(f"****** La bomba real estaba en: {bomba_real} :O ******")
                        return
            else:
                print("Decision: no desactivar, se considera vacia")
                casillas_restantes -= 1

    print("\n****** No se encontro la bomba :( ******")
    print(f"****** La bomba real estaba en: {bomba_real} :O ******")

def main():
    random.seed()
    datos = leer_tablero("tablero.json")
    tablero = datos["tablero"]
    sensibilidad = datos["sensibilidad"]
    falso_positivo = datos["falso_positivo"]

    colocar_bomba_azar(tablero)
    guardar_tablero(datos, "tablero.json")
    recorrer_tablero(tablero, sensibilidad, falso_positivo)
    imprimir_tablero(tablero)


if __name__ == "__main__":
    main()