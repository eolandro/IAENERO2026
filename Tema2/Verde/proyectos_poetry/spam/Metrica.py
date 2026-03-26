import yaml
import re

archivo_txt = "10msjspam.txt"
archivo_resultados = "clasificador.yaml"
archivo_metricas = "metricas_evaluacion.yaml"

with open(archivo_txt, "r", encoding="utf-8") as f:
    contenido = f.read()

patron = re.compile(r'(?i)^\s*(SPAM|NO\s*SPAM)\s*\n*\s*"(.+?)"', re.DOTALL | re.MULTILINE)
pares = patron.findall(contenido)

etiquetas_reales = {}
for etiqueta, mensaje in pares:
    mensaje_limpio = mensaje.strip().replace('\n', ' ')
    etiqueta_normalizada = "spam" if etiqueta.strip().upper() == "SPAM" else "no_spam"
    etiquetas_reales[mensaje_limpio] = etiqueta_normalizada

with open(archivo_resultados, "r", encoding="utf-8") as f:
    clasificaciones = yaml.safe_load(f)

VP = FP = VN = FN = 0

for msg, real in etiquetas_reales.items():
    prediccion = None
    for m in clasificaciones:
        if m.strip().replace('\n', ' ') == msg:
            prediccion = clasificaciones[m]["clasificacion"]
            break

    if prediccion is None:
        continue

    if real == "spam" and prediccion == "spam":
        VP += 1
    elif real == "no_spam" and prediccion == "spam":
        FP += 1
    elif real == "no_spam" and prediccion == "no_spam":
        VN += 1
    elif real == "spam" and prediccion == "no_spam":
        FN += 1

# Calcular métricas
total = VP + FP + VN + FN
exactitud = (VP + VN) / total if total else 0
precision = VP / (VP + FP) if (VP + FP) else 0
sensibilidad = VP / (VP + FN) if (VP + FN) else 0
especificidad = VN / (VN + FP) if (VN + FP) else 0
prevalencia = (VP + FN) / total if total else 0
f1 = 2 * (precision * sensibilidad) / (precision + sensibilidad) if (precision + sensibilidad) else 0

metricas = {
    "Exactitud": round(exactitud, 3),
    "Precisión": round(precision, 3),
    "Sensibilidad": round(sensibilidad, 3),
    "Especificidad": round(especificidad, 3),
    "Prevalencia": round(prevalencia, 3),
    "F1-score": round(f1, 3)
}

with open(archivo_metricas, "w", encoding="utf-8") as f:
    yaml.dump(metricas, f, allow_unicode=True, sort_keys=False)
