import yaml
import re

ruta_datos = "10msjspam.txt"
ruta_predicciones = "clasificador.yaml"
ruta_salida = "metricas_evaluacion.yaml"

# Leer archivo con etiquetas reales
with open(ruta_datos, "r", encoding="utf-8") as archivo:
    texto_base = archivo.read()

# Extraer etiqueta + mensaje
regex = re.compile(r'(?i)^\s*(SPAM|NO\s*SPAM)\s*\n*\s*"(.+?)"', re.DOTALL | re.MULTILINE)
coincidencias = regex.findall(texto_base)

valores_reales = {}
for tipo, contenido in coincidencias:
    limpio = contenido.strip().replace('\n', ' ')
    etiqueta = "spam" if tipo.upper().strip() == "SPAM" else "no_spam"
    valores_reales[limpio] = etiqueta

# Leer clasificaciones generadas
with open(ruta_predicciones, "r", encoding="utf-8") as archivo:
    predicciones = yaml.safe_load(archivo)

# Inicializar contadores
tp = fp = tn = fn = 0

# Función para normalizar texto
def normalizar(cadena):
    return cadena.strip().replace('\n', ' ')

# Comparar resultados
for mensaje_real, etiqueta_real in valores_reales.items():
    etiqueta_predicha = None
    
    for mensaje_predicho, datos in predicciones.items():
        if normalizar(mensaje_predicho) == mensaje_real:
            etiqueta_predicha = datos.get("clasificacion")
            break
    
    if etiqueta_predicha is None:
        continue

    if etiqueta_real == "spam":
        if etiqueta_predicha == "spam":
            tp += 1
        else:
            fn += 1
    else:
        if etiqueta_predicha == "spam":
            fp += 1
        else:
            tn += 1

# Cálculo de métricas
total = tp + fp + tn + fn

acc = (tp + tn) / total if total > 0 else 0
prec = tp / (tp + fp) if (tp + fp) != 0 else 0
rec = tp / (tp + fn) if (tp + fn) != 0 else 0
spec = tn / (tn + fp) if (tn + fp) != 0 else 0
prev = (tp + fn) / total if total > 0 else 0

f1_score = 0
if prec + rec > 0:
    f1_score = 2 * (prec * rec) / (prec + rec)

resultado_metricas = {
    "accuracy": round(acc, 3),
    "precision": round(prec, 3),
    "recall": round(rec, 3),
    "prevalence": round(prev, 3)
}

# Guardar métricas
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    yaml.dump(resultado_metricas, archivo, allow_unicode=True, sort_keys=False)

print("Métricas calculadas y guardadas correctamente.")