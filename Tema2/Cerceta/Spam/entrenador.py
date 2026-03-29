import json, tomllib
from pathlib import Path

# Archivos
RUTA = Path(__file__).parent
ENTRADA = RUTA / "mensajes.toml"
SALIDA = RUTA / "entrenador.json"

# Carga de mensajes
with open(ENTRADA, "rb") as archivo:
    mensajes: dict[str, int | str] = tomllib.load(archivo)["mensajes"]


# Entrenador
def entrenador(datos: dict = mensajes):
    dta = datos
    etiquetas = {"spam", "no_spam"}

    txt_msj = list(
        map(
            lambda x: {
                "id": x["id"],
                "texto": x["texto"].strip(),
                "etiqueta": x["etiqueta"] if x["etiqueta"] in etiquetas else "no_spam",
            },
            dta,
        )
    )

    spam = sum(1 for m in txt_msj if m["etiqueta"] == "spam")
    no_spam = sum(1 for m in txt_msj if m["etiqueta"] == "no_spam")
    total = len(txt_msj)

    return {
        "resultados": {
            "total": total,
            "spam": spam,
            "no_spam": no_spam,
            "p_spam": round(spam / total, 4) if total else 0,
            "p_no_spam": round(no_spam / total, 4) if total else 0,
        },
        "mensajes": txt_msj,
    }


# Guardar
with open(SALIDA, "w", encoding="utf-8") as archivo:
    json.dump(entrenador(), archivo, ensure_ascii=False, indent=2)

print(f" Archivo generado: {SALIDA}")
