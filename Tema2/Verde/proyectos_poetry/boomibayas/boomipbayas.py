import yaml
import random

# Probabilidad de que el sensor detecte una bomba cuando SI hay bomba
PROB_SENSOR_BOMBA = 0.9

# Probabilidad de que el sensor detecte bomba cuando en realidad NO hay nada
PROB_SENSOR_VACIO = 0.2


# Función para leer el archivo YAML donde viene el mapa
def leer_archivo_mapa(ruta_archivo):
    
    # Abrimos el archivo en modo lectura
    with open(ruta_archivo, "r") as archivo:
        contenido = yaml.safe_load(archivo)

    # Regresamos únicamente la matriz del mapa
    return contenido["mapa"]


# Busca en el mapa la posición real de la bomba
def localizar_bomba(matriz):

    # Recorremos cada fila del mapa
    for fila_indice, fila in enumerate(matriz):

        # Recorremos cada columna
        for columna_indice, valor in enumerate(fila):

            # Si encontramos un 1 significa que ahí está la bomba
            if valor == 1:
                return fila_indice, columna_indice

    # Si no se encontró bomba
    return None, None


# Función que calcula la probabilidad usando Bayes
def calcular_probabilidad(prior, sensor_positivo):

    # Si el sensor detectó algo
    if sensor_positivo:

        # Fórmula de Bayes cuando hay detección
        numerador = PROB_SENSOR_BOMBA * prior

        denominador = (
            (PROB_SENSOR_BOMBA * prior)
            + (PROB_SENSOR_VACIO * (1 - prior))
        )

    else:

        # Probabilidad de NO detectar bomba cuando sí hay
        no_detectar_bomba = 1 - PROB_SENSOR_BOMBA

        # Probabilidad de NO detectar cuando está vacío
        no_detectar_vacio = 1 - PROB_SENSOR_VACIO

        numerador = no_detectar_bomba * prior

        denominador = (
            (no_detectar_bomba * prior)
            + (no_detectar_vacio * (1 - prior))
        )

    # Resultado final de la probabilidad
    return numerador / denominador


# Función principal donde el robot busca la bomba
def iniciar_busqueda(tablero):

    total_filas = len(tablero)
    total_columnas = len(tablero[0])

    # Obtener la ubicación real de la bomba
    bomba_real_fila, bomba_real_col = localizar_bomba(tablero)

    # Número total de casillas
    casillas_restantes = total_filas * total_columnas

    # Probabilidad inicial uniforme
    probabilidad_base = 1 / casillas_restantes

    # Recorrido del mapa en forma serpiente
    for f in range(total_filas):

        # Si la fila es par se recorre normal
        if f % 2 == 0:
            recorrido = range(total_columnas)

        # Si es impar se recorre al revés
        else:
            recorrido = reversed(range(total_columnas))

        for c in recorrido:

            print(f"\nAnalizando casilla ({f}, {c})...")

            # Verificamos si en esa posición está la bomba real
            es_bomba = (f == bomba_real_fila and c == bomba_real_col)

            # Simulación del sensor
            sensor = random.random() < (
                PROB_SENSOR_BOMBA if es_bomba else PROB_SENSOR_VACIO
            )

            # Calculamos la probabilidad con Bayes
            prob_actual = calcular_probabilidad(probabilidad_base, sensor)

            print(f"Probabilidad estimada de bomba: {prob_actual:.4f}")

            # Si el sensor marcó positivo
            if sensor:

                prob_total = prob_actual

                # Hacemos dos revisiones adicionales
                for revision in range(2):

                    verificacion = random.random() < (
                        PROB_SENSOR_BOMBA if es_bomba else PROB_SENSOR_VACIO
                    )

                    print(
                        f"  → Revisión {revision+2}: "
                        f"{'Positivo' if verificacion else 'Negativo'}"
                    )

                    # Actualizamos la probabilidad
                    prob_total = calcular_probabilidad(prob_total, verificacion)

                    print(f"    Probabilidad actualizada: {prob_total:.4f}")

                    # Si supera el 50% se confirma
                    if prob_total >= 0.5:

                        if es_bomba:
                            print(
                                f"\nBoomie confirmó bomba en ({f},{c}) "
                                f"con {prob_total*100:.2f}% de certeza"
                            )
                            return True

                        else:
                            print(
                                f"Alarma falsa: {prob_total*100:.2f}% "
                                f"pero no hay bomba."
                            )
                            break

                # Si la probabilidad no fue suficiente
                if prob_total < 0.5:
                    print(
                        f"Probabilidad final {prob_total*100:.2f}% "
                        f"insuficiente. Boomie sigue buscando."
                    )

                elif es_bomba:
                    print(
                        f"\nBoomie encontró la bomba en ({f},{c}) "
                        f"después de 3 revisiones."
                    )
                    return True

            # Reducimos el número de casillas restantes
            casillas_restantes -= 1

            print(f"Casillas restantes: {casillas_restantes}")

            # Actualizamos probabilidad base
            probabilidad_base = 1 / casillas_restantes if casillas_restantes > 0 else 0

    # Si terminó todo el mapa sin encontrarla
    print("\nBoomie explotó... no logró encontrar la bomba.")

    return False


# Programa principal
if __name__ == "__main__":

    # Cargar el mapa desde el archivo YAML
    mapa_juego = leer_archivo_mapa("mapa.yaml")

    # Iniciar la búsqueda
    iniciar_busqueda(mapa_juego)
