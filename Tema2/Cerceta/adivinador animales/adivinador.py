import yaml
import os
import math

DATOS = "tabla.yaml"

def entropia(candidatos, tabla, atributo):
    n = len(candidatos)
    si = sum(1 for a in candidatos if tabla[a][atributo] == 1)
    no = n - si
    h = 0.0
    for k in (si, no):
        if k > 0:
            p = k / n
            h -= p * math.log2(p)
    return h


def elegir_pregunta(candidatos, tabla, usadas):
    atributos = [a for a in tabla[candidatos[0]] if a not in usadas]
    return max(atributos, key=lambda a: entropia(candidatos, tabla, a), default=None)


def preguntar(atributo):
    texto = f"¿Tu animal tiene o es '{atributo}'?"
    while True:
        r = input(f"{texto} [s/n]: ").strip().lower()
        if r in ("s", "n"):
            return 1 if r == "s" else 0
        print("Responde s o n.")


def jugar(tabla):
    print("\nPiensa en un animal...\n")
    candidatos = list(tabla.keys())
    usadas = set()

    while len(candidatos) > 1:
        atributo = elegir_pregunta(candidatos, tabla, usadas)
        if not atributo:
            break

        usadas.add(atributo)
        respuesta  = preguntar(atributo)
        candidatos = [a for a in candidatos if tabla[a][atributo] == respuesta]

        if not candidatos:
            print("\nNo encontre el animal. Puede que no este en la base de datos.")
            return

        if 1 < len(candidatos) <= 4:
            print(f"  (Candidatos: {', '.join(candidatos)})")

    if len(candidatos) == 1:
        print(f"\n¡Tu animal es el {candidatos[0].upper()}!")
    else:
        print(f"\nNo pude decidir entre: {', '.join(candidatos)}")


# ── Main ──

def main():

    if not os.path.exists(DATOS):
        print(f"No se encontro '{DATOS}'. Ejecuta primero entrenador.py")
        return

    with open(DATOS, "r", encoding="utf-8") as f:
        tabla = yaml.safe_load(f)

    while True:
        jugar(tabla)
        if input("\n¿Otra ronda? [s/n]: ").strip().lower() != "s":
            break

if __name__ == "__main__":
    main()
