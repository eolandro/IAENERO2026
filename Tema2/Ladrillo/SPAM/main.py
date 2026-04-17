from entrenador import entrenador
from detokenizador import detokenizador
from clasificador import clasificador
from evaluador import evaluar

def menu():

    print("\nCLASIFICADOR SPAM")
    print("1. Entrenar sistema")
    print("2. Generar tabla de probabilidades")
    print("3. Clasificar mensajes")
    print("4. Evaluar sistema")
    print("5. Salir")

    return input("Selecciona opcion: ")


if __name__ == "__main__":

    while True:

        op = menu()

        if op == "1":
            entrenador()

        elif op == "2":
            detokenizador()

        elif op == "3":
            clasificador()

        elif op == "4":
            evaluar()

        elif op == "5":
            break

        else:
            print("Opcion invalida")