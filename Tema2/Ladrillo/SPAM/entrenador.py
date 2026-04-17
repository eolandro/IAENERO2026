import yaml

def entrenador():

    data = {"mensajes": []}

    for i in range(10):

        texto = input("Mensaje: ")
        etiqueta = input("spam o ham: ")

        data["mensajes"].append({
            "texto": texto,
            "etiqueta": etiqueta
        })

    with open("entrenamiento.yml", "w") as f:
        yaml.dump(data, f, allow_unicode=True)