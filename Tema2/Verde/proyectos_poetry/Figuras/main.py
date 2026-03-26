import argparse
import Adivinador as ADV
import json
from pathlib import Path

# Se usa para recibir el archivo por consola
parser = argparse.ArgumentParser()

parser.add_argument(
    "Archivo", help="Archivo: ", type=Path
)

args = parser.parse_args()

# Crear objeto del adivinador
adv = ADV.Adivinador()

# Verifica que el archivo exista
if args.Archivo.exists():
    print("👍")

    with args.Archivo.open('r') as arch_json:

        # Cargar JSON
        datos = json.load(arch_json)

        # Separar preguntas y transiciones
        preguntas = datos.get("Preguntas", {})
        parametros = datos["Transcisiones"]

        # Enviar datos al sistema
        adv.datos(preguntas, parametros)

        # Ejecutar el sistema
        adv.preguntas()