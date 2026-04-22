from ruamel.yaml import YAML

def inicializador():
    yaml = YAML()
    
    # Definición de la Red Semántica: Nodos (animales) y Arcos (características)
    animales = [
        "perro", "gato", "caballo", "sapo", "lobo", "quetzal", 
        "gallina", "hamster", "castor", "huron", "vaca", "foca"
    ]
    
    caracteristicas = [
        "Es un animal homeotermo (sangre caliente)?",
        "Posee glandulas mamarias?",
        "Es un depredador activo?",
        "Su habitat principal involucra medios acuaticos?",
        "Tiene extremidades modificadas (pezuñas, alas o aletas)?",
        "Es un animal domesticado?",
        "Posee habitos nocturnos?",
        "Su piel es desnuda o con escamas?",
        "Tiene capacidad de vuelo?",
        "Produce sonidos fuertes (aullido, relincho, mugido)?"
    ]

    data = {
        'animales': animales,
        'caracteristicas': caracteristicas
    }

    with open('animales.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data, file)
    
    print("=== ETAPA 1: INICIALIZADOR COMPLETO ===")
    print("Archivo 'animales.yaml' generado exitosamente.")

if __name__ == "__main__":
    inicializador()
