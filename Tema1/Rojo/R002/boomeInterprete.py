import argparse
import anlex
from vm import BoomeVM

parser = argparse.ArgumentParser(
    prog="BoomeInterpreter",
    description="Ejecuta un archivo de codigo para Boome",
    epilog="Proyecto escolar: interprete y maquina virtual"
)

parser.add_argument(
    "archivo_codigo",
    type=argparse.FileType("r"),
    help="Ejemplo:\n  python boomeInterprete.py codigo.boomie"
)

args = parser.parse_args()


def limpiar_linea(linea):
    # Elimina comentarios con # y recorta espacios
    if "#" in linea:
        linea = linea.split("#", 1)[0]
    return linea.strip()


def valor_token(tok, ovm):
    # Convierte un token a valor entero:
    # - r0..r3 -> valor del registro
    # - 0x..   -> numero hexadecimal
    try:
        if tok.startswith("r") and len(tok) == 2 and tok[1] in ovm.R:
            return ovm.R[tok[1]]
        if tok.startswith("0x"):
            return int(tok, 16)
    except Exception:
        return None
    return None


if args.archivo_codigo:
    try:
        lineas_raw = args.archivo_codigo.readlines()
        lineas = [limpiar_linea(l) for l in lineas_raw]
        lineas = [l for l in lineas if l]

        ovm = BoomeVM()

        # Bombas fijas para las pruebas (fila, columna)
        bombas = [
            (0, 2),
            (1, 4),
            (2, 7),
            (4, 0),
        ]
        for f, c in bombas:
            if 0 <= f < len(ovm.Mapa) and 0 <= c < len(ovm.Mapa[f]):
                ovm.Mapa[f][c] = "*"

        print(ovm)

        pc = 0
        n = len(lineas)

        # Para evitar ciclos infinitos en caso de saltos mal definidos
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

            tokens = linea.split(" ")
            tokens = [t for t in tokens if t]

            # Saltos: salta_igual X Y Z / salta_dif X Y Z
            if len(tokens) == 4 and tokens[0] in ["salta_igual", "salta_dif"]:
                op, x, y, z = tokens

                vx = valor_token(x, ovm)
                vy = valor_token(y, ovm)
                vz = valor_token(z, ovm)

                ovm.ultimaInstruccion = ovm.instruccionActual
                ovm.instruccionActual = linea

                # Si algun token no es valido, se detiene la ejecucion
                if vx is None or vy is None or vz is None:
                    ovm.Vivo = False
                    print(ovm)
                    break

                hacer_salto = (vx == vy) if op == "salta_igual" else (vx != vy)

                if hacer_salto:
                    # Z se usa como destino (linea dentro del archivo)
                    if vz < 0 or vz >= n:
                        ovm.Vivo = False
                        print(ovm)
                        break
                    pc = vz
                else:
                    pc += 1

                print(ovm)
                continue

            # Resto de instrucciones: las ejecuta la VM
            ovm.fetchDecodeExecute(linea)
            print(ovm)
            pc += 1

        if steps >= MAX_STEPS:
            print("Fin: limite de pasos alcanzado (posible ciclo infinito).")

        if not ovm.Vivo:
            print("Boome murio. Fin de la ejecucion.")

    except Exception:
        # En entrega escolar se evita mostrar traceback
        print("Error controlado: el programa termino sin poder ejecutar el archivo.")