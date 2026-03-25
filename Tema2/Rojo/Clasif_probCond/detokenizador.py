import json
import re

archivo_entrada = "conocimiento_entrenamiento.json"
archivo_salida = "tabla_probabilidades.json"

stopwords = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "a", "ante", "bajo", "con", "contra", "desde",
    "en", "entre", "hacia", "hasta", "para", "por", "segun", "sin",
    "sobre", "tras", "y", "e", "o", "u", "que", "como", "al"
}

frecuencia_s = {}
frecuencia_n = {}
total_tokens_s = 0
total_tokens_n = 0

try:
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        filas = json.load(f)
except FileNotFoundError:
    print(f"No existe {archivo_entrada}. Ejecuta entrenador.py primero.")
    raise SystemExit(1)

if len(filas) != 10:
    print(f"Se esperaban 10 mensajes en {archivo_entrada} y hay {len(filas)}.")
    raise SystemExit(1)

for fila in filas:
    mensaje = fila["mensaje"].lower()
    etiqueta = fila["etiqueta"].strip().lower()

    mensaje = re.sub(r"[^\w\sáéíóúüñ]", " ", mensaje)
    partes = mensaje.split()

    tokens = []
    for token in partes:
        if token not in stopwords:
            tokens.append(token)

    for token in tokens:
        if etiqueta == "s":
            frecuencia_s[token] = frecuencia_s.get(token, 0) + 1
            total_tokens_s += 1
        elif etiqueta == "n":
            frecuencia_n[token] = frecuencia_n.get(token, 0) + 1
            total_tokens_n += 1

vocabulario = set(frecuencia_s.keys()) | set(frecuencia_n.keys())

filas_salida = []
for token in sorted(vocabulario):
    fs = frecuencia_s.get(token, 0)
    fn = frecuencia_n.get(token, 0)

    if total_tokens_s > 0:
        ps = fs / total_tokens_s
    else:
        ps = 0

    if total_tokens_n > 0:
        pn = fn / total_tokens_n
    else:
        pn = 0

    filas_salida.append({
        "token": token,
        "frecuencia_s": fs,
        "frecuencia_n": fn,
        "prob_s": ps,
        "prob_n": pn,
    })

with open(archivo_salida, "w", encoding="utf-8") as f:
    json.dump(filas_salida, f, ensure_ascii=False, indent=2)

print(f"Archivo generado: {archivo_salida}")
