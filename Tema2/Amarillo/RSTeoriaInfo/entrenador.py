# Calcula la entropia de cada caracteristica y guarda pesos_ordenados.yaml

import math
import yaml
from pathlib import Path

DIR_DATOS = Path(__file__).parent / "datos"
RUTA_CONOCIMIENTO = DIR_DATOS / "conocimiento.yaml"
RUTA_PESOS = DIR_DATOS / "pesos_ordenados.yaml"


def cargar_conocimiento() -> dict:
    # Carga YAML de conocimiento
    with open(RUTA_CONOCIMIENTO, "r", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)


def calcular_entropia(candidatos: list, caracteristica: str, animales: dict) -> float:
    # H = -(p_si * log2(p_si) + p_no * log2(p_no))
    total = len(candidatos)
    if total == 0:
        return 0.0

    cantidad_si = sum(1 for n in candidatos if animales[n][caracteristica] == 1)
    cantidad_no = total - cantidad_si

    if cantidad_si == 0 or cantidad_no == 0:
        return 0.0

    p_si, p_no = cantidad_si / total, cantidad_no / total
    return round(-(p_si * math.log2(p_si) + p_no * math.log2(p_no)), 6)


def ordenar_por_entropia(conocimiento: dict) -> list:
    # Ordena caracteristicas de mayor a menor entropia
    animales = conocimiento["animales"]
    caracs = conocimiento["caracteristicas"]
    candidatos = list(animales.keys())

    entropias = [
        {"caracteristica": c, "entropia": calcular_entropia(candidatos, c, animales)}
        for c in caracs
    ]
    entropias.sort(key=lambda x: x["entropia"], reverse=True)
    return entropias


def guardar_pesos(orden: list) -> None:
    # Guarda el orden optimo en YAML
    datos = {"orden_optimo": orden}
    with open(RUTA_PESOS, "w", encoding="utf-8") as archivo:
        yaml.dump(datos, archivo, allow_unicode=True, sort_keys=False)
    print(f"  Archivo generado: {RUTA_PESOS}")


def main() -> None:
    if not RUTA_CONOCIMIENTO.exists():
        print("[Error] Falta conocimiento.yaml")
        return

    conocimiento = cargar_conocimiento()
    orden = ordenar_por_entropia(conocimiento)

    print("=" * 60)
    print("  ENTRENADOR - Calculo de Entropia")
    print("=" * 60)
    for item in orden:
        print(f"  {item['caracteristica']:<20} {item['entropia']:>10.6f}")

    guardar_pesos(orden)


if __name__ == "__main__":
    main()
