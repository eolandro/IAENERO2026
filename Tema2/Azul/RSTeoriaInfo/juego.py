#Juego tipo Akinator para adivinar animales
#Usa entropía de información para elegir la pregunta óptima cada turno

from inicializador import ANIMALES, PREGUNTAS
from entrenador import animales_con_caracteristica, mejor_pregunta


def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    print("=" * 55)
    print("         ADIVINA EL ANIMAL 🐾")
    print("=" * 55)
    print("  Piense en uno de los 12 animales de la lista.")
    print("  Responda Si (s) o No (n) a cada pregunta.")
    print("  ¡Intentaré adivinarlo con el menor número")
    print("  de preguntas posible!")
    print("=" * 55)


def mostrar_animales():
    print("\n  Animales disponibles:\n")
    animales = [
        "Perro", "Gato", "Hámster", "Sapo", "Caballo", "Gallina",
        "Quetzal", "Hurón", "Castor", "Lobo", "Vaca", "Foca"
    ]
    for i, a in enumerate(animales, 1):
        print(f"   {i:2}. {a}")
    print()


def pedir_respuesta(pregunta: str, num_pregunta: int, total_candidatos: int) -> bool:
    while True:
        print(f"\n  Pregunta {num_pregunta}  ({total_candidatos} animal(es) posible(s))")
        print(f"  {pregunta}")
        resp = input("  Tu respuesta [s/n]: ").strip().lower()
        if resp in ('s', 'si', 'sí', 'yes', 'y', '1'):
            return True
        elif resp in ('n', 'no', '0'):
            return False
        else:
            print("  ⚠️ Entrada no valida. Por favor responda 's' o 'n'.")


def jugar():
    limpiar_pantalla()
    banner()
    mostrar_animales()

    input("  Presiona ENTER cuando hayas pensado en un animal...")
    limpiar_pantalla()
    banner()

    candidatos = list(ANIMALES)
    ya_preguntadas = set()
    num_pregunta = 0

    print("\n  ¡Empecemos! Responde honestamente \n")

    while len(candidatos) > 1:
        carac = mejor_pregunta(candidatos, ya_preguntadas)

        if carac is None:
            break

        num_pregunta += 1
        ya_preguntadas.add(carac)

        respuesta = pedir_respuesta(PREGUNTAS[carac], num_pregunta, len(candidatos))

        valor = 1 if respuesta else 0
        candidatos = animales_con_caracteristica(carac, valor, candidatos)


        if len(candidatos) <= 3:
            print(f"\n  Candidatos restantes: {', '.join(candidatos)}")

#Resultado final
    print("\n" + "=" * 55)
    if len(candidatos) == 1:
        animal = candidatos[0]
        print(f"\n  El sistema ha determinado que su animal es:\n")
        print(f"            {animal.upper()}\n")
        print(f"  Identificado en {num_pregunta} pregunta(s).")

    print("=" * 55)


def main():
    while True:
        jugar()
        print()
        otra = input("  ¿Deseas jugar de nuevo? [s/n]: ").strip().lower()
        if otra not in ('s', 'si', 'sí', 'yes', 'y'):
            print("\n  Hasta luego. 🐾\n")
            break
        limpiar_pantalla()


if __name__ == "__main__":
    main()
