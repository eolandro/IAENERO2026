import argparse
import anlex
from vm import BoomeVM
import os
import time

# Configuración de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("Archivo")
args = parser.parse_args()

programa = []

# Lectura y procesamiento del archivo
if os.path.exists(args.Archivo):
    with open(args.Archivo, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            
            # 1. Intentamos usar tu analizador léxico (anlex.py)
            tokens = anlex.procesar_linea(linea)
            
            if tokens:
                # Si anlex lo valida, lo agregamos
                programa.append(tokens)
            else:
                # 2. FUNCIONALIDAD ADICIONAL:
                # Si anlex no lo reconoce (como pasa con 'avanza' o 'sensor'),
                # procesamos manualmente para que la VM pueda trabajar.
                tokens_manuales = [t for t in linea.split(" ") if t]
                if tokens_manuales:
                    programa.append(tokens_manuales)
else:
    print(f"Error: El archivo {args.Archivo} no existe.")
    exit()

# Inicialización de la Máquina Virtual
vm = BoomeVM()

print(f"--- Iniciando ejecución de: {args.Archivo} ---")

# Ciclo de ejecución (Mantiene la lógica original del main)
while vm.PC < len(programa) and vm.estado == "Activo":
    # Opcional: Limpiar pantalla para animación
    # os.system('cls' if os.name == 'nt' else 'clear')
    
    instruccion = programa[vm.PC]
    print(f"\n>>> Paso {vm.PC}: {instruccion}")
    
    vm.ejecutar(instruccion)
    vm.PC += 1
    
    # Imprime el estado actual de la VM (registros, posición, mapa)
    print(vm)
    
    # Pausa para visualizar la ejecución
    time.sleep(0.3)

print(f"\nFin del programa. Resultado final: {vm.estado}")