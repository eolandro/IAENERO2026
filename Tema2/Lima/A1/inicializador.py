import json
import pandas as pd

datos_animales = {
    'animal': ['Perro', 'Gato', 'Hamster', 'Sapo', 'Caballo', 'Gallina', 'Quetzal', 'Huron', 'Castor', 'Lobo', 'Vaca', 'Foca'],
    'colorido': [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    'cuadrupedo': [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  
    'bigotes': [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    'pequeño': [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0],
    'carrera': [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0],  
    'construye': [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], 
    'largo': [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    'gordito': [1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1],  
    'manchas': [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1], 
    'aullido': [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    'huevo': [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],  
    'salta': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 
}

dataset = {
    'animales': datos_animales,
    'atributos': ['colorido', 'cuadrupedo', 'bigotes', 'pequeño', 'carrera', 
                'construye', 'largo', 'gordito', 'manchas', 'aullido', 'huevo', 'salta'],
    'version': 2.0,
    'total_animales': len(datos_animales['animal'])
}

def inicializar():
    df = pd.DataFrame(datos_animales)
    
    with open('adivinar_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(" Inicializado adivinar_dataset.json")
    print(f" {len(df)} animales, {len(dataset['atributos'])} atributos en BINARIOS")
    print("\nEjemplo:")
    print(df[['animal', 'colorido', 'cuadrupedo', 'bigotes', 'pequeño', 'carrera', 'construye', 'largo', 'gordito', 'manchas', 'aullido', 'huevo', 'salta']].head(12))
    print("\n Listo para: py thon adivinar.py")

if __name__ == "__main__":
    inicializar()
