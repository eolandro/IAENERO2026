"""
Evaluador
El supervisor etiqueta los mensajes nuevos,
se compara con los resultados del clasificador y se calculan las métricas:
Accuracy, Precision, Recall, Prevalence.
"""

import os
from ruamel.yaml import YAML


yaml = YAML()
yaml.preserve_quotes = True

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLASIFICADOS = os.path.join(DATA_DIR, "mensajes_clasificados.yml")
MENSAJES_NUEVOS = os.path.join(DATA_DIR, "mensajes_nuevos.yml")
SALIDA = os.path.join(DATA_DIR, "metricas.yml")


def cargar_clasificados(ruta):
    """Carga mensajes clasificados por el sistema."""
    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.load(f)
    return datos["mensajes_clasificados"]


def cargar_mensajes(ruta):
    """Carga mensajes nuevos para que el supervisor los etiquete."""
    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.load(f)
    return datos["mensajes"]


def etiquetar_ground_truth(mensajes):
    """
    El supervisor etiqueta los mensajes nuevos para poder evaluar el clasificador.
    """
    etiquetas = []
    print("\n" + "=" * 60)
    print("  EVALUADOR - Clasificación del Supervisor")
    print("=" * 60)
    print("Clasifica cada mensaje como 'spam' o 'no_spam'.\n")

    for msg in mensajes:
        print(f"--- Mensaje {msg['id']} ---")
        print(f"  \"{msg['texto']}\"")

        while True:
            respuesta = input("  ¿Es spam? (s/n): ").strip().lower()
            if respuesta in ("s", "n"):
                break
            print("  Por favor responde 's' para spam o 'n' para no_spam.")

        etiqueta = "spam" if respuesta == "s" else "no_spam"
        etiquetas.append(etiqueta)
        print(f"  -> Etiquetado como: {etiqueta}\n")

    return etiquetas


def construir_matriz_confusion(reales, predichos):
    """
    Construye la matriz de confusión.
    Positivo = spam, Negativo = no_spam.

    Retorna: TP, TN, FP, FN
    """
    tp = tn = fp = fn = 0

    for real, pred in zip(reales, predichos):
        if real == "spam" and pred == "spam":
            tp += 1  # Verdadero Positivo
        elif real == "no_spam" and pred == "no_spam":
            tn += 1  # Verdadero Negativo
        elif real == "no_spam" and pred == "spam":
            fp += 1  # Falso Positivo
        elif real == "spam" and pred == "no_spam":
            fn += 1  # Falso Negativo

    return tp, tn, fp, fn


def calcular_metricas(tp, tn, fp, fn):
    """
    Calcula las métricas de evaluación:
    - Accuracy: (TP + TN) / Total
    - Precision: TP / (TP + FP)
    - Recall: TP / (TP + FN)
    - Prevalence: (TP + FN) / Total
    """
    total = tp + tn + fp + fn

    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    prevalence = (tp + fn) / total if total > 0 else 0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "prevalence": round(prevalence, 4),
    }


def guardar_metricas(metricas, matriz, ruta):
    """Guarda las métricas y la matriz de confusión en YAML."""
    datos = {
        "matriz_confusion": {
            "verdadero_positivo_TP": matriz[0],
            "verdadero_negativo_TN": matriz[1],
            "falso_positivo_FP": matriz[2],
            "falso_negativo_FN": matriz[3],
        },
        "metricas": {
            "accuracy": float(metricas["accuracy"]),
            "precision": float(metricas["precision"]),
            "recall": float(metricas["recall"]),
            "prevalence": float(metricas["prevalence"]),
        },
    }
    with open(ruta, "w", encoding="utf-8") as f:
        yaml.dump(datos, f)
    print(f"Archivo generado: {ruta}")


def ejecutar():
    """Ejecuta la etapa de evaluación completa."""
    clasificados = cargar_clasificados(CLASIFICADOS)
    mensajes = cargar_mensajes(MENSAJES_NUEVOS)

    # Supervisor etiqueta ground truth
    ground_truth = etiquetar_ground_truth(mensajes)

    # Obtener predicciones del clasificador
    predicciones = [msg["etiqueta"] for msg in clasificados]

    # Construir matriz de confusión
    tp, tn, fp, fn = construir_matriz_confusion(ground_truth, predicciones)

    # Calcular métricas
    metricas = calcular_metricas(tp, tn, fp, fn)

    # Mostrar resultados
    print("\n" + "=" * 60)
    print("  RESULTADOS DE EVALUACIÓN")
    print("=" * 60)
    print(f"\nMatriz de Confusión:")
    print(f"  {'':>20} {'Pred: Spam':<15} {'Pred: No_Spam':<15}")
    print(f"  {'Real: Spam':<20} TP = {tp:<10} FN = {fn:<10}")
    print(f"  {'Real: No_Spam':<20} FP = {fp:<10} TN = {tn:<10}")
    print(f"\nMétricas:")
    print(f"  Accuracy:    {metricas['accuracy']}")
    print(f"  Precision:   {metricas['precision']}")
    print(f"  Recall:      {metricas['recall']}")
    print(f"  Prevalence:  {metricas['prevalence']}")

    guardar_metricas(metricas, (tp, tn, fp, fn), SALIDA)
    return metricas


if __name__ == "__main__":
    ejecutar()
