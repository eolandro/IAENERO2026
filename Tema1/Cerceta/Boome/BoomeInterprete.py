import argparse
import anlex
from vm import BoomeVM


def cargar_lineas(archivo):
    lineas = []
    for raw in archivo:
        if "#" in raw:
            raw = raw.split("#", 1)[0]
        raw = raw.strip()
        if raw != "":
            lineas.append(raw)
    return lineas


def main():
    parser = argparse.ArgumentParser(
        prog="BoomeInterprete",
        description="Ejecuta un archivo de código Boome",
    )
    parser.add_argument("archivo_codigo", type=argparse.FileType("r"))
    parser.add_argument("--paso", action="store_true", help="Pausa por instrucción")
    parser.add_argument(
        "--sin-mapa", action="store_true", help="No imprime el mapa en cada paso"
    )
    args = parser.parse_args()

    lineas = cargar_lineas(args.archivo_codigo)

    vm = BoomeVM(filas=5, columnas=25)

    if not args.sin_mapa:
        print(vm)

    pc = 0
    while pc < len(lineas):
        linea = lineas[pc]
        tokens = anlex.tokenizar(linea)

        ok, err = anlex.validar(tokens)
        if not ok:
            print("Error de sintaxis en línea " + str(pc + 1) + ": " + err)
            print("  >> " + linea)
            break

        pc = vm.execute(tokens, pc)

        if not args.sin_mapa:
            print(vm)

        if args.paso:
            input("Enter para continuar...")

        if not vm.Vivo:
            break


if __name__ == "__main__":
    main()
