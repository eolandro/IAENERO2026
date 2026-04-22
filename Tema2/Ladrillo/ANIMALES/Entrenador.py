from ruamel.yaml import YAML
from pathlib import Path

def entrenador():
    yaml = YAML()
    archivo_animales = Path('animales.yaml')
    
    if not archivo_animales.exists():
        print("Error: Ejecuta primero el Inicializador.py")
        return

    with open(archivo_animales, 'r', encoding='utf-8') as file:
        datos = yaml.load(file)
    
    animales = datos['animales']
    caracteristicas = datos['caracteristicas']
    
    print("=== ETAPA 2: ENTRENADOR (TABLA DE PESOS) ===")
    tabla = {}
    
    for animal in animales:
        print(f"\n--- Configurando: {animal.upper()} ---")
        respuestas = []
        
        for i, car in enumerate(caracteristicas, 1):
            while True:
                # Validación multiformato solicitada por el usuario
                resp = input(f"{i}. {car} (si/no): ").strip().lower()
                if resp in ['si', 'sí', 's', '1']:
                    respuestas.append(1)
                    break
                elif resp in ['no', 'n', '0']:
                    respuestas.append(0)
                    break
                print("Respuesta inválida. Use: si, no, s, n, 1 o 0.")

        # Cálculo de Suma Binaria (Optimización de Información)
        suma_binaria = 0
        for bit in respuestas:
            suma_binaria = (suma_binaria << 1) | bit 

        tabla[animal] = {
            'respuestas': respuestas,
            'suma_binaria': int(suma_binaria)
        }
    
    datos_finales = {
        'caracteristicas': caracteristicas,
        'tabla_animales': tabla
    }
    
    with open('tabla.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(datos_finales, file)
    
    print("\n¡Entrenamiento completado! 'tabla.yaml' guardado.")

if __name__ == "__main__":
    entrenador()
