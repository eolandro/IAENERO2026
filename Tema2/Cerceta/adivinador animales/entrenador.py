import yaml
import os

ENTRADA = "animales.yaml"
SALIDA  = "tabla.yaml"


def preguntar(animal, atributo):
    while True:
        r = input(f"  ¿{animal} tiene '{atributo}'? [s/n]: ").strip().lower()
        if r in ("s", "n"):
            return 1 if r == "s" else 0
        print("  Responde s o n.")


def main():
    if not os.path.exists(ENTRADA):
        print(f"No se encontro '{ENTRADA}'. Ejecuta primero inicializador.py")
        return

    with open(ENTRADA, "r", encoding="utf-8") as f:
        datos = yaml.safe_load(f)

    animales   = list(datos.keys())
    atributos  = list(datos[animales[0]].keys())

    # tabla[animal][atributo] = 0 o 1
    tabla = {a: {} for a in animales}

    # Recorre por atributo — diferente a recorrer por animal
    for atributo in atributos:
        print(f"\n--- Atributo: {atributo.upper()} ---")
        for animal in animales:
            tabla[animal][atributo] = preguntar(animal, atributo)

    with open(SALIDA, "w", encoding="utf-8") as f:
        yaml.dump(tabla, f, allow_unicode=True,
                  default_flow_style=False, sort_keys=False)

    print(f"\nTabla guardada en '{SALIDA}'.")
    print("Siguiente: adivinador.py")


if __name__ == "__main__":
    main()
