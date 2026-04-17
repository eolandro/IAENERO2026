from ruamel.yaml import YAML


def inicializador():
	
    animales = []
    caracteristicas = []
    yaml = YAML()

    print("=== INICIALIZADOR ===")
    print("Ingresa 10 animales:")
    for i in range(10):
        animal = input(f"{i+1}. Animal: ").strip()
        animales.append(animal)

    print("\nIngresa 10 características (preguntas de 'si o no':")
    for i in range(10):
        car = input(f"{i+1}. Característica: ").strip()
        caracteristicas.append(car)

    data = {
        'animales': animales,
        'caracteristicas': caracteristicas
    }

    with open('animales.yaml', 'w') as file:
        yaml.dump(data, file) 
        
#El default_flow_stile es para que se guarde de manera mas legible y el unicode permite acentos y ñ	
	
    print("\nArchivo 'animales.yaml' generado exitosamente")

inicializador()
