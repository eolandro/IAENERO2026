import argparse
import anlex
from vm import BoomeVM

parser = argparse.ArgumentParser(
    prog='BoomeInterprete',
    description='Ejecuta un archivo de código para boome',
    epilog='Este programa fue hecho para la clase IA 2026'
)

parser.add_argument(
    'archivo_codigo',
    type=argparse.FileType('r'),
    help='Ejemplo:\nBoomeInterprete.py codigo.boome'
)

args = parser.parse_args()

if args.archivo_codigo:
    lineas = args.archivo_codigo.readlines()
    # Hacer copia de las lineas
    # Limpiar para procesar
    lineas_procesar = []


    for i, l in enumerate(lineas):
        # ignorar comentarios y quitar espacios en blanco
        # el split divide la lista en dos al encontrar el caracter #
        #  el [0] indica que tomara lo que estaba antes del #
        l_limpia = l.split('#')[0].strip()
        if l_limpia:
            lineas_procesar.append((i, l_limpia))

    # EJEMPLO DE LINEA LIMPIA (0, "movi")
    ovm = BoomeVM()
    print("\n ESTADO INICIAL ")
    print(ovm)

    contador = 0

    while contador < len(lineas_procesar):


        #  contador=0  idx = 0, linea = 'movi'
        idx, linea = lineas_procesar[contador]
        print(f"\n--- Ejecutando línea (0 based)  {idx}: {linea}  ---")
        print(f"--- Ejecutando línea (1 based)  {idx + 1}: {linea}  ---")


        # Parsear la linea con anlex
        instruccion = anlex.procesar_linea(linea)

        if not instruccion:
            print(f"ERROR de sintaxis en la linea  (0 based) {idx}: {linea}")
            print(f"ERROR de sintaxis en la linea (1 based){idx + 1 }: {linea}")
            break


        # True podemos ejecutar la siguiente linea sin problemas
        # Si es difeente de uno nos da el numero de linea a la cual queremos volver o en otras
        # palabras el destino

        siguiente = ovm.fetchDecodeExecute(instruccion)

        # MOSSTRAR ESTADO DESPUES DE EJECUTAR
        print(ovm)

        # isinstance(objeto, tipo)
        if isinstance(siguiente, bool):
            contador += 1  # Siguiente instrucción normalmente
        # ES UN SATLO
        else:
            contador = siguiente


        if not ovm.Vivo:
            print("Boome ha muerto :( DETENIENDO EJECUCION")
            break

    print("\n--- EJECUCIÓN FINALIZADA ---")









