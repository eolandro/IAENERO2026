import json
import os

def cargador(archivo):
    try:
        with open(archivo, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileExistsError:
        print("El archivo no existe")
        return
    except json.JSONDecodeError:
        print("El archivo no es un json")
        return

def adivina():
    archivo = cargador("figuras.json")
    if not archivo:
        return
    
    preguntas = archivo["preguntas"]
    grafo = archivo["grafo"]

    nodo = "P0"

    print("=========== Piensa en una figura ===========")
    print("=========== Figuras disponibles ============")
    print("Círculo, Elipse, Triángulo Equilátero, Triángulo Isósceles,\
        \nTriángulo Rectángulo, Cuadrado, Rombo, Trapezoide, \
        \nTrapecio, Rectángulo, Romboide, Pentagono, \
        \nHexagono, Heptagono, Octagono, Eneagono, \
        \nDecagono, Endecagono, Dodecagono, Pentagrama, \
        \nHexagrama \n")

    print("================ Adivinador ================")
    print("Responde las preguntas y adivinare la figura que pensaste \n")
    

    while nodo in preguntas:
        txt_pregunta = preguntas[nodo]
        opciones = grafo[nodo]

        print(f"=> {txt_pregunta}")
        teclas_validas = list(opciones.keys())
        print(f"opciones validas {teclas_validas}")

        respuesta = input("R => ").strip().upper()

        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        if respuesta in opciones:
            nodo = opciones[respuesta]
        else:
            print(f"{respuesta} no es una opcion valida. Intenta otra vez \n")

    print(f"{'='*44}")
    print(f"Tu figura es un {nodo}".center(44))
    print(f"{'='*44}")



adivina()