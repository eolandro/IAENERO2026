from ruamel.yaml import YAML
from pathlib import Path

def entrenador():
    # Verificar que el archivo animales.yaml existe
    yaml = YAML()
    archivo_animales = Path('animales.yaml')
    if not archivo_animales.exists():
        print("Error: No se encuentra el archivo 'animales.yaml'")
        print("Ejecuta primero el programa inicializador.")
        return

    # Cargar datos del archivo YAML
    with open(archivo_animales, 'r') as file:
        datos = yaml.load(file)
    
    animales = datos['animales']
    caracteristicas = datos['caracteristicas']
    
    print("=== ENTRENADOR ===")
    print("Responde 'si' o 'no' para cada característica de cada animal:\n")
    
    # Crear tabla de respuestas
    tabla = {}
    
    for animal in animales:
        print(f"\n--- {animal.upper()} ---")
        respuestas = []
        
        for i, caracteristica in enumerate(caracteristicas, 1):
            while True:
                respuesta = input(f"{i}. {caracteristica}: ").strip().lower()
                if respuesta in ['si', 'sí', 's', '1']:
                    respuestas.append(1)
                    break
                elif respuesta in ['no', 'n', '0']:
                    respuestas.append(0)
                    break
                else:
                    print("Por favor, responde 'si' o 'no'")
                    
        

        # Calcular suma binaria 
        suma_binaria = 0
        for bit in respuestas:
            suma_binaria = suma_binaria * 2 + bit   


        tabla[animal] = {
            'respuestas': respuestas,
            'suma_binaria': suma_binaria
        }
    
    # Guardar tabla en archivo YAML
    datos_tabla = {
        'caracteristicas': caracteristicas,
        'tabla_animales': tabla
    }
    
    with open('tabla.yaml', 'w') as file:
        yaml.dump(datos_tabla, file)
    
    print(f"\nTabla guardada en 'tabla.yaml'")
    print("Resumen de sumas binarias:")
    for animal, datos in tabla.items():
        print(f"{animal}: {datos['respuestas']} → {datos['suma_binaria']}")


entrenador()
