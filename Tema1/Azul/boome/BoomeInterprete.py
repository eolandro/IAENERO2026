import argparse
import anlex
from vm import BoomeVM

# Configuracion del parser de argumentos
parser = argparse.ArgumentParser(
    prog='BoomeInterprete',
    description='Ejecuta un archivo de codigo para Boome',
    epilog='Este programa fue hecho para la clase de IA'
)
parser.add_argument(
    'archivo_codigo',
    type=argparse.FileType('r'),
    help="Ejemplo: BoomeInterprete.py codigo.boome",
)
args = parser.parse_args()

if args.archivo_codigo:
    lineas_raw = args.archivo_codigo.readlines()

    # Filtrar comentarios y lineas vacias
    lineas = []
    for linea in lineas_raw:
        limpia = linea.strip()
        # Ignorar lineas vacias y comentarios
        if not limpia or limpia.startswith("#"):
            continue
        lineas.append(limpia)

    # Validacion lexica/sintactica previa a la ejecucion
    errores = False
    for i, linea in enumerate(lineas):
        if not anlex.procesar_linea(linea):
            print(f"Error en linea {i + 1}: {linea}")
            errores = True

    # Si hay errores, no se ejecuta el programa
    if errores:
        print("sintax-error")
    else:
        # Tokenizar cada linea para la VM
        programa = [linea.split() for linea in lineas]
        # Crear la VM y cargar el programa
        ovm = BoomeVM()
        ovm.programa = programa
        # Ejecutar instruccion por instruccion
        ovm.ejecutar()
