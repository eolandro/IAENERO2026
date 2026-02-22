import argparse
import anlex
from vm import BoomeVM
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument("Archivo")
args = parser.parse_args()

programa = []
with open(args.Archivo, "r") as f:
    for linea in f:
        tokens = anlex.procesar_linea(linea)
        if tokens:
            programa.append(tokens)

vm = BoomeVM()

while vm.PC < len(programa) and vm.estado == "Activo":
    # Descomenta la siguiente linea si quieres ver animacion:
    # os.system('cls' if os.name == 'nt' else 'clear')
    
    instruccion = programa[vm.PC]
    print(f"\n>>> Paso {vm.PC}: {instruccion}")
    vm.ejecutar(instruccion)
    vm.PC += 1
    print(vm)
    time.sleep(0.2)

print(f"Fin del programa. Resultado: {vm.estado}")