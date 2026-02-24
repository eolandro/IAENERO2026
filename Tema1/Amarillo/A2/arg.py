import argparse
import anlex
from mqv import BoomerVM


parser = argparse.ArgumentParser(
    prog='BoomerInterpreter',
    description='Interpreta el lenguaje de programación Boomer',
    epilog='¡Programa hecho en clases de IA!'
)
parser.add_argument(
    'archivo_codigo',
    type=argparse.FileType('r'),
    help='Archivo con código Boomer a interpretar'
)
args = parser.parse_args()


if args.archivo_codigo:
    lineas = args.archivo_codigo.readlines()
    lineas = [l.strip() for l in lineas if l.strip() and '#' not in l]

    # Crear la máquina virtual y mostrar estado inicial
    ovm = BoomerVM()
    print("=== Estado inicial ===")
    print(ovm)

    PC = 0
    while PC < len(lineas):
        linea = lineas[PC]

        # Validación léxico-sintáctica antes de ejecutar
        if not anlex.procesar_linea(linea):
            print(f"Error de sintaxis en linea {PC}: '{linea}'")
            break

        # Ejecutar instrucción en la VM
        salto = ovm.fetchDecodeExecute(linea)
        print(f"[PC={PC}] {linea}")
        print(ovm)

        # Si Boome murió durante la ejecución, detener
        if not ovm.Vivo:
            print("Boome ha muerto. Fin de la ejecución.")
            break

        # Determinar siguiente PC
        if isinstance(salto, int):
            PC = salto          # Salto condicional tomado
        else:
            PC += 1             # Avance normal


'''
duraznito@drzn:~/IA$ python3 arg.py
usage: BoomerInterpreter [-h] archivo_codigo
BoomerInterpreter: error: the following arguments are required: archivo_codigo
duraznito@drzn:~/IA$ python3 arg.py codigo_boome
R1: 0
R2: 0
R3: 0
['B', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
Ultima Instruccion: 
Instruccion Actual: 
Vivo: True
--------------------------------------------------
Traceback (most recent call last):
  File "/home/duraznito/IA/arg.py", line 21, in <module>
    R = anlex.procesar_linea(linea)
        ^^^^^
NameError: name 'anlex' is not defined. Did you mean: 'anext'?
duraznito@drzn:~/IA$ 
'''