import json
from collections import defaultdict

# ============================== STOPWORDS ==============================#

STOPWORDS = [
    "el", "la", "los", "las", "de", "del", "y", "a", "en",
    "para", "con", "un", "una", "unos", "unas", "que", "se",
    "su", "al", "por", "como", "me", "te", "le", "nos",
    "lo", "si", "mas", "pero", "o", "e", "ni", "es", "son",
    "has", "hay", "este", "esta", "ese", "esa", "esto"
]

MENSAJES_ENTRENAMIENTO = [
    "Gana dinero rapido desde casa",
    "Oferta exclusiva solo hoy",
    "Haz clic aqui para premio",
    "Te ganaste un premio gratis",
    "Compra ahora con descuento",
    "Hola como estas",
    "Nos vemos manana en clase",
    "Recuerda la tarea de matematicas",
    "Vamos a comer juntos",
    "Reunion a las 3 pm"
]

def limpiar_texto(texto):
    """Tokeniza y elimina stopwords del texto."""
    palabras = texto.lower().split()
    return [p for p in palabras if p not in STOPWORDS]


# ============================== ENTRENADOR ==============================#

def entrenador():
    """
    R006 - Entrenador
    Etiqueta manualmente 10 mensajes y genera entrenamiento.json.
    Si el archivo ya existe, pregunta si se desea re-etiquetar.
    """
    print("\n========== ENTRENADOR (R006) ==========")

    import os
    if os.path.exists("entrenamiento.json"):
        resp = input("entrenamiento.json ya existe. ¿Re-etiquetar? (s/n): ").strip().lower()
        if resp != "s":
            print("  Usando entrenamiento.json existente.\n")
            with open("entrenamiento.json", encoding="utf-8") as f:
                return json.load(f)

    print("Etiqueta cada mensaje: 's' = spam  |  'n' = no spam\n")

    datos = []
    for i, mensaje in enumerate(MENSAJES_ENTRENAMIENTO):
        print(f"[{i+1}/10] \"{mensaje}\"")
        while True:
            r = input("¿Es spam? (s/n): ").strip().lower()
            if r == "s":
                datos.append({"mensaje": mensaje, "etiqueta": "spam"})
                break
            elif r == "n":
                datos.append({"mensaje": mensaje, "etiqueta": "no_spam"})
                break
            else:
                print("  Escribe 's' o 'n'.")
        print()

    with open("entrenamiento.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print("✔ entrenamiento.json generado.\n")
    return datos


# ============================== DETOKENIZADOR ==============================#

def detokenizador():
    """
    R007 - DeTokenizador
    Lee entrenamiento.json, tokeniza, filtra stopwords,
    calcula probabilidad condicional con suavizado de Laplace
    y genera probabilidades.json.
    """
    print("========== DETOKENIZADOR (R007) ==========")

    with open("entrenamiento.json", encoding="utf-8") as f:
        datos = json.load(f)

    conteo_spam    = defaultdict(int)
    conteo_no_spam = defaultdict(int)
    total_spam     = 0
    total_no_spam  = 0

    for d in datos:
        palabras = limpiar_texto(d["mensaje"])
        if d["etiqueta"] == "spam":
            for p in palabras:
                conteo_spam[p] += 1
                total_spam += 1
        else:
            for p in palabras:
                conteo_no_spam[p] += 1
                total_no_spam += 1

    vocabulario = set(list(conteo_spam.keys()) + list(conteo_no_spam.keys()))
    V = len(vocabulario)

    # Suavizado de Laplace
    tabla_prob = {}
    for palabra in vocabulario:
        p_spam    = (conteo_spam[palabra]    + 1) / (total_spam    + V)
        p_no_spam = (conteo_no_spam[palabra] + 1) / (total_no_spam + V)
        tabla_prob[palabra] = {
            "spam":    round(p_spam,    6),
            "no_spam": round(p_no_spam, 6)
        }

    with open("probabilidades.json", "w", encoding="utf-8") as f:
        json.dump(tabla_prob, f, indent=4, ensure_ascii=False)

    print(f"  Palabras únicas  : {V}")
    print(f"  Tokens spam      : {total_spam}")
    print(f"  Tokens no_spam   : {total_no_spam}")
    print("✔ probabilidades.json generado.\n")

    return tabla_prob
