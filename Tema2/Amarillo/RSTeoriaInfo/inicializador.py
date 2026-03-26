# inicializador.py - R001
# Muestra un resumen de la base de conocimiento en datos/conocimiento.yaml

import yaml
from pathlib import Path

# Directorio de datos
DIR_DATOS = Path(__file__).parent / "datos"
RUTA_CONOCIMIENTO = DIR_DATOS / "conocimiento.yaml"


def cargar_conocimiento() -> dict:
    # Carga YAML de conocimiento
    with open(RUTA_CONOCIMIENTO, "r", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)


def mostrar_resumen(conocimiento: dict) -> None:
    # Muestra animales y caracteristicas cargadas
    animales = list(conocimiento["animales"].keys())
    caracteristicas = conocimiento["caracteristicas"]

    print("=" * 60)
    print("  INICIALIZADOR")
    print("=" * 60)
    print(f"\n  Animales ({len(animales)}):")
    for i, nombre in enumerate(animales, 1):
        print(f"    {i:2}. {nombre}")

    print(f"\n  Caracteristicas ({len(caracteristicas)}):")
    for carac in caracteristicas:
        print(f"    - {carac}")

    print(f"\n  Preguntas: {len(conocimiento['preguntas'])}")
    print("\n  Base de conocimiento lista.")
    print("=" * 60)


def main() -> None:
    if not RUTA_CONOCIMIENTO.exists():
        print(f"[Error] No se encontro: {RUTA_CONOCIMIENTO}")
        return

    conocimiento = cargar_conocimiento()
    mostrar_resumen(conocimiento)


if __name__ == "__main__":
    main()
