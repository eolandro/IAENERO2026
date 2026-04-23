from ruamel.yaml import YAML

def inicializador():
    yaml = YAML()
    
    animales = [
        "Perro", "Gato", "Hamster", "Sapo", "Caballo", 
        "Gallina", "Quetzal", "Huron", "Castor", "Lobo", "Vaca", "Foca"
    ]
    
    caracteristicas = [
        "Colorido", "Cuadrúpedo", "Bigotes", "Pequeño", "Carrera", 
        "Construye", "Largo", "Gordita(o)", "Machas", "Aullido", "Huevo", "Salta"
    ]

    data = {'animales': animales, 'caracteristicas': caracteristicas}

    with open('animales.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data, file)
    
    print("=== ETAPA 1: INICIALIZADOR (RSTeoriaInfo) ===")
    print(f"Animales cargados: {', '.join(animales)}")
    print("Archivo 'animales.yaml' generado con éxito.")

if __name__ == "__main__":
    inicializador()
