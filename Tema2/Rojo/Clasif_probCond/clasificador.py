import json
import re

archivo_yaml = "mensajes.yaml"
archivo_tabla = "tabla_probabilidades.json"
archivo_salida = "clasificacion_resultados.json"

stopwords = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "a", "ante", "bajo", "con", "contra", "desde",
    "en", "entre", "hacia", "hasta", "para", "por", "segun", "sin",
    "sobre", "tras", "y", "e", "o", "u", "que", "como", "al"
}


def leer_lista_yaml(ruta, clave):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"No existe {ruta}.")
        raise SystemExit(1)

    lista = []
    en_seccion = False

    for linea in lineas:
        txt = linea.strip()

        if not txt or txt.startswith("#"):
            continue

        if txt == f"{clave}:":
            en_seccion = True
            continue

        if en_seccion and txt.endswith(":") and not txt.startswith("-"):
            break

        if en_seccion and txt.startswith("-"):
            item = txt[1:].strip()
            if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            if item:
                lista.append(item)

    return lista


try:
    with open(archivo_tabla, "r", encoding="utf-8") as f:
        tabla = json.load(f)
except FileNotFoundError:
    print(f"No existe {archivo_tabla}. Ejecuta detokenizador.py primero.")
    raise SystemExit(1)

probabilidades = {}
for fila in tabla:
    token = fila["token"]
    prob_s = float(fila["prob_s"])
    prob_n = float(fila["prob_n"])
    probabilidades[token] = (prob_s, prob_n)

resultados = []

print("CLASIFICADOR")
print("Clasifica los 10 mensajes nuevos")

mensajes_nuevos = leer_lista_yaml(archivo_yaml, "mensajes_nuevos")
if len(mensajes_nuevos) != 10:
    print(f"Se esperaban 10 mensajes_nuevos en {archivo_yaml} y hay {len(mensajes_nuevos)}.")
    raise SystemExit(1)

for i, mensaje in enumerate(mensajes_nuevos, start=1):
    print(f"\nClasificando mensaje {i}: {mensaje}")

    limpio = mensaje.lower()
    limpio = re.sub(r"[^\w\sáéíóúüñ]", " ", limpio)
    partes = limpio.split()

    tokens = []
    for token in partes:
        if token not in stopwords:
            tokens.append(token)

    votos_s = 0
    votos_n = 0

    for token in tokens:
        if token in probabilidades:
            ps, pn = probabilidades[token]
            if ps > pn:
                votos_s += 1
            elif pn > ps:
                votos_n += 1

    if votos_s > votos_n:
        prediccion = "s"
    else:
        prediccion = "n"

    if prediccion == "s":
        texto_pred = "spam"
    else:
        texto_pred = "no_spam"

    print(f"Predicción: {texto_pred}")

    resultados.append({"mensaje": mensaje, "prediccion": prediccion})

with open(archivo_salida, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"Archivo generado: {archivo_salida}")
