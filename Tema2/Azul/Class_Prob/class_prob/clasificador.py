"""
Clasificador
Lee mensajes nuevos y la tabla de probabilidades.
Aplica método de consenso (media, mediana, moda, umbral, ratio)
con votación por democracia para clasificar cada mensaje.
"""

import os
from statistics import mean, median
from collections import Counter
from ruamel.yaml import YAML


yaml = YAML()
yaml.preserve_quotes = True

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MENSAJES_NUEVOS = os.path.join(DATA_DIR, "mensajes_nuevos.yml")
TABLA_PROB = os.path.join(DATA_DIR, "tabla_probabilidades.yml")
SALIDA = os.path.join(DATA_DIR, "mensajes_clasificados.yml")


# Reusar funciones de tokenización del detokenizador
from class_prob.detokenizador import tokenizar, filtrar_stopwords


def cargar_mensajes(ruta):
    """Carga mensajes nuevos desde YAML."""
    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.load(f)
    return datos["mensajes"]


def cargar_tabla(ruta):
    """Carga la tabla de probabilidades desde YAML."""
    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.load(f)
    return datos["probabilidades"], datos["metadata"]


def obtener_probabilidades_mensaje(tokens, tabla):
    """
    Obtiene las probabilidades P(token|spam) y P(token|no_spam)
    para cada token del mensaje.
    """
    probs_spam = []
    probs_no_spam = []

    for token in tokens:
        if token in tabla:
            probs_spam.append(tabla[token]["p_spam"])
            probs_no_spam.append(tabla[token]["p_no_spam"])

    return probs_spam, probs_no_spam


def metodo_media(probs_spam, probs_no_spam):
    """Voto por media: promedio de probabilidades spam > promedio no_spam."""
    if not probs_spam:
        return "no_spam"
    avg_spam = mean(probs_spam)
    avg_no_spam = mean(probs_no_spam)
    return "spam" if avg_spam > avg_no_spam else "no_spam"


def metodo_mediana(probs_spam, probs_no_spam):
    """Voto por mediana: mediana de probabilidades spam > mediana no_spam."""
    if not probs_spam:
        return "no_spam"
    med_spam = median(probs_spam)
    med_no_spam = median(probs_no_spam)
    return "spam" if med_spam > med_no_spam else "no_spam"


def metodo_moda(tokens, tabla):
    """
    Voto por moda: cuenta cuántos tokens tienen mayor probabilidad
    de ser spam vs no_spam. La clase con más tokens gana.
    """
    votos = []
    for token in tokens:
        if token in tabla:
            if tabla[token]["p_spam"] > tabla[token]["p_no_spam"]:
                votos.append("spam")
            else:
                votos.append("no_spam")

    if not votos:
        return "no_spam"
    conteo = Counter(votos)
    return conteo.most_common(1)[0][0]


def metodo_umbral(probs_spam, probs_no_spam):
    """Voto por umbral directo: suma de P(spam) > suma de P(no_spam)."""
    if not probs_spam:
        return "no_spam"
    return "spam" if sum(probs_spam) > sum(probs_no_spam) else "no_spam"


def metodo_ratio(probs_spam, probs_no_spam):
    """Voto por ratio: producto de ratios P(spam)/P(no_spam) > 1."""
    if not probs_spam:
        return "no_spam"
    ratio = 1.0
    for ps, pn in zip(probs_spam, probs_no_spam):
        if pn > 0:
            ratio *= (ps / pn)
    return "spam" if ratio > 1.0 else "no_spam"


def consenso_democracia(tokens, probs_spam, probs_no_spam, tabla):
    """
    Aplica los 5 métodos de consenso y decide por democracia
    (mayoría simple de votos).
    """
    votos = {
        "media": metodo_media(probs_spam, probs_no_spam),
        "mediana": metodo_mediana(probs_spam, probs_no_spam),
        "moda": metodo_moda(tokens, tabla),
        "umbral": metodo_umbral(probs_spam, probs_no_spam),
        "ratio": metodo_ratio(probs_spam, probs_no_spam),
    }

    # Democracia: mayoría simple
    conteo = Counter(votos.values())
    etiqueta_final = conteo.most_common(1)[0][0]

    return etiqueta_final, votos


def clasificar_mensajes(mensajes, tabla):
    """Clasifica todos los mensajes nuevos usando el método de consenso."""
    clasificados = []

    for msg in mensajes:
        tokens = filtrar_stopwords(tokenizar(msg["texto"]))
        probs_spam, probs_no_spam = obtener_probabilidades_mensaje(tokens, tabla)
        etiqueta, votos = consenso_democracia(tokens, probs_spam, probs_no_spam, tabla)

        clasificados.append({
            "id": msg["id"],
            "texto": msg["texto"],
            "etiqueta": etiqueta,
            "votos": {k: v for k, v in votos.items()},
        })

    return clasificados


def guardar_clasificados(clasificados, ruta):
    """Guarda los mensajes clasificados en YAML."""
    datos = {"mensajes_clasificados": clasificados}
    with open(ruta, "w", encoding="utf-8") as f:
        yaml.dump(datos, f)
    print(f"Archivo generado: {ruta}")


def ejecutar():
    """Ejecuta la etapa de clasificación completa."""
    print("\n" + "=" * 60)
    print("  CLASIFICADOR - Método de Consenso")
    print("=" * 60)

    mensajes = cargar_mensajes(MENSAJES_NUEVOS)
    tabla, metadata = cargar_tabla(TABLA_PROB)

    clasificados = clasificar_mensajes(mensajes, tabla)

    print(f"\nResultados de clasificación:")
    print(f"{'ID':<5} {'Etiqueta':<10} {'Media':<10} {'Mediana':<10} "
          f"{'Moda':<10} {'Umbral':<10} {'Ratio':<10}")
    print("-" * 65)
    for msg in clasificados:
        v = msg["votos"]
        print(f"{msg['id']:<5} {msg['etiqueta']:<10} {v['media']:<10} "
              f"{v['mediana']:<10} {v['moda']:<10} {v['umbral']:<10} "
              f"{v['ratio']:<10}")

    guardar_clasificados(clasificados, SALIDA)
    return clasificados


if __name__ == "__main__":
    ejecutar()
