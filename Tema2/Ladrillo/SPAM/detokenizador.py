import yaml
import os
from collections import defaultdict

def detokenizador():

    if not os.path.exists("entrenamiento.yml"):
        print("ERROR: No existe entrenamiento.yml")
        print("Primero debes ejecutar la opcion 1 (Entrenar sistema)")
        return

    stopwords = ["de","la","el","los","las","y","o","en","con","para","por","a"]

    spam = defaultdict(int)
    ham = defaultdict(int)

    with open("entrenamiento.yml") as f:
        data = yaml.safe_load(f)

    for item in data["mensajes"]:

        mensaje = item["texto"].lower()
        etiqueta = item["etiqueta"]

        tokens = mensaje.split()
        tokens = [t for t in tokens if t not in stopwords]

        for t in tokens:

            if etiqueta == "spam":
                spam[t] += 1
            else:
                ham[t] += 1

    tabla = {}

    palabras = set(list(spam.keys()) + list(ham.keys()))

    for p in palabras:
        tabla[p] = {
            "spam": spam[p],
            "ham": ham[p]
        }

    with open("probabilidades.yml", "w") as f:
        yaml.dump(tabla, f)

    print("Tabla de probabilidades generada correctamente")