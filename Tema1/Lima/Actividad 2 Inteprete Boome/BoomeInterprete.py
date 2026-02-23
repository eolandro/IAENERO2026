import argparse
import andlex
from vm import BoomeVM

parser = argparse.ArgumentParser(
    prog="BoomeInterprete",
    description="Ejecuta un archivo de codigo para boome",
    epilog="Este programa fue hecho para la clase de IA",
)

parser.add_argument(
    "archivo_codigo",
    type=argparse.FileType("r"),
    help="Ejemplo:\n  BoomeInterprete.py codigo.boome",
)

args = parser.parse_args()

ovm = BoomeVM()
lineas = []
for linea in args.archivo_codigo:
    linea = linea.split("#", 1)[0].strip()
    linea = linea.replace("=", " = ").replace("+", " + ").replace("-", " - ")
    if linea:
        lineas.append(linea)

while ovm.contadorlineas < len(lineas):
    linea = lineas[ovm.contadorlineas]
    if not andlex.procesar_linea(linea):
        print(f"Error en la linea {ovm.contadorlineas + 1}:")
        print(f"  {linea}")
        break
    ovm.fetchDecodeExecute(linea)
    print(ovm)
    ovm.contadorlineas += 1

