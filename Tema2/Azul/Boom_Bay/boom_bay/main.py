"""
Boom_Bay: Toma de decisiones con Bayes.
Simulador de búsqueda bayesiana para localizar una bomba en un tablero.
"""

import random
from pathlib import Path
from ruamel.yaml import YAML


# --- Constantes del sensor ---
P_POSITIVO_DADO_BOMBA = 0.9    # De 10 bombas, 9 detecta correctamente
P_POSITIVO_DADO_VACIO = 0.2    # De 10 vacíos, 2 detecta erróneamente como bomba
MAX_LECTURAS = 3               # Lecturas del sensor por casilla
UMBRAL_BOMBA = 0.5             # Si prob > 50%, se activa el desactivador
MAX_DESACTIVACIONES = 3        # Intentos máximos del desactivador


def cargar_tablero(ruta: str) -> dict:
    """Lee el tablero desde un archivo YAML usando ruamel.yaml."""
    yaml = YAML()
    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.load(f)
    print(f"Tablero cargado desde '{ruta}':")
    for fila_nombre in datos:
        print(f"  {fila_nombre}: {datos[fila_nombre]}")
    print()
    return datos


def simular_sensor(valor_real: int) -> int:
    """
    Simula el sensor imperfecto del robot.
    - Si hay bomba (1): 90% de detectarla (retorna 1), 10% falso negativo (retorna 0).
    - Si está vacío (0): 80% correcto (retorna 0), 20% falso positivo (retorna 1).
    """
    if valor_real == 1:
        return 1 if random.random() < P_POSITIVO_DADO_BOMBA else 0
    else:
        return 1 if random.random() < P_POSITIVO_DADO_VACIO else 0


def calcular_bayes(prob_bomba: float) -> float:
    """
    Aplica la Regla de Bayes para actualizar la probabilidad de bomba
    dado que el detector dio positivo.

    P(bomba|+) = P(+|bomba) * P(bomba) / P(+)
    donde P(+) = P(+|bomba)*P(bomba) + P(+|vacío)*P(no_bomba)
    """
    prob_no_bomba = 1.0 - prob_bomba
    # Probabilidad total de detector positivo
    p_positivo = (P_POSITIVO_DADO_BOMBA * prob_bomba) + (P_POSITIVO_DADO_VACIO * prob_no_bomba)
    # Probabilidad posterior (Bayes)
    prob_posterior = (P_POSITIVO_DADO_BOMBA * prob_bomba) / p_positivo
    return prob_posterior


def buscar_bomba(tablero: dict) -> None:
    """
    Recorre el tablero en zigzag y busca la bomba usando inferencia bayesiana.
    En cada celda realiza hasta 3 lecturas. Si el sensor da positivo,
    calcula Bayes y actualiza la creencia. Si la prob supera el umbral,
    activa el desactivador.
    """
    filas = list(tablero.keys())
    total_casillas = sum(len(tablero[f]) for f in filas)
    desactivaciones = MAX_DESACTIVACIONES
    casillas_revisadas = 0
    bomba_encontrada = False

    print(f"Iniciando búsqueda en tablero de {total_casillas} casillas...")
    print(f"Desactivaciones disponibles: {desactivaciones}")
    print(f"Umbral de decisión: {UMBRAL_BOMBA * 100}%")
    print("=" * 60)

    for i, fila_nombre in enumerate(filas):
        fila = tablero[fila_nombre]
        # Zigzag: filas pares izq→der, impares der→izq
        columnas = range(len(fila)) if i % 2 == 0 else range(len(fila) - 1, -1, -1)

        for col in columnas:
            valor_real = fila[col]
            casillas_revisadas += 1
            casillas_restantes = total_casillas - casillas_revisadas
            # Probabilidad priori: 1 bomba entre las casillas restantes + actual
            prob_bomba = 1.0 / (casillas_restantes + 1)

            print(f"\n--- Casilla {fila_nombre}{col + 1} (revisada #{casillas_revisadas}) ---")

            # Realizar hasta MAX_LECTURAS
            positivos = 0
            for lectura in range(1, MAX_LECTURAS + 1):
                resultado = simular_sensor(valor_real)
                if resultado == 1:
                    positivos += 1
                    prob_bomba = calcular_bayes(prob_bomba)
                    print(f"  Lectura {lectura}: POSITIVO  -> P(bomba|+) = {prob_bomba:.4f} ({prob_bomba * 100:.2f}%)")
                else:
                    print(f"  Lectura {lectura}: negativo")

            # Decisión
            if positivos > 0 and prob_bomba > UMBRAL_BOMBA:
                if desactivaciones > 0:
                    desactivaciones -= 1
                    if valor_real == 1:
                        print(f"  *** DESACTIVADOR USADO en {fila_nombre}{col + 1}: ¡BOMBA DESACTIVADA! ***")
                        bomba_encontrada = True
                    else:
                        print(f"  *** DESACTIVADOR USADO en {fila_nombre}{col + 1}: Falso positivo (no había bomba) ***")
                    print(f"  Desactivaciones restantes: {desactivaciones}")
                else:
                    print(f"  Probabilidad alta ({prob_bomba * 100:.2f}%) pero sin desactivaciones disponibles.")
            else:
                print(f"  Casilla segura (prob: {prob_bomba * 100:.2f}%). Avanzando.")

            if bomba_encontrada:
                break
        if bomba_encontrada:
            break

    # Resultado final
    print("\n" + "=" * 60)
    if bomba_encontrada:
        print("MISIÓN EXITOSA: La bomba fue localizada y desactivada.")
    elif desactivaciones == 0:
        print("MISIÓN FALLIDA: Se agotaron los desactivadores sin encontrar la bomba.")
    else:
        print("BÚSQUEDA COMPLETA: No se detectó la bomba con suficiente certeza.")
    print(f"Casillas revisadas: {casillas_revisadas}/{total_casillas}")
    print(f"Desactivaciones usadas: {MAX_DESACTIVACIONES - desactivaciones}/{MAX_DESACTIVACIONES}")


def main():
    """Punto de entrada principal del programa."""
    print("=" * 60)
    print("  BOOM_BAY: Toma de decisiones con Bayes")
    print("  Búsqueda bayesiana de bombas en tablero")
    print("=" * 60)
    print()

    # Cargar tablero
    ruta_yaml = Path(__file__).parent.parent / "tablero.yaml"
    tablero = cargar_tablero(str(ruta_yaml))

    # Ejecutar búsqueda
    buscar_bomba(tablero)


if __name__ == "__main__":
    main()
