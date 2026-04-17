import random
import secrets
import numpy as np
from ruamel.yaml import YAML

yaml = YAML()

FILAS = ["A", "B", "C", "D", "E"]
COLUMNAS = list(range(1, 11))

# Si realmente hay bomba: 90% de marcar 1
LECTURAS_BOMBA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
# Si realmente NO hay bomba: 20% de marcar 1
LECTURAS_VACIO = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]


def cargar_mapa(archivo="mapa.yaml"):
    with open(archivo, "r", encoding="utf-8") as f:
        mapa = yaml.load(f)

    mapa_limpio = {}
    for casilla, valor in mapa.items():
        mapa_limpio[casilla] = int(valor)

    print("Mapa cargado correctamente desde 'mapa.yaml'")
    return mapa_limpio


def elegir_generador():
    print("\nSelecciona el generador de números aleatorios:")
    print("0 -> random (por defecto)")
    print("1 -> numpy")
    print("2 -> secrets")

    try:
        opcion = int(input("Escribe una opción: ").strip())
    except ValueError:
        opcion = 0

    match opcion:
        case 1:
            return lambda lista: int(np.random.choice(lista)), "numpy"
        case 2:
            return secrets.choice, "secrets"
        case _:
            return random.choice, "random"


def generar_recorrido():
    recorrido = []

    for i, fila in enumerate(FILAS):
        if i % 2 == 0:
            for col in COLUMNAS:
                recorrido.append(f"{fila}{col}")
        else:
            for col in reversed(COLUMNAS):
                recorrido.append(f"{fila}{col}")

    return recorrido


def mostrar_tablero(exploradas, posicion_robot=None, bombas_marcadas=None):
    if bombas_marcadas is None:
        bombas_marcadas = set()

    print()
    print("   " + " ".join(str(c) for c in COLUMNAS))

    for fila in FILAS:
        fila_str = ""
        for col in COLUMNAS:
            casilla = f"{fila}{col}"

            if casilla == posicion_robot:
                fila_str += "R "
            elif casilla in bombas_marcadas:
                fila_str += "B "
            elif casilla in exploradas:
                fila_str += ". "
            else:
                fila_str += "X "
        print(f"{fila}  {fila_str}")
    print()


def actualizar_bayes(prior_bomba, lectura):
    prob_lectura_si_bomba = 0.9 if lectura == 1 else 0.1
    prob_lectura_si_no_bomba = 0.2 if lectura == 1 else 0.8

    numerador = prob_lectura_si_bomba * prior_bomba
    denominador = numerador + (prob_lectura_si_no_bomba * (1 - prior_bomba))

    if denominador == 0:
        return prior_bomba

    return numerador / denominador


def evaluar_casillas(mapa, generador):
    recorrido = generar_recorrido()
    total_casillas = len(recorrido)
    total_bombas = sum(mapa.values())
    prior_base = total_bombas / total_casillas

    exploradas = set()
    probabilidades_finales = {}

    for casilla in recorrido:
        mostrar_tablero(exploradas, posicion_robot=casilla)

        print(f"Revisando casilla {casilla}")
        print(f"Probabilidad inicial de bomba en {casilla}: {prior_base:.6f}")

        valor_real = mapa[casilla]
        prob_bomba = prior_base

        for intento in range(1, 4):
            if valor_real == 1:
                lectura = generador(LECTURAS_BOMBA)
            else:
                lectura = generador(LECTURAS_VACIO)

            prob_bomba = actualizar_bayes(prob_bomba, lectura)

            print(
                f"  Lectura {intento}: sensor = {lectura} "
                f"-> P(bomba | evidencia) = {prob_bomba:.6f}"
            )

        probabilidades_finales[casilla] = prob_bomba
        exploradas.add(casilla)

        print(f"Probabilidad final en {casilla}: {prob_bomba:.6f}")
        print("-" * 50)

    return probabilidades_finales, total_bombas


def seleccionar_bombas(probabilidades, total_bombas):
    ordenadas = sorted(
        probabilidades.items(),
        key=lambda elemento: elemento[1],
        reverse=True
    )
    return {casilla for casilla, _ in ordenadas[:total_bombas]}


def main():
    mapa = cargar_mapa("mapa.yaml")
    generador, nombre_generador = elegir_generador()

    print(f"\nGenerador seleccionado: {nombre_generador}")
    print("Iniciando búsqueda...\n")

    probabilidades, total_bombas = evaluar_casillas(mapa, generador)
    bombas_detectadas = seleccionar_bombas(probabilidades, total_bombas)

    bombas_reales = {casilla for casilla, valor in mapa.items() if valor == 1}
    correctas = bombas_detectadas & bombas_reales
    falsas_alarmas = bombas_detectadas - bombas_reales
    faltantes = bombas_reales - bombas_detectadas

    print("\nMapa final:")
    mostrar_tablero(set(generar_recorrido()), bombas_marcadas=bombas_detectadas)

    print("=" * 50)
    print("Probabilidades finales más altas:")
    ranking = sorted(probabilidades.items(), key=lambda x: x[1], reverse=True)
    for casilla, prob in ranking[:10]:
        print(f"  {casilla}: {prob:.6f}")

    print("\nBombas detectadas:")
    for casilla in sorted(bombas_detectadas):
        print(f"  {casilla}")

    if correctas:
        print("\nBombas encontradas correctamente:")
        for casilla in sorted(correctas):
            print(f"  {casilla}")

    if falsas_alarmas:
        print("\nFalsas alarmas:")
        for casilla in sorted(falsas_alarmas):
            print(f"  {casilla}")

    if faltantes:
        print("\nBombas reales no detectadas:")
        for casilla in sorted(faltantes):
            print(f"  {casilla}")

    print("=" * 50)


if __name__ == "__main__":
    main()