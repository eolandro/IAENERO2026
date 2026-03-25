import os
import json
import yaml


"""
##R001##
##10##
Descripción: Generar programa "inicializador"
Restricciones: NA.
"""


BASE_DIR = os.path.dirname(__file__)
RUTA_CONFIG = os.path.join(BASE_DIR, "config.yaml")
RUTA_ANIMALES = os.path.join(BASE_DIR, "animales.json")


def main():
    print("\n" + "=" * 50)
    print(" R001: INICIALIZADOR")
    print("=" * 50)

    archivo_config = open(RUTA_CONFIG, "r", encoding="utf-8")
    config = yaml.safe_load(archivo_config)
    archivo_config.close()

    caracteristicas = []
    pesos = {}
    preguntas = {}
    for nombre_caracteristica, info in config["caracteristicas"].items():
        caracteristicas.append(nombre_caracteristica)
        pesos[nombre_caracteristica] = info["peso"]
        preguntas[nombre_caracteristica] = info["pregunta"]

    animales = []
    for nombre_animal, valores in config["animales"].items():
        puntaje = 0
        for nombre_caracteristica in caracteristicas:
            valor = valores.get(nombre_caracteristica, 0)
            puntaje = puntaje + (valor * pesos[nombre_caracteristica])

        registro = {
            "nombre": nombre_animal,
            "caracteristicas": valores,
            "puntaje": puntaje,
        }
        animales.append(registro)

    animales_ordenados = animales.copy()
    n = len(animales_ordenados)
    for i in range(n):
        for j in range(0, n - i - 1):
            if animales_ordenados[j]["puntaje"] < animales_ordenados[j + 1]["puntaje"]:
                temp = animales_ordenados[j]
                animales_ordenados[j] = animales_ordenados[j + 1]
                animales_ordenados[j + 1] = temp

    print("\nTabla (animal y puntaje):")
    for animal in animales_ordenados:
        print("- " + animal["nombre"] + " -> " + str(animal["puntaje"]))

    salida = {
        "caracteristicas": caracteristicas,
        "pesos": pesos,
        "preguntas": preguntas,
        "animales": animales,
    }

    archivo_salida = open(RUTA_ANIMALES, "w", encoding="utf-8")
    json.dump(salida, archivo_salida, ensure_ascii=False, indent=2)
    archivo_salida.close()


if __name__ == "__main__":
    main()
