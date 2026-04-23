from ruamel.yaml import YAML
from pathlib import Path

def entrenador():
    yaml = YAML()
    if not Path('animales.yaml').exists(): return print("Error: Ejecuta Inicializador.py")

    with open('animales.yaml', 'r', encoding='utf-8') as file:
        datos = yaml.load(file)
    
    animales, caracteristicas = datos['animales'], datos['caracteristicas']
    
    print("=== ETAPA 2: ENTRENADOR (RSTeoriaInfo) ===")
    print("-" * 40)
    print("LISTA DE ANIMALES A ENTRENAR:")
    for i, ani in enumerate(animales, 1): print(f"{i}. {ani}")
    print("-" * 40)

    tabla = {}
    # Ajuste de pesos para 13 características (2^12 down to 2^0)
    pesos = [2**i for i in range(len(caracteristicas)-1, -1, -1)]
    
    for animal in animales:
        print(f"\n>> Configurando: {animal.upper()}")
        respuestas = []
        suma_binaria = 0
        for i, car in enumerate(caracteristicas):
            resp = input(f"   ¿{car}? (1:Si / 0:No): ").strip()
            val = 1 if resp in ['1', 's', 'si'] else 0
            respuestas.append(val)
            if val == 1: suma_binaria += pesos[i]

        tabla[animal] = {'respuestas': respuestas, 'suma_binaria': suma_binaria}
    
    with open('tabla.yaml', 'w', encoding='utf-8') as file:
        yaml.dump({'caracteristicas': caracteristicas, 'tabla_animales': tabla}, file)
    print("\n[OK] Tabla de pesos generada en 'tabla.yaml'.")

if __name__ == "__main__":
    entrenador()
