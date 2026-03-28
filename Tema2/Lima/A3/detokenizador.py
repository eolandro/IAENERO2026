import json

def cargar_datos():
    try:
        with open("mensajesEtiquetados.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        print("Error: No se encontró mensajesEtiquetados.json")
        return None

def obtener_palabras():
    return [
        "el","la","los","las","de","del","y","en","a","que","para","con","por",
        "un","una","es","tu","su","al","lo","como","más","pero",
        "the","and","to","of","in","your","now",
        "nao","não","para","com","por","uma","um","agora","e"
    ]

def limpiar_texto(texto):
    texto = texto.lower()
    # aquí creo una variable vacía donde iré guardando el texto limpio carácter por carácter
    limpio = ""
    for caracter in texto:
        # aquí verifico si el carácter es una letra (a-z) o un espacio
        if caracter.isalpha() or caracter == " ":
            limpio += caracter
        else:
            limpio += " "   # reemplaza símbolos por espacio

    return limpio


def tokenizar(texto, palabras_filtrar):
    texto = limpiar_texto(texto)
    # aquí separo el texto en palabras (tokens) usando los espacios
    palabras = texto.split()

    tokens = []
    for palabra in palabras:
        if palabra not in palabras_filtrar:
            tokens.append(palabra)

    return tokens


def contar_palabras(datos, palabras_filtrar):

    conteo = {
        "spam": {},
        "noSpam": {}
    }

    total_palabras = {
        "spam": 0,
        "noSpam": 0
    }

    for item in datos:
        mensaje = item["mensaje"]
        tipo = item["tipo"]

        tokens = tokenizar(mensaje, palabras_filtrar)

        for token in tokens:

            # Inicializar si no existe
            if token not in conteo[tipo]:
                conteo[tipo][token] = 0

            conteo[tipo][token] += 1
            total_palabras[tipo] += 1

    return conteo, total_palabras


def calcular_probabilidades(conteo, total_palabras):

    probabilidades = {
        "spam": {},
        "noSpam": {}
    }

    for tipo in conteo:
        for palabra in conteo[tipo]:

            frecuencia = conteo[tipo][palabra]

            if total_palabras[tipo] == 0:
                prob = 0
            else:
                prob = frecuencia / total_palabras[tipo]

            probabilidades[tipo][palabra] = prob

    return probabilidades


def guardar_probabilidades(probabilidades):

    with open("tablaProbabilidades.json", "w", encoding="utf-8") as archivo:
        json.dump(probabilidades, archivo, indent=4, ensure_ascii=False)

    print("\nTabla de probabilidades generada correctamente")



def main():

    datos = cargar_datos()
    if datos is None:
        return

    palabras_filtrar = obtener_palabras()

    conteo, total_palabras = contar_palabras(datos, palabras_filtrar)

    probabilidades = calcular_probabilidades(conteo, total_palabras)

    guardar_probabilidades(probabilidades)
    


if __name__ == "__main__":
    main()