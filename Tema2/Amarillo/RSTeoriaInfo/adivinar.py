# Red semántica con Teoria de la Información (RSTeoriaInfo)
# EQUIPO AMARILLO 

import yaml
from pathlib import Path

DIR_DATOS = Path(__file__).parent / "datos"
RUTA_CONOCIMIENTO = DIR_DATOS / "conocimiento.yaml"
RUTA_PESOS = DIR_DATOS / "pesos_ordenados.yaml"

RESP_SI = {"s", "si", "sí", "y", "1"}
RESP_NO = {"n", "no", "0"}


def cargar_conocimiento() -> dict:
    with open(RUTA_CONOCIMIENTO, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cargar_orden() -> list:
    # Orden de preguntas calculado por el entrenador
    with open(RUTA_PESOS, "r", encoding="utf-8") as f:
        datos = yaml.safe_load(f)
    return [item["caracteristica"] for item in datos["orden_optimo"]]


def pedir_respuesta(preg: str, num: int, total: int) -> bool:
    # Solicita s/n al usuario
    while True:
        print(f"\n  Pregunta {num} ({total} posibles)")
        print(f"  {preg}")
        entrada = input("  Tu respuesta [s/n]: ").strip().lower()
        if entrada in RESP_SI: return True
        if entrada in RESP_NO: return False
        print("  ⚠ Escribe 's' o 'n'.")


def jugar(conocimiento: dict, orden: list) -> None:
    animales = conocimiento["animales"]
    preguntas = conocimiento["preguntas"]
    candidatos = list(animales.keys())

    print("\n  Animales posibles:", ", ".join(candidatos))
    input("\n  Presiona ENTER para empezar...")

    num = 0
    while len(candidatos) > 1:
        sig_carac = None
        for c in orden:
            if len({animales[n][c] for n in candidatos}) > 1:
                sig_carac = c
                break

        if not sig_carac: break

        num += 1
        resp = pedir_respuesta(preguntas[sig_carac], num, len(candidatos))
        valor = 1 if resp else 0
        candidatos = [n for n in candidatos if animales[n][sig_carac] == valor]

        if 1 < len(candidatos) <= 3:
            print(f"  Posibles: {', '.join(candidatos)}")

    print("\n" + "=" * 60)
    if len(candidatos) == 1:
        print(f"  Tu animal es: *** {candidatos[0].upper()} *** ({num} preguntas)")
    else:
        print(f"  No pude decidir. Candidatos: {', '.join(candidatos)}")
    print("=" * 60)


def main() -> None:
    if not RUTA_CONOCIMIENTO.exists() or not RUTA_PESOS.exists():
        print("[Error] Ejecuta primero inicializador.py y entrenador.py")
        return

    conocimiento = cargar_conocimiento()
    orden = cargar_orden()

    while True:
        jugar(conocimiento, orden)
        if input("\n  ¿De nuevo? [s/n]: ").lower() not in RESP_SI: break


if __name__ == "__main__":
    main()
