import argparse
import anlex
from vm import BoomeVM

parser = argparse.ArgumentParser()
parser.add_argument("archivo", type=argparse.FileType("r"))
args = parser.parse_args()

lineas = [l.strip() for l in args.archivo if l.strip()]

vm = BoomeVM()
print(vm)

cont = 0
while cont < len(lineas) and vm.Vivo:

    instruccion = lineas[cont]
    es_valida = anlex.procesar_linea(instruccion)

    if not es_valida:
        print("Error sintáctico:", instruccion)
        break

    salto = vm.ejecutar(instruccion)
    print(vm)

    if salto is not None:
        cont = salto
    else:
        cont += 1

if not vm.Vivo:
    print("Boome ha dejado de funcionar.")