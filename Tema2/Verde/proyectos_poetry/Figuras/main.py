#ejecución: py main.py arbol.json

import argparse
import Adivinador as ADV
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "Archivo", help="Archivo: ", type=Path
)

args = parser.parse_args()
adv=ADV.Adivinador()
if args.Archivo.exists():
    print("👍")
    with args.Archivo.open('r') as arch_json:
        datos = json.load(arch_json)      # leer archivo JSON
        preguntas = datos.get("Preguntas", {})  # solo la parte de Preguntas
        parametros = datos["Transcisiones"]  # solo la parte de Parametros
        adv.datos(preguntas,parametros) 
        adv.preguntas()
            