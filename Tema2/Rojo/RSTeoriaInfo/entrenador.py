import os
import json


"""
##R002##
##10##
Descripción: Generar programa "entrenador"
Restricciones: NA.
"""


BASE_DIR = os.path.dirname(__file__)
RUTA_ANIMALES = os.path.join(BASE_DIR, "animales.json")
RUTA_PREGUNTAS = os.path.join(BASE_DIR, "preguntas_ordenadas.json")


def main():
    print("\n" + "=" * 50)
    print(" R002: ENTRENADOR")
    print("=" * 50)

    if not os.path.exists(RUTA_ANIMALES):
        print("No existe animales.json. Ejecuta primero inicializador.py")
        return

    archivo = open(RUTA_ANIMALES, "r", encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()

    detalle = []
    for caracteristica in datos["caracteristicas"]:
        registro = {
            "caracteristica": caracteristica,
            "pregunta": datos["preguntas"][caracteristica],
            "peso": datos["pesos"][caracteristica],
        }
        detalle.append(registro)

    n = len(detalle)
    for i in range(n):
        for j in range(0, n - i - 1):
            if detalle[j]["peso"] < detalle[j + 1]["peso"]:
                temp = detalle[j]
                detalle[j] = detalle[j + 1]
                detalle[j + 1] = temp

    print("\n#   Caracteristica   Peso  Pregunta")
    print("-" * 88)

    posicion = 1
    for dato in detalle:
        numero = str(posicion)
        if len(numero) < 3:
            numero = numero + (" " * (3 - len(numero)))

        nombre = dato["caracteristica"]
        if len(nombre) < 14:
            nombre = nombre + (" " * (14 - len(nombre)))

        peso_texto = str(dato["peso"])
        if len(peso_texto) < 6:
            peso_texto = (" " * (6 - len(peso_texto))) + peso_texto

        print(numero + " " + nombre + " " + peso_texto + "  " + dato["pregunta"])
        posicion += 1

    orden_preguntas = []
    for registro in detalle:
        orden_preguntas.append(registro["caracteristica"])

    salida = {
        "orden_preguntas": orden_preguntas,
        "detalle": detalle,
        "pesos": datos["pesos"],
    }

    archivo_salida = open(RUTA_PREGUNTAS, "w", encoding="utf-8")
    json.dump(salida, archivo_salida, ensure_ascii=False, indent=2)
    archivo_salida.close()


if __name__ == "__main__":
    main()
