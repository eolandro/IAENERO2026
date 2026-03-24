import json

def evaluador(resultados):
    """
    R009 - Evaluador
    El supervisor etiqueta los 10 mensajes nuevos, compara con las
    predicciones del clasificador y calcula:
      Accuracy, Precision, Recall, Prevalence + Matriz de Confusión.
    Guarda los resultados en evaluacion.json.
    """
    print("========== EVALUADOR (R009) ==========")
    print("Etiqueta cada mensaje para comparar con la predicción.")
    print("Escribe 's' = spam  |  'n' = no spam\n")

    etiquetas_reales = []

    for i, r in enumerate(resultados):
        print(f"[{i+1}/10] \"{r['mensaje']}\"")
        print(f"         Predicción del sistema: {r['prediccion']}")
        while True:
            resp = input("¿Es realmente spam? (s/n): ").strip().lower()
            if resp == "s":
                etiquetas_reales.append("spam")
                break
            elif resp == "n":
                etiquetas_reales.append("no_spam")
                break
            else:
                print("  Escribe 's' o 'n'.")
        print()

    # ---- Matriz de confusión ---- #
    TP = FP = TN = FN = 0

    for i in range(len(resultados)):
        pred = resultados[i]["prediccion"]
        real = etiquetas_reales[i]

        if   pred == "spam"    and real == "spam":    TP += 1
        elif pred == "spam"    and real == "no_spam": FP += 1
        elif pred == "no_spam" and real == "no_spam": TN += 1
        elif pred == "no_spam" and real == "spam":    FN += 1

    total = len(resultados)

    # ---- Métricas con protección contra división por cero ---- #
    accuracy   = (TP + TN) / total                          if total       > 0 else 0.0
    precision  = TP / (TP + FP)                             if (TP + FP)  > 0 else 0.0
    recall     = TP / (TP + FN)                             if (TP + FN)  > 0 else 0.0
    prevalence = (TP + FN) / total                          if total       > 0 else 0.0
    # F1 como métrica adicional (armónico de precision y recall)
    f1         = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    # Error complemento de accuracy
    error_rate = 1.0 - accuracy

    print("\n-------- MATRIZ DE CONFUSIÓN --------")
    print(f"{'':20} {'PRED: spam':>12} {'PRED: no_spam':>14}")
    print(f"{'REAL: spam':20} {'TP = '+str(TP):>12} {'FN = '+str(FN):>14}")
    print(f"{'REAL: no_spam':20} {'FP = '+str(FP):>12} {'TN = '+str(TN):>14}")

    print("\n-------- MÉTRICAS --------")
    print(f"  Accuracy   : {round(accuracy,   4)}")
    print(f"  Precision  : {round(precision,  4)}")
    print(f"  Recall     : {round(recall,     4)}")
    print(f"  Prevalence : {round(prevalence, 4)}")
    print(f"  F1-Score   : {round(f1,         4)}")
    print(f"  Error Rate : {round(error_rate, 4)}\n")

    # ---- Guardar resultados de evaluación ---- #
    evaluacion = {
        "matriz_confusion": {
            "TP": TP, "FP": FP,
            "TN": TN, "FN": FN
        },
        "metricas": {
            "accuracy":   round(accuracy,   4),
            "precision":  round(precision,  4),
            "recall":     round(recall,     4),
            "prevalence": round(prevalence, 4),
            "f1_score":   round(f1,         4),
            "error_rate": round(error_rate, 4)
        },
        "detalle": [
            {
                "mensaje":    resultados[i]["mensaje"],
                "prediccion": resultados[i]["prediccion"],
                "real":       etiquetas_reales[i],
                "correcto":   resultados[i]["prediccion"] == etiquetas_reales[i]
            }
            for i in range(len(resultados))
        ]
    }

    with open("evaluacion.json", "w", encoding="utf-8") as f:
        json.dump(evaluacion, f, indent=4, ensure_ascii=False)

    print("✔ evaluacion.json generado.\n")
    return evaluacion
