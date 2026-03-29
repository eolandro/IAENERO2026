import json, tomllib, pandas
from pathlib import Path

from utilitario import tokenizar, aplicar_consenso, clasificar_por_probabilidad

# Rutas
DIRECTORIO = Path(__file__).parent
MENSAJES_NUEVOS = DIRECTORIO / "mensajes_nuevos.toml"
ENTRADA = DIRECTORIO / "detokenizador.json"
SALIDA = DIRECTORIO / "clasificador.json"

CONSENSO = "media"  # media | mediana | moda | democracia

# Mensajes Nuevos
with open(MENSAJES_NUEVOS, "rb") as f:
    mensajes_nuevos = tomllib.load(f)

# Detokenizador
with open(ENTRADA, encoding="utf-8") as f:
    detokenizador = json.load(f)


def clasificadorMensaje(mensaje, prob, prob_spam, consenso):
    tokens = tokenizar(mensaje["texto"])
    probabilidad = list(
        filter(
            lambda p: p is not None,
            map(lambda t: prob.get(t, {}).get("P_spam_dado_token"), tokens),
        )
    )
    prob_consenso = (
        aplicar_consenso(probabilidad, consenso) if probabilidad else prob_spam
    )

    etiqueta = clasificar_por_probabilidad(prob_consenso)
    return {
        "id": mensaje["id"],
        "mensaje": mensaje["texto"],
        "tokens": tokens,
        "tokens_conocidos": [t for t in tokens if t in prob],
        "probabilidad_tokens": {
            t: round(prob[t]["P_spam_dado_token"], 4) for t in tokens if t in prob
        },
        "prob_consenso": round(prob_consenso, 4),
        "metodo": consenso,
        "etiqueta": etiqueta,
    }


def clasificadorLote(mensajes, prob, prob_spam, consenso):
    return list(
        map(lambda m: clasificadorMensaje(m, prob, prob_spam, consenso), mensajes)
    )


def genJSON(datos, ruta: Path):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print(f"Clasificador guardado: {ruta}\n")


def main():
    print("█" * 20)
    print("Clasificador")
    print("█" * 20)

    mensajes = mensajes_nuevos.get("mensajes", [])

    datos = detokenizador
    tabla = datos["tabla_probabilidades"]
    prob_spam = datos["metadata"]["p_spam"]

    resultado = clasificadorLote(mensajes, tabla, prob_spam, CONSENSO)

    spam = sum(1 for m in resultado if m["etiqueta"] == "spam")
    no_spam = len(mensajes) - spam

    resultado_salida = {
        "metadata": {
            "metodo": CONSENSO,
            "mensajes": len(resultado),
            "predichos_spam": spam,
            "predichos_no_spam": no_spam,
        },
        "clasificaciones": resultado,
    }

    print(
        f"""
Mensajes: {len(mensajes)}
Predichos:
    - Spam: {spam}
    - No Spam: {no_spam}
""",
    )

    print(pandas.DataFrame(resultado))

    genJSON(resultado_salida, SALIDA)


if __name__ == "__main__":
    main()
