import os
import sys
import runpy

ruta = os.path.dirname(__file__)
os.chdir(ruta)

scripts = [
    "entrenador.py",
    "detokenizador.py",
    "clasificador.py",
    "metricas.py",
]

print("\nINICIANDO PRACTICA CLASS_PROB\n")

for script in scripts:
    print(f">>> Ejecutando {script}...")
    archivo = os.path.join(ruta, script)

    try:
        runpy.run_path(archivo, run_name="__main__")
    except SystemExit as ex:
        codigo = ex.code if isinstance(ex.code, int) else 1
        if codigo == 0:
            print(f"OK: {script} completado\n")
            continue
        print(f"ERROR: {script} falló")
        sys.exit(1)
    except Exception:
        print(f"ERROR: {script} falló")
        sys.exit(1)

    print(f"OK: {script} completado\n")

print("Práctita terminada")
