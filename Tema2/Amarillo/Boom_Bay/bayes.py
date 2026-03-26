# Motor matematico de Bayes

import random

# Parametros del sensor
P_DETECCION = 0.9      # P(positivo | bomba)
P_F_POSITIVO = 0.2     # P(positivo | no bomba)


def calcular_posterior(p_previa: float) -> float:
    # Bayes: P(bomba|+) = P(+|bomba) * P(bomba) / P(+)
    p_vacio = 1.0 - p_previa
    p_pos = (P_DETECCION * p_previa) + (P_F_POSITIVO * p_vacio)

    if p_pos == 0: return 0.0
    return round((P_DETECCION * p_previa) / p_pos, 6)


def simular_sensor(hay_bomba: int) -> int:
    # Simula lectura de sensor imperfecto (retorna 1 o 0)
    umbral = P_DETECCION if hay_bomba == 1 else P_F_POSITIVO
    return 1 if random.random() < umbral else 0
