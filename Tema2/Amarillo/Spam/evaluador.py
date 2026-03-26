# evaluador
# Compara predicciones contra ground truth y genera metricas

import yaml
from pathlib import Path

DIR_DATOS = Path(__file__).parent / "datos"
RUTA_CLAS = DIR_DATOS / "mensajes_clasificados.yaml"
RUTA_NUEVOS = DIR_DATOS / "mensajes_nuevos.yaml"
RUTA_SALIDA = DIR_DATOS / "metricas.yaml"


def evaluar(real: list, pred: list) -> dict:
    # Calcula VP, VN, FP, FN y metricas (Accuracy, Precision, Recall, etc.)
    vp = vn = fp = fn = 0
    for r, p in zip(real, pred):
        if r == "spam" and p == "spam": vp += 1
        elif r == "no_spam" and p == "no_spam": vn += 1
        elif r == "no_spam" and p == "spam": fp += 1
        else: fn += 1
    
    total = vp + vn + fp + fn
    return {
        "vp": vp, "vn": vn, "fp": fp, "fn": fn,
        "accuracy": round((vp + vn) / total, 4) if total > 0 else 0,
        "precision": round(vp / (vp + fp), 4) if (vp + fp) > 0 else 0,
        "recall": round(vp / (vp + fn), 4) if (vp + fn) > 0 else 0
    }


def main() -> None:
    if not RUTA_CLAS.exists(): return
    with open(RUTA_CLAS, "r") as f: preds = [m["etiqueta"] for m in yaml.safe_load(f)["mensajes_clasificados"]]
    with open(RUTA_NUEVOS, "r") as f: msgs = yaml.safe_load(f)["mensajes"]

    print("=" * 60 + "\n  EVALUADOR - Supervisor Ground Truth\n" + "=" * 60)
    reales = []
    for m in msgs:
        print(f"  Mensaje: {m['texto']}")
        reales.append("spam" if input("  ¿Es spam? (s/n): ").lower() == "s" else "no_spam")

    res = evaluar(reales, preds)
    print(f"\n  VP: {res['vp']} | VN: {res['vn']} | FP: {res['fp']} | FN: {res['fn']}")
    print(f"  Accuracy: {res['accuracy']} | Precision: {res['precision']} | Recall: {res['recall']}")

    with open(RUTA_SALIDA, "w") as f: yaml.dump(res, f)


if __name__ == "__main__":
    main()
