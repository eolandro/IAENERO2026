import json
import math

def cargar_probabilidades():
    try:
        with open("tablaProbabilidades.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("Error: No se encontró tablaProbabilidades.json")
        return None


def cargar_mensajes():
    try:
        with open("mensajesNuevos.txt", "r", encoding="utf-8") as archivo:
            return [line.strip() for line in archivo if line.strip()]
    except FileNotFoundError:
        print("Error: No se encontró mensajesNuevos.txt")
        return []


def obtener_palabras():
    return [
        "el","la","los","las","de","del","y","en","a","que","para","con","por",
        "un","una","es","tu","su","al","lo","como","más","pero",
        "the","and","to","of","in","your","now",
        "nao","não","para","com","por","uma","um","agora","e"
    ]


def limpiar_texto(texto):
    texto = texto.lower()
    limpio = ""

    for caracter in texto:
        if caracter.isalpha() or caracter == " ":
            limpio += caracter
        else:
            limpio += " "

    return limpio

def tokenizar(texto, palabras_filtrar):
    texto = limpiar_texto(texto)
    palabras = texto.split()

    tokens = []
    for palabra in palabras:
        if palabra not in palabras_filtrar:
            tokens.append(palabra)

    return tokens


def clasificar_mensaje(tokens, probabilidades):

    # Usamos logaritmos para evitar que números muy pequeños se hagan 0
    log_spam = 0
    log_no_spam = 0

    for palabra in tokens:

        # Si la palabra no existe, usamos un valor muy pequeño
        p_spam = probabilidades["spam"].get(palabra, 0.000001)
        p_no_spam = probabilidades["noSpam"].get(palabra, 0.000001)

        # Sumamos logaritmos (equivale a multiplicar probabilidades)
        log_spam += math.log(p_spam)
        log_no_spam += math.log(p_no_spam)

    # El método de consenso que utilicé fue comparación directa 
    # de probabilidades acumuladas. Cada palabra aporta evidencia y 
    # al final se decide la clase con mayor probabilidad total
    if log_spam > log_no_spam:
        return "spam"
    else:
        return "noSpam"


def clasificar_mensajes(mensajes, probabilidades, palabras_filtrar):

    resultados = []

    for mensaje in mensajes:
        tokens = tokenizar(mensaje, palabras_filtrar)

        tipo = clasificar_mensaje(tokens, probabilidades)

        resultados.append({
            "mensaje": mensaje,
            "clasificacion": tipo
        })

    return resultados


def guardar_resultados(resultados):

    with open("resultadosClasificacion.json", "w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, indent=4, ensure_ascii=False)

    print("\nClasificación completada, se generó resultadosClasificacion.json")



def main():

    probabilidades = cargar_probabilidades()
    if probabilidades is None:
        return

    mensajes = cargar_mensajes()
    if not mensajes:
        return

    palabras_filtrar = obtener_palabras()

    resultados = clasificar_mensajes(mensajes, probabilidades, palabras_filtrar)

    guardar_resultados(resultados)


if __name__ == "__main__":
    main()