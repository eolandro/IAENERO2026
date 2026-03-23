"""
DeTokenizador
Lee mensajes etiquetados, tokeniza, filtra stopwords
y calcula la probabilidad condicional P(token|spam) y P(token|no_spam).
Genera una tabla de probabilidades en YAML.
"""

import os
import re
from collections import Counter
from ruamel.yaml import YAML


yaml = YAML()
yaml.preserve_quotes = True

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ENTRADA = os.path.join(DATA_DIR, "mensajes_etiquetados.yml")
SALIDA = os.path.join(DATA_DIR, "tabla_probabilidades.yml")

# Stopwords en español: artículos, preposiciones, conectores
STOPWORDS = {
    # Artículos
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    # Preposiciones
    "a", "al", "ante", "bajo", "con", "contra", "de", "del", "desde",
    "en", "entre", "hacia", "hasta", "para", "por", "sin", "sobre", "tras",
    # Conectores
    "y", "e", "o", "u", "ni", "que", "pero", "sino", "aunque",
    "si", "como", "porque", "pues", "ya",
    # Pronombres y otros
    "me", "te", "se", "lo", "le", "nos", "les", "mi", "tu", "su",
    "es", "ha", "he", "ser", "no", "más",
}


def cargar_etiquetados(ruta):
    """Carga mensajes etiquetados desde YAML."""
    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.load(f)
    return datos["mensajes_etiquetados"]


def tokenizar(texto):
    """
    Tokeniza un texto: convierte a minúsculas, elimina puntuación
    y divide en palabras individuales.
    """
    texto = texto.lower()
    texto = re.sub(r"[¡¿.,;:!?\"'()\-\d%]", "", texto)
    tokens = texto.split()
    return tokens


def filtrar_stopwords(tokens):
    """Elimina artículos, preposiciones y conectores de la lista de tokens."""
    return [t for t in tokens if t not in STOPWORDS]


def calcular_probabilidades(mensajes):
    """
    Calcula P(token|spam) y P(token|no_spam) 

    P(token|clase) = (count(token, clase) + 1) / (total_tokens_clase + vocabulario)
    """
    tokens_spam = []
    tokens_no_spam = []

    for msg in mensajes:
        tokens = filtrar_stopwords(tokenizar(msg["texto"]))
        if msg["etiqueta"] == "spam":
            tokens_spam.extend(tokens)
        else:
            tokens_no_spam.extend(tokens)

    # Contar frecuencias
    freq_spam = Counter(tokens_spam)
    freq_no_spam = Counter(tokens_no_spam)

    # Vocabulario total
    vocabulario = set(list(freq_spam.keys()) + list(freq_no_spam.keys()))
    tam_vocab = len(vocabulario)

    total_spam = len(tokens_spam)
    total_no_spam = len(tokens_no_spam)

    # Calcular probabilidades con suavizado de Laplace
    tabla = {}
    for token in sorted(vocabulario):
        p_spam = round((freq_spam.get(token, 0) + 1) / (total_spam + tam_vocab), 4)
        p_no_spam = round((freq_no_spam.get(token, 0) + 1) / (total_no_spam + tam_vocab), 4)
        tabla[token] = {
            "p_spam": float(p_spam),
            "p_no_spam": float(p_no_spam),
            "freq_spam": freq_spam.get(token, 0),
            "freq_no_spam": freq_no_spam.get(token, 0),
        }

    return tabla, total_spam, total_no_spam, tam_vocab


def guardar_tabla(tabla, total_spam, total_no_spam, tam_vocab, ruta):
    """Guarda la tabla de probabilidades en YAML."""
    datos = {
        "metadata": {
            "total_tokens_spam": total_spam,
            "total_tokens_no_spam": total_no_spam,
            "tamano_vocabulario": tam_vocab,
        },
        "probabilidades": tabla,
    }
    with open(ruta, "w", encoding="utf-8") as f:
        yaml.dump(datos, f)
    print(f"Archivo generado: {ruta}")


def ejecutar():
    """Ejecuta la etapa de detokenización completa."""
    print("\n" + "=" * 60)
    print("  DETOKENIZADOR - Cálculo de Probabilidades")
    print("=" * 60)

    mensajes = cargar_etiquetados(ENTRADA)
    tabla, t_spam, t_nospam, vocab = calcular_probabilidades(mensajes)

    print(f"\nTokens en mensajes spam: {t_spam}")
    print(f"Tokens en mensajes no_spam: {t_nospam}")
    print(f"Tamaño del vocabulario: {vocab}")
    print(f"\nTabla de probabilidades ({len(tabla)} tokens):")
    print(f"{'Token':<20} {'P(t|spam)':<12} {'P(t|no_spam)':<12} {'F.Spam':<8} {'F.NoSpam':<8}")
    print("-" * 60)
    for token, vals in tabla.items():
        print(f"{token:<20} {vals['p_spam']:<12} {vals['p_no_spam']:<12} "
              f"{vals['freq_spam']:<8} {vals['freq_no_spam']:<8}")

    guardar_tabla(tabla, t_spam, t_nospam, vocab, SALIDA)
    return tabla


if __name__ == "__main__":
    ejecutar()
