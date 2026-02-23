import argparse
import anlex
from vm import BoomeVM

parse = argparse.ArgumentParser(
    prog="BoomeInterprete",
    description="Ejecuta un archivo de codigo para boome",
    epilog="Este programa fue hecho para la clase de IA"
)

parse.add_argument(
    "archivo_codigo",
    type=argparse.FileType('r'),
    help="Ejemplo:\n BoomeInterprete.py codigo.boome"
)

args = parse.parse_args()

if args.archivo_codigo:
    lineas = args.archivo_codigo.readlines()

   
    lineas = [
        l.strip().replace("\t", " ").strip()
        for l in lineas
        if l.strip() and '#' not in l
    ]

    ovm = BoomeVM()
    print(ovm)

    pc = 0  # ← program counter

    while pc < len(lineas) and ovm.Vivo:

        linea = lineas[pc].strip() 

        R = anlex.procesar_linea(linea)
        if not R:
            print(f"Error en la línea: {linea}")
            break

        salto = ovm.fetchDecodeExecute(linea)

        print(ovm)

        if salto is not None:
            pc = salto
        else:
            pc += 1