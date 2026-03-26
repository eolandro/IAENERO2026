# detokenizador.py
# Tokeniza mensajes y calcula probabilidades con Laplace

import re
import yaml
from collections import Counter
from pathlib import Path

DIR_DATOS = Path(__file__).parent / "datos"
RUTA_ENTRADA = DIR_DATOS / "mensajes_etiquetados.yaml"
RUTA_SALIDA = DIR_DATOS / "tabla_probs.yaml"

# Stopwords: articulos, preposiciones y conectores
PALABRAS_VACIAS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "a", "al", "ante", "bajo", "con", "contra", "de", "del", "desde",
    "en", "entre", "hacia", "hasta", "para", "por", "sin", "sobre", "tras",
    "y", "e", "o", "u", "ni", "que", "pero", "sino", "aunque",
    "si", "como", "porque", "pues", "ya",
    "me", "te", "se", "lo", "le", "nos", "les", "mi", "tu", "su",
    "es", "ha", "he", "ser", "no", "mas", "tu", "su",
}


def tokenizar(texto: str) -> list:
    # Limpia y divide texto en palabras
    texto = texto.lower()
    texto = re.sub(r"[¡¿.,;:!?\"'()\-\d%@#$]", " ", texto)
    return [t for t in texto.split() if t not in PALABRAS_VACIAS and len(t) > 1]


def calcular_probabilidades(mensajes: list) -> tuple[dict, int, int, int]:
    # P(t|clase) = (frec + 1) / (total + vocab)
    tokens_spam, tokens_nospam = [], []

    for msg in mensajes:
        tokens = tokenizar(msg["texto"])
        if msg["etiqueta"] == "spam": tokens_spam.extend(tokens)
        else: tokens_nospam.extend(tokens)

    f_spam, f_nospam = Counter(tokens_spam), Counter(tokens_nospam)
    vocab = set(f_spam.keys()) | set(f_nospam.keys())
    t_s, t_n, t_v = len(tokens_spam), len(tokens_nospam), len(vocab)

    tabla = {}
    for t in sorted(vocab):
        tabla[t] = {
            "p_spam": round((f_spam.get(t, 0) + 1) / (t_s + t_v), 6),
            "p_no_spam": round((f_nospam.get(t, 0) + 1) / (t_n + t_v), 6),
            "frec_spam": f_spam.get(t, 0),
            "frec_no_spam": f_nospam.get(t, 0),
        }
    return tabla, t_s, t_n, t_v


def main() -> None:
    if not RUTA_ENTRADA.exists(): return
    with open(RUTA_ENTRADA, "r", encoding="utf-8") as f:
        mensajes = yaml.safe_load(f)["mensajes_etiquetados"]

    print("=" * 60 + "\n  DETOKENIZADOR - Probabilidades\n" + "=" * 60)
    tabla, t_s, t_n, t_v = calcular_probabilidades(mensajes)

    datos = {"metadatos": {"total_spam": t_s, "total_no_spam": t_n, "vocab": t_v}, "probabilidades": tabla}
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        yaml.dump(datos, f, allow_unicode=True, sort_keys=False)
    print(f"  Tablas generadas: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
