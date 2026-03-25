import argparse
import os
import anlex
from vm import BoomeVM
from map_loader import cargar_mapa_desde_archivo

parser = argparse.ArgumentParser(
    prog="BoomeInterpreter",
    description="Ejecuta un archivo de codigo para Boome",
    epilog="Proyecto escolar: interprete y maquina virtual"
)

parser.add_argument(
    "archivo_codigo",
    nargs="?",
    default="test_bayes.boomie",
    help="Ejemplo:\n  boomieinterpreter test_bayes.boomie"
)

parser.add_argument(
    "--mapa",
    type=str,
    default="mapa_bayes.txt",
    help="Ruta al archivo de mapa base (5x10). Se insertan 3 bombas aleatorias por corrida."
)

args = parser.parse_args()


def resolver_ruta_local(ruta):
    if os.path.isabs(ruta):
        return ruta
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, ruta)


def limpiar_linea(linea):
    # Elimina comentarios con # y recorta espacios
    if "#" in linea:
        linea = linea.split("#", 1)[0]
    return linea.strip()


if args.archivo_codigo:
    try:
        ruta_codigo = resolver_ruta_local(args.archivo_codigo)
        ruta_mapa = resolver_ruta_local(args.mapa)

        with open(ruta_codigo, "r", encoding="utf-8") as archivo_codigo:
            lineas_raw = archivo_codigo.readlines()

        lineas = [limpiar_linea(l) for l in lineas_raw]
        lineas = [l for l in lineas if l]

        ovm = BoomeVM()

        mapa = cargar_mapa_desde_archivo(ruta_mapa)
        ovm.cargar_mapa(mapa)
        ovm.insertar_bombas_aleatorias(3)

        print(ovm)

        pc = 0
        n = len(lineas)

        # Para evitar ciclos infinitos
        MAX_STEPS = 500
        steps = 0

        while pc < n and ovm.Vivo and steps < MAX_STEPS:
            steps += 1
            linea = lineas[pc]

            # Validacion lexica/sintactica antes de ejecutar
            ok = anlex.procesar_linea(linea)
            if not ok:
                ovm.ultimaInstruccion = ovm.instruccionActual
                ovm.instruccionActual = linea
                ovm.Vivo = False
                print(ovm)
                break

            # ✅ La VM resuelve TODO (incluidos los saltos) y regresa el nuevo pc
            pc = ovm.step(linea, pc, n)

            print(ovm)

        if steps >= MAX_STEPS:
            print("Fin: limite de pasos alcanzado (posible ciclo infinito).")

        if not ovm.Vivo:
            print("Boome murio. Fin de la ejecucion.")

    except ValueError as ex:
        print(f"Error controlado de mapa: {ex}")
    except Exception:
        # En entrega escolar se evita mostrar traceback
        print("Error controlado: el programa termino sin poder ejecutar el archivo.")