# clasificador
# Filtra mensajes nuevos usando 5 metodos de consenso (democracia)

import re
import yaml
from collections import Counter
from statistics import mean, median
from pathlib import Path

DIR_DATOS = Path(__file__).parent / "datos"
RUTA_NUEVOS = DIR_DATOS / "mensajes_nuevos.yaml"
RUTA_TABLA = DIR_DATOS / "tabla_probs.yaml"
RUTA_SALIDA = DIR_DATOS / "mensajes_clasificados.yaml"

# Stopwords iguales a detokenizador.py
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
    texto = texto.lower()
    texto = re.sub(r"[¡¿.,;:!?\"'()\-\d%@#$]", " ", texto)
    return [t for t in texto.split() if t not in PALABRAS_VACIAS and len(t) > 1]


def votar(tokens: list, tabla: dict) -> tuple[str, dict]:
    # Metodos: Media, Mediana, Moda, Umbral, Ratio
    ps = [tabla[t]["p_spam"] for t in tokens if t in tabla]
    pn = [tabla[t]["p_no_spam"] for t in tokens if t in tabla]
    
    if not ps: return "no_spam", {}

    votos = {
        "media": "spam" if mean(ps) > mean(pn) else "no_spam",
        "mediana": "spam" if median(ps) > median(pn) else "no_spam",
        "moda": Counter(["spam" if tabla[t]["p_spam"] > tabla[t]["p_no_spam"] else "no_spam" 
                         for t in tokens if t in tabla]).most_common(1)[0][0],
        "umbral": "spam" if sum(ps) > sum(pn) else "no_spam",
        "ratio": "spam" if (lambda r: r > 1.0)(
            eval("*".join([str(s/n) for s, n in zip(ps, pn) if n > 0]) or "1")) else "no_spam"
    }
    return Counter(votos.values()).most_common(1)[0][0], votos


def main() -> None:
    if not RUTA_NUEVOS.exists() or not RUTA_TABLA.exists(): return
    with open(RUTA_NUEVOS, "r") as f: msgs = yaml.safe_load(f)["mensajes"]
    with open(RUTA_TABLA, "r") as f: tabla = yaml.safe_load(f)["probabilidades"]

    print("=" * 60 + "\n  CLASIFICADOR - Consenso\n" + "=" * 60)
    resultados = []
    for m in msgs:
        etiqueta, votos = votar(tokenizar(m["texto"]), tabla)
        resultados.append({"id": m["id"], "texto": m["texto"], "etiqueta": etiqueta, "votos": votos})
        print(f"  ID {m['id']}: {etiqueta}")

    with open(RUTA_SALIDA, "w") as f: yaml.dump({"mensajes_clasificados": resultados}, f)


if __name__ == "__main__":
    main()
