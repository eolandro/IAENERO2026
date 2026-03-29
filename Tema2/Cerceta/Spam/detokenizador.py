import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

from utilitario import tokenizar


# Rutas
DIR_BASE = Path(__file__).parent
ENTRADA = DIR_BASE / "entrenador.json"  # tu R006
SALIDA = DIR_BASE / "detokenizador.json"


def cargar_json(ruta: Path) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def agrupar_tokens_por_clase(mensajes: list[dict]) -> dict[str, list[str]]:
    """
    Devuelve {clase: [tokens...]} usando defaultdict + map.
    """
    acumulado: dict[str, list[str]] = defaultdict(list)

    def acumular(mensaje: dict) -> None:
        clase = mensaje["etiqueta"]
        tokens = tokenizar(mensaje["texto"])
        acumulado[clase].extend(tokens)

    list(map(acumular, mensajes))
    return dict(acumulado)


def calcular_prob_condicional(
    tokens_spam: list[str],
    tokens_no_spam: list[str],
    p_spam: float,
    p_no_spam: float,
    suavizado: float = 1.0,
) -> dict:
    """
    Calcula:
        P(token | spam)
        P(token | no_spam)
        P(spam | token) vía Bayes.
    """
    conteo_spam = Counter(tokens_spam)
    conteo_no_spam = Counter(tokens_no_spam)

    vocab = set(conteo_spam) | set(conteo_no_spam)
    total_spam = len(tokens_spam) + suavizado * len(vocab)
    total_no_spam = len(tokens_no_spam) + suavizado * len(vocab)

    def calcular_token(token: str) -> tuple[str, dict]:
        p_t_spam = (conteo_spam.get(token, 0) + suavizado) / total_spam
        p_t_no_spam = (conteo_no_spam.get(token, 0) + suavizado) / total_no_spam

        numerador = p_t_spam * p_spam
        denominador = numerador + p_t_no_spam * p_no_spam
        p_spam_dado_token = numerador / denominador if denominador else 0.5

        return token, {
            "P_token_dado_spam": round(p_t_spam, 6),
            "P_token_dado_no_spam": round(p_t_no_spam, 6),
            "P_spam_dado_token": round(p_spam_dado_token, 6),
            "frec_spam": conteo_spam.get(token, 0),
            "frec_no_spam": conteo_no_spam.get(token, 0),
        }

    return dict(map(calcular_token, sorted(vocab)))


def resumen_tokens(tokens: list[str], top: int = 10) -> dict:
    conteo = Counter(tokens)
    return {
        "total_tokens": len(tokens),
        "vocab_unico": len(conteo),
        "top_tokens": dict(conteo.most_common(top)),
    }


def guardar_json(datos: dict, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"\nDestokenizador guardado: {ruta}\n")


def main():
    print("█" * 20)
    print("R007 - DETOKENIZADOR")
    print("█" * 20)

    # Cargar entrenador.json (tu R006)
    conocimiento = cargar_json(ENTRADA)

    # Metadatos y mensajes
    meta = conocimiento.get("datos", {})
    mensajes = conocimiento["mensajes"]

    p_spam = meta["p_spam"]
    p_no_spam = meta["p_no_spam"]

    # Tokenizar y agrupar por clase
    tokens_por_clase = agrupar_tokens_por_clase(mensajes)
    tokens_spam = tokens_por_clase.get("spam", [])
    tokens_no_spam = tokens_por_clase.get("no_spam", [])

    # Tabla de probabilidades
    tabla_prob = calcular_prob_condicional(
        tokens_spam,
        tokens_no_spam,
        p_spam,
        p_no_spam,
    )

    salida = {
        "metadata": {
            "version": "1.0",
            "modulo": "Detokenizador",
            "generado": datetime.now().isoformat(),
            "vocab_total": len(tabla_prob),
            "p_spam": p_spam,
            "p_no_spam": p_no_spam,
            "resumen_spam": resumen_tokens(tokens_spam),
            "resumen_no_spam": resumen_tokens(tokens_no_spam),
        },
        "tabla_probabilidades": tabla_prob,
    }

    print(
        f"""
Resultados:
    - Vocabulario: {len(tabla_prob)} tokens
    - Tokens spam: {len(tokens_spam)}
    - Tokens no_spam: {len(tokens_no_spam)}
"""
    )

    # Top 5 tokens más "spam"
    top_spam = sorted(
        tabla_prob.items(),
        key=lambda x: x[1]["P_spam_dado_token"],
        reverse=True,
    )[:5]

    print("Top 5 tokens spam:")
    list(
        map(
            lambda x: print(
                f"    - {x[0]}: P(spam|token) = {x[1]['P_spam_dado_token']:.4f}"
            ),
            top_spam,
        )
    )

    guardar_json(salida, SALIDA)

    return salida


if __name__ == "__main__":
    main()
