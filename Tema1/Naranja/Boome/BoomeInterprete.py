import argparse
import anlex
from vm import BoomeVM
parser = argparse.ArgumentParser(
    prog = 'BoomeInterprete',
    description = 'Ejecuta un serchivo con codigo ',
    epilog = 'Este programa fue hecho para la calse de IA'
);

parser.add_argument(
    'archivo_codigo',
    type = argparse.FileType('r'),
    help = 'Ejemplo: \nBoomeInterprete.py codigo.boome'
);
#Nombre
#Seocupa pra abrir un archivo en modo de lectura
#Se le esta dando el tipo de sintaxtis que debe tener

#Si llegue aqui es porque la linea de código existe
args = parser.parse_args();
if args.archivo_codigo:
    lineas = args.archivo_codigo.readlines();
    lineas = [l.strip() for l in lineas if not '#' in l];#Se quita todos los espacios en blancos que se pueda tener por tener una compresion de listas. Lo ultimo es para ignorar los comentarios
    ovm = BoomeVM();
    print( ovm );
    #Código anterior sin saltos
    """
    for linea in lineas:
        R=anlex.procesar_linea(linea)
        if not R:
            print(f"Error en la linea \n{linea}");
            break;
        ovm.fetchDecodeExecute(linea);
        print(ovm);
    """
    #Version 2 con saltos
    PC = 0 # Program Counter (Contador de Programa)
    while PC < len(lineas):
        linea = lineas[PC];
        # Validacion del anlex
        if not anlex.procesar_linea(linea):
            print( f"Error de sintaxis en linea {PC}: {linea}" );
            break
        # Ejecutamos y esperamos respuesta (¿Hubo salto?)
        salto = ovm.fetchDecodeExecute(linea);
        print( ovm );
        # Lógica del Control de Flujo
        if isinstance(salto, int):
            PC = salto;#Saltar
        else:
            PC += 1;#Siguiente linea
#python3 BoomeInterprete.py codigo.boome
