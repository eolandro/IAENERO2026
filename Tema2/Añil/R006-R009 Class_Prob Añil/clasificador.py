import json
import math
import statistics
from entrenador import limpiar_texto

MENSAJES_NUEVOS = [
    "Hola te mando el archivo",
    "Gana dinero con este metodo",
    "Nos vemos en la reunion",
    "Oferta limitada compra ya",
    "Puedes revisar la tarea",
    "Haz clic aqui para ganar premio",
    "Te envio el reporte",
    "Promocion especial solo hoy",
    "Vamos al cine manana",
    "Dinero gratis solo registrate"
]

# Probabilidad mínima para palabras desconocidas 
DEFAULT_PROB = 1e-6


def _obtener_probabilidades(palabras, tabla):
    """
    Devuelve listas de P(spam|word) y P(no_spam|word) para cada token.
    Palabras desconocidas reciben DEFAULT_PROB.
    """
    probs_spam    = []
    probs_no_spam = []
    for p in palabras:
        probs_spam.append(tabla[p]["spam"]    if p in tabla else DEFAULT_PROB)
        probs_no_spam.append(tabla[p]["no_spam"] if p in tabla else DEFAULT_PROB)
    return probs_spam, probs_no_spam

# ============================== MÉTODOS DE CLASIFICACIÓN ==============================#


def metodo_bayes(palabras, tabla):
    """
    Naive Bayes con log-probabilidades.
    Retorna 'spam' o 'no_spam'.
    """
    score_spam    = math.log(0.5)
    score_no_spam = math.log(0.5)

    probs_spam, probs_no_spam = _obtener_probabilidades(palabras, tabla)
    for ps, pn in zip(probs_spam, probs_no_spam):
        score_spam    += math.log(ps)
        score_no_spam += math.log(pn)

    return "spam" if score_spam > score_no_spam else "no_spam"


def metodo_democracia(palabras, tabla):
    """
    Voto por palabra: cada token vota si P(spam) > P(no_spam).
    En empate, gana no_spam (sesgo conservador).
    Retorna 'spam' o 'no_spam'.
    """
    votos_spam    = 0
    votos_no_spam = 0

    probs_spam, probs_no_spam = _obtener_probabilidades(palabras, tabla)
    for ps, pn in zip(probs_spam, probs_no_spam):
        if ps > pn:
            votos_spam += 1
        else:
            votos_no_spam += 1

    return "spam" if votos_spam > votos_no_spam else "no_spam"


def metodo_media(palabras, tabla):
    """
    Calcula la media de P(spam|word) y P(no_spam|word).
    Retorna 'spam' si media_spam > media_no_spam.
    """
    probs_spam, probs_no_spam = _obtener_probabilidades(palabras, tabla)
    media_spam    = statistics.mean(probs_spam)
    media_no_spam = statistics.mean(probs_no_spam)
    return "spam" if media_spam > media_no_spam else "no_spam"


def metodo_mediana(palabras, tabla):
    """
    Calcula la mediana de P(spam|word) y P(no_spam|word).
    Retorna 'spam' si mediana_spam > mediana_no_spam.
    """
    probs_spam, probs_no_spam = _obtener_probabilidades(palabras, tabla)
    mediana_spam    = statistics.median(probs_spam)
    mediana_no_spam = statistics.median(probs_no_spam)
    return "spam" if mediana_spam > mediana_no_spam else "no_spam"


def metodo_moda(palabras, tabla):
    """
    Por cada token, asigna la etiqueta con mayor probabilidad.
    La moda de esas etiquetas determina la clase.
    En empate, gana no_spam.
    """
    etiquetas = []
    probs_spam, probs_no_spam = _obtener_probabilidades(palabras, tabla)
    for ps, pn in zip(probs_spam, probs_no_spam):
        etiquetas.append("spam" if ps > pn else "no_spam")

    try:
        moda = statistics.mode(etiquetas)
    except statistics.StatisticsError:
        # Empate perfecto: conservador → no_spam
        moda = "no_spam"
    return moda


# ============================== CONSENSO FINAL ============================== #

def consenso_final(votos):
    """
    Toma la lista de resultados de todos los métodos y
    aplica votación mayoritaria. En empate, gana no_spam.
    """
    spam_count    = votos.count("spam")
    no_spam_count = votos.count("no_spam")
    return "spam" if spam_count > no_spam_count else "no_spam"


# ============================== CLASIFICAR UN MENSAJE ==============================#

def clasificar_mensaje(mensaje, tabla):
    """
    Aplica los 5 métodos y devuelve un dict con todos los resultados.
    """
    palabras = limpiar_texto(mensaje)

    if not palabras:
        return {
            "bayes":      "no_spam",
            "democracia": "no_spam",
            "media":      "no_spam",
            "mediana":    "no_spam",
            "moda":       "no_spam",
            "consenso":   "no_spam"
        }

    bayes      = metodo_bayes(palabras, tabla)
    democracia = metodo_democracia(palabras, tabla)
    media      = metodo_media(palabras, tabla)
    mediana    = metodo_mediana(palabras, tabla)
    moda       = metodo_moda(palabras, tabla)
    consenso   = consenso_final([bayes, democracia, media, mediana, moda])

    return {
        "bayes":      bayes,
        "democracia": democracia,
        "media":      media,
        "mediana":    mediana,
        "moda":       moda,
        "consenso":   consenso
    }


# ============================== CLASIFICADOR PRINCIPAL ============================== #

def clasificador():
    """
    R008 - Clasificador
    Lee probabilidades.json, clasifica MENSAJES_NUEVOS con 5 métodos
    y genera resultados.json.
    """
    print("========== CLASIFICADOR (R008) ==========")

    with open("probabilidades.json", encoding="utf-8") as f:
        tabla = json.load(f)

    resultados = []

    encabezado = f"{'#':<4} {'Mensaje':<35} {'Bayes':<10} {'Democracia':<12} {'Media':<10} {'Mediana':<10} {'Moda':<10} {'Consenso'}"
    print(encabezado)
    print("-" * len(encabezado))

    for i, mensaje in enumerate(MENSAJES_NUEVOS):
        r = clasificar_mensaje(mensaje, tabla)

        fila = (
            f"{i+1:<4} {mensaje:<35} "
            f"{r['bayes']:<10} {r['democracia']:<12} "
            f"{r['media']:<10} {r['mediana']:<10} "
            f"{r['moda']:<10} {r['consenso']}"
        )
        print(fila)

        resultados.append({
            "mensaje":    mensaje,
            "prediccion": r["consenso"],
            "detalle":    r
        })

    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("\n✔ resultados.json generado.\n")
    return resultados
