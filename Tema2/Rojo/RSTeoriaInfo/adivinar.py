import os
import json


"""
##R003##
##10##
Descripción: Adivinar el animal con el minimo de preguntas en el programa "adivinar"
Restricciones: NA.
"""


BASE_DIR = os.path.dirname(__file__)
RUTA_ANIMALES = os.path.join(BASE_DIR, "animales.json")
RUTA_PREGUNTAS = os.path.join(BASE_DIR, "preguntas_ordenadas.json")


def main():
    print("\n" + "=" * 50)
    print(" R003: ADIVINAR")
    print("=" * 50)

    if not os.path.exists(RUTA_ANIMALES):
        print("No existe animales.json. Ejecuta primero inicializador.py")
        return
    if not os.path.exists(RUTA_PREGUNTAS):
        print("No existe preguntas_ordenadas.json. Ejecuta primero entrenador.py")
        return

    archivo_animales = open(RUTA_ANIMALES, "r", encoding="utf-8")
    datos_animales = json.load(archivo_animales)
    archivo_animales.close()

    archivo_preguntas = open(RUTA_PREGUNTAS, "r", encoding="utf-8")
    datos_preguntas = json.load(archivo_preguntas)
    archivo_preguntas.close()

    nombres = []
    for animal in datos_animales["animales"]:
        nombres.append(animal["nombre"])

    print("Animales disponibles: " + str(nombres))

    while True:
        animales = datos_animales["animales"]
        pesos = datos_animales["pesos"]
        preguntas = datos_animales["preguntas"]
        orden = datos_preguntas["orden_preguntas"]

        puntaje_usuario = 0
        preguntas_hechas = 0

        print("\nPiensa en un animal de la lista y responde con s/n.\n")

        for caracteristica in orden:
            print("Pregunta " + str(preguntas_hechas + 1) + ":")

            while True:
                resp = input("  " + preguntas[caracteristica] + " (s/n): ").strip().lower()
                if resp in ("s", "si", "sí"):
                    puntaje_usuario += pesos[caracteristica]
                    preguntas_hechas += 1
                    break
                if resp in ("n", "no"):
                    preguntas_hechas += 1
                    break
                print("  Responde con s o n.")

        mejor = None
        mejor_diferencia = None
        for animal in animales:
            diferencia = abs(animal["puntaje"] - puntaje_usuario)
            if mejor is None or diferencia < mejor_diferencia:
                mejor = animal
                mejor_diferencia = diferencia

        print("=" * 48)
        print("Puntaje total obtenido: " + str(puntaje_usuario))
        print("Animal probable: " + mejor["nombre"].upper())
        print("Puntaje del animal: " + str(mejor["puntaje"]))
        print("Diferencia: " + str(mejor_diferencia))
        print("Preguntas hechas: " + str(preguntas_hechas) + " de " + str(len(orden)))
        print("=" * 48)

        otra = input("\nQuieres jugar de nuevo? (s/n): ").strip().lower()
        if otra not in ("s", "si", "sí"):
            print("Fin del programa.")
            break


if __name__ == "__main__":
    main()
