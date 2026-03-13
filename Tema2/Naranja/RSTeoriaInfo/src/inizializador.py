# Inicializador del programa de animals.
import json


class Inizializador:
    def __init__(self):
        self.animales = []

    def agregar_animal(self, animal, caracteristica):
        self.animales.append({"animal": animal, "caracteristica": caracteristica})

    # utf8
    def repetidos(self, anica):
        for registro in self.animales:
            if registro["animal"] == anica or registro["caracteristica"] == anica:
                print(
                    "El animal o la característica ya existe en el registro. No se agregará."
                )
                return True
        return False

    def mostrar_animales(self):
        for animal in self.animales:
            print(
                f"Animal: {animal['animal']}, Caracteristica: {animal['caracteristica']}"
            )

    def crear_archivo_json(self, nombre_archivo):
        with open(nombre_archivo, "w") as archivo:
            json.dump(self.animales, archivo, indent=4)


def validador(tipo, mensaje):
    while True:
        try:
            valor = tipo(input(mensaje))
            return valor
        except ValueError:
            print(f"Por favor, ingresa un valor válido del tipo {tipo.__name__}.")


objAnimales = Inizializador()
cantidad = validador(int, "¿Cuántos animales deseas agregar? ")
for i in range(cantidad):
    while True:
        animal = input(f"Ingrese el nombre del animal #{i + 1}: ")
        if not objAnimales.repetidos(animal):
            break
    while True:
        caracteristica = input(f"Ingrese la característica del animal #{i + 1}: ")
        if not objAnimales.repetidos(caracteristica):
            break
    objAnimales.agregar_animal(animal, caracteristica)
print("\nRegistro de Animales:")
objAnimales.mostrar_animales()
nombre_archivo = "ver1.json"
objAnimales.crear_archivo_json(nombre_archivo)
print(f"Archivo '{nombre_archivo}' creado exitosamente con el registro de animales.")

