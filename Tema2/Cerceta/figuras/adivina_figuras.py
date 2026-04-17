from ruamel.yaml import YAML

def cargar_datos(nombre="figuras.yaml"):
    yaml = YAML()
    with open(nombre, "r", encoding="utf-8") as archivo:
        return yaml.load(archivo)


def construir_arbol(lista_arbol):
    arbol = {}
    i = 0
    while i < len(lista_arbol):
        origen = lista_arbol[i][0]
        respuesta = str(lista_arbol[i][1]).upper()
        destino = lista_arbol[i][2]

        arbol[origen] = arbol.get(origen, {})
        arbol[origen][respuesta] = destino
        i += 1

    return arbol


def mostrar_figuras(data):
    padres = set(map(lambda x: x[0], data["arbol"]))
    terminales = list(
        map(
            lambda x: x[1],
            filter(lambda x: x[0] not in padres, data["preguntas"])
        )
    )

    print("\nFiguras geometricas posibles:")
    i = 0
    while i < len(terminales):
        print("->", terminales[i])
        i += 1


def adivinador():
    data = cargar_datos()
    preguntas = dict(data["preguntas"])
    arbol = construir_arbol(data["arbol"])

    mostrar_figuras(data)

    actual = "P0"

    while True:
        texto = preguntas.get(actual)
        opciones = list(arbol.get(actual, {}).keys())

        if len(opciones) == 0:
            print("\n¡Tu figura es un:", texto + "!")
            break

        print("\n" + texto)
        print("Opciones a elegir:", opciones)

        respuesta = input("Respuesta: ").strip().upper()
        siguiente = arbol.get(actual, {}).get(respuesta)

        if siguiente is None:
            print("La respuesta no válida. Intenta de nuevo.")
            continue

        actual = siguiente

        if actual not in preguntas:
            print("Hay un nodo en el árbol que no existe en preguntas:", actual)
            break


if __name__ == "__main__":
    adivinador()