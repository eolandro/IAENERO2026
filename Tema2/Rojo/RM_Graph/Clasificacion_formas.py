import yaml
import os

carpeta = os.path.dirname(__file__)
archivo = open(carpeta + "/uso.yaml", encoding="utf-8")
datos = yaml.safe_load(archivo)
archivo.close()

grafo = datos["grafo"]
nodos = grafo["nodos"]

print("\nADIVINADOR DE FIGURAS ")
print("Piensa en una figura y responde las preguntas:\n")

nodo_actual = grafo["inicio"]

while True:

    nodo = nodos.get(nodo_actual)

    if nodo is None:
        print("\nLa figura es: " + nodo_actual)
        break

    pregunta = nodo["pregunta"]
    transiciones = nodo["transiciones"]

    respuesta = input(pregunta + " ").strip().lower()

    if respuesta in transiciones:
        nodo_actual = transiciones[respuesta]
    else:
        print("Respuesta no válida. Intenta nuevamente.")
    
    