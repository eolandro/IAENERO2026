import yaml

def evaluar():

    TP = TN = FP = FN = 0

    try:
        with open("resultados.yml", encoding="utf-8") as f:
            datos = yaml.safe_load(f)

    except FileNotFoundError:
        print("Error: No se encontró el archivo resultados.yml")
        return

    except yaml.YAMLError as e:
        print("Error al leer YAML:", e)
        return

    if not datos:
        print("No hay datos en el archivo.")
        return

    for i, item in enumerate(datos, start=1):

        try:
            mensaje = item["mensaje"]
            pred = item["prediccion"].strip().lower()
        except KeyError:
            print(f"[ERROR] Estructura inválida en registro {i}: {item}")
            continue

        if pred not in ("spam", "ham"):
            print(f"[ADVERTENCIA] Predicción inválida en registro {i}: {pred}")
            continue

        real = input(f"Clasificación real de '{mensaje}' (spam/ham): ").strip().lower()

        if real not in ("spam", "ham"):
            print("Entrada inválida, se omite...")
            continue

        if real == "spam" and pred == "spam":
            TP += 1
        elif real == "spam" and pred == "ham":
            FN += 1
        elif real == "ham" and pred == "spam":
            FP += 1
        elif real == "ham" and pred == "ham":
            TN += 1

    total = TP + TN + FP + FN

    if total == 0:
        print("No hay datos válidos para evaluar.")
        return

    accuracy = (TP + TN) / total
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    prevalence = (TP + FN) / total

    print("\n=== RESULTADOS ===")
    print(f"TP: {TP}  TN: {TN}  FP: {FP}  FN: {FN}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"Prevalence: {prevalence:.4f}")