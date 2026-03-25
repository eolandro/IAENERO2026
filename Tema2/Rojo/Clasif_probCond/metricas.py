import json

archivo_entrada = "clasificacion_resultados.json"
archivo_salida = "metricas_resultados.txt"

try:
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        filas = json.load(f)
except FileNotFoundError:
    print(f"No existe {archivo_entrada}. Ejecuta clasificador.py primero.")
    raise SystemExit(1)

if len(filas) != 10:
    print(f"Se esperaban 10 mensajes en {archivo_entrada} y hay {len(filas)}.")
    raise SystemExit(1)

TP = 0
TN = 0
FP = 0
FN = 0

print("METRICAS")
print("Responde para cada mensaje si realmente es spam o no.")

for i, fila in enumerate(filas, start=1):
    mensaje = fila["mensaje"]
    pred = fila["prediccion"].strip().lower()

    if pred == "s":
        pred_texto = "spam"
    else:
        pred_texto = "no_spam"

    print(f"\nMensaje {i}: {mensaje}")
    print(f"Predicción del clasificador: {pred_texto}")

    while True:
        real_in = input("¿Etiqueta real? (s/n o spam/no_spam): ").strip().lower()
        if real_in == "s" or real_in == "spam":
            real = "s"
            break
        if real_in == "n" or real_in == "no_spam":
            real = "n"
            break
        print("Entrada inválida. Usa s/n o spam/no_spam.")

    if pred == "s" and real == "s":
        TP += 1
    elif pred == "n" and real == "n":
        TN += 1
    elif pred == "s" and real == "n":
        FP += 1
    elif pred == "n" and real == "s":
        FN += 1

total = len(filas)

if TP + FN > 0:
    recall = TP / (TP + FN)
else:
    recall = 0

if TP + FP > 0:
    precision = TP / (TP + FP)
else:
    precision = 0

if total > 0:
    accuracy = (TP + TN) / total
    prevalence = (TP + FN) / total
else:
    accuracy = 0
    prevalence = 0

lineas = [
    "Matriz de confusión",
    f"TP: {TP}",
    f"TN: {TN}",
    f"FP: {FP}",
    f"FN: {FN}",
    "",
    "Métricas",
    f"Recall: {recall}",
    f"Precision: {precision}",
    f"Accuracy: {accuracy}",
    f"Prevalence: {prevalence}",
]

with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write("\n".join(lineas))

print(f"Archivo generado: {archivo_salida}")
print("\nMatriz de confusión")
print(f"TP: {TP}")
print(f"TN: {TN}")
print(f"FP: {FP}")
print(f"FN: {FN}")
print("\nMétricas")
print(f"Recall: {recall}")
print(f"Precision: {precision}")
print(f"Accuracy: {accuracy}")
print(f"Prevalence: {prevalence}")
