import json, tomllib, pandas
from pathlib import Path

RUTA = Path(__file__).parent
ENTRADA = RUTA / "mensajes_nuevos.toml"
CLASIFICACIONES = RUTA / "clasificador.json"
SALIDA = RUTA / "evaluador.json"


def cargar_mensajes(ruta: Path):
    with open(ruta, "rb") as f:
        return tomllib.load(f)


def cargar_detokenizador(ruta: Path):
    with open(ruta, "r") as f:
        return json.load(f)


# Matriz de confusión
CONFUSION = {
    ("spam", "spam"): "TP",  # Verdadero Positivo
    ("no_spam", "no_spam"): "TN",  # Verdadero Negativo
    ("spam", "no_spam"): "FN",  # Falso Negativo
    ("no_spam", "spam"): "FP",  # Falso Positivo
}


def categorizar(real: str, predicho: str):
    return CONFUSION.get((real, predicho), "DESCONOCIDO")


def genMatriz(pares):
    from collections import Counter

    conteo = Counter(map(lambda p: categorizar(p[0], p[1]), pares))
    return {k: conteo.get(k, 0) for k in ("TP", "TN", "FP", "FN")}


def calculoMetricas(matriz):
    TP = matriz["TP"]
    TN = matriz["TN"]
    FP = matriz["FP"]
    FN = matriz["FN"]

    total = TP + TN + FP + FN

    exactitud = (TP + TN) / total if total else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    exhaustiva = TP / (TP + FN) if (TP + FN) else 0
    prevalencia = (TP + FN) / total if total else 0

    f1 = (
        2 * precision * exhaustiva / (precision + exhaustiva)
        if (precision + exhaustiva)
        else 0
    )

    taza_error = 1 - exactitud
    especificidad = TN / (TN + FP) if (TN + FP) else 0

    return {
        "exactitud": round(exactitud, 4),
        "precision": round(precision, 4),
        "exhaustiva": round(exhaustiva, 4),
        "prevalencia": round(prevalencia, 4),
        "f1": round(f1, 4),
        "taza_error": round(taza_error, 4),
        "especificidad": round(especificidad, 4),
    }


# Detalles de Mensaje (Combina etiquetas reales del supervisor con predicciones.)
def constructorDetalles(supervisor, clasificador):
    mapa = {m["id"]: m["etiqueta_supervisor"] for m in supervisor}

    def enriquecer(clasif):
        real = mapa.get(clasif["id"], "no_spam")
        predicho = clasif["etiqueta"]
        categoria = categorizar(real, predicho)
        correcto = categoria in ("TP", "TN")
        return {
            "id": clasif["id"],
            "etiqueta_real": real,
            "etiqueta_predicha": predicho,
            "prob_consenso": clasif["prob_consenso"],
            "resultado": categoria,
            "correcto": correcto,
        }

    return list(map(enriquecer, clasificador))


def generarResultado(datos, ruta: Path):
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    print(f"Evaluación guardada: {ruta}")


# Datos consola
def imprimirMatriz(matriz):
    print(
        "-" * 40,
        "Matriz de Confusión:",
        "-" * 40,
        pandas.DataFrame(
            {
                "Predicción SPAM": [matriz["TP"], matriz["FP"]],
                "Predicción NO SPAM": [matriz["FN"], matriz["TN"]],
            },
            index=["Real SPAM", "Real NO SPAM"],
        ),
        sep="\n",
    )


def imprimirMetrica(metrica):
    print(
        "-" * 40,
        "Metricas:",
        "-" * 40,
        pandas.DataFrame([metrica], columns=metrica.keys()),
        sep="\n",
    )


def main():
    mensajes = cargar_mensajes(ENTRADA).get("mensajes", [])
    clasficaciones = cargar_detokenizador(CLASIFICACIONES)["clasificaciones"]

    detalle = constructorDetalles(mensajes, clasficaciones)

    pares = list(map(lambda d: (d["etiqueta_real"], d["etiqueta_predicha"]), detalle))
    matriz = genMatriz(pares)
    metricas = calculoMetricas(matriz)

    imprimirMatriz(matriz)
    print("")
    imprimirMetrica(metricas)
    print("")
    print(
        "-" * 40,
        pandas.DataFrame(
            {
                "REAL": [d["etiqueta_real"] for d in detalle],
                "PREDICHO": [d["etiqueta_predicha"] for d in detalle],
                "RESULTADO": [d["resultado"] for d in detalle],
                "CORRECTO": ["OK" if d["correcto"] else "X" for d in detalle],
            },
            index=[d["id"] for d in detalle],
        ),
        sep="\n",
    )

    info = {
        "matriz": {
            "datos": {
                "TP": matriz["TP"],
                "TN": matriz["TN"],
                "FP": matriz["FP"],
                "FN": matriz["FN"],
            },
            "desc": {
                "TP": "Verdadero Positivo: spam detectado correctamente",
                "TN": "Verdadero Negativo: no_spam detectado correctamente",
                "FP": "Falso Positivo: no_spam clasificado como spam",
                "FN": "Falso Negativo: spam clasificado como no_spam",
            },
        },
        "metricas": metricas,
        "detalles": detalle,
    }

    print("")
    generarResultado(info, SALIDA)
    print("")

    return info


if __name__ == "__main__":
    main()
