import yaml

SALIDA = "animales.yaml"
NUM_ATRIBUTOS = 12
NUM_ANIMALES  = 12


def pedir_atributos(n):
    print("\nIngresa los atributos:")
    atributos = []
    for i in range(1, n + 1):
        while True:
            val = input(f"  Atributo {i}: ").strip().lower()
            if val:
                atributos.append(val)
                break
            print("  Ingresa un atributo valido.")
    return atributos


def pedir_animales(n):
    print("\nIngresa los animales:")
    animales = []
    for i in range(1, n + 1):
        while True:
            val = input(f"  Animal {i}: ").strip().lower()
            if val:
                animales.append(val)
                break
            print("  Ingresa un nombre valido.")
    return animales


def main():
    atributos = pedir_atributos(NUM_ATRIBUTOS)
    animales  = pedir_animales(NUM_ANIMALES)

    estructura = {a: {attr: "" for attr in atributos} for a in animales}

    with open(SALIDA, "w", encoding="utf-8") as f:
        yaml.dump(estructura, f, allow_unicode=True,
                  default_flow_style=False, sort_keys=False)

    print(f"\nGuardado en '{SALIDA}'")
    print("Siguiente: entrenador.py")


if __name__ == "__main__":
    main()