import yaml      
import os        
import random    
import math      


def entropia(valores):
    # Calcula qué tan buena es una característica
    # mientras más equilibrados estén los 0 y 1, mejor
    
    total = len(valores)
    
    if total == 0:
        return 0
    
    # Proporción de respuestas
    p1 = valores.count(1) / total
    p0 = valores.count(0) / total
    
    h = 0
    
    # Fórmula básica de entropía
    for p in [p1, p0]:
        if p > 0:
            h -= p * math.log2(p)
    
    return h


def adivinar(archivo_datos):

    # Verifica que exista el archivo
    if not os.path.exists(archivo_datos):
        print(f"Error. El archivo no se encontro")
        return

    # Carga los datos del archivo YAML
    try:
        with open(archivo_datos, 'r', encoding='utf-8') as file:
            datos_animales = yaml.safe_load(file)
            
            if not datos_animales:
                print("Error. El archivo YAML de datos esta vacio")
                return
    except Exception as e:
        print(f"Error: {e}")
        return

    # Lista de animales disponibles
    animales = list(datos_animales.keys())
    
    # Lista de características
    existentes = list(next(iter(datos_animales.values())).keys())

    print("\nSelecciona 1 para si o 0 para no")
    
    # Se repite hasta que quede un solo animal
    while len(animales) > 1:
        
        util = []
        
        # Filtra solo características que sí ayudan a diferenciar
        for clave in existentes:
            valores = set()
            
            for animal in animales:
                valor = datos_animales[animal].get(clave)
                if valor is not None:
                    valores.add(valor)
            
            if len(valores) > 1:
                util.append(clave)
        
        # Elegir la mejor característica (la más útil)
        mejor_caracteristica = None
        mejor_valor = -1

        for clave in util:
            valores = []
            
            for animal in animales:
                v = datos_animales[animal].get(clave)
                if v is not None:
                    valores.append(v)
            
            h = entropia(valores)
            
            if h > mejor_valor:
                mejor_valor = h
                mejor_caracteristica = clave

        caracteristica = mejor_caracteristica

        # Evita repetir la misma pregunta
        existentes.remove(caracteristica)
        
        # Pregunta al usuario
        while True:
            r = input(f"\n¿Tu animal tiene {caracteristica}? ").strip()
            
            if r in ['0', '1']:
                respuesta = int(r)
                break
            else:
                print("Respuesta incorrecta. Ingresa 1 para Si o 0 para No")

        nuevos_animales = []
        
        # Filtra los animales según la respuesta
        for animal in animales:
            v = datos_animales[animal].get(caracteristica, -1)
            
            if v == respuesta:
                nuevos_animales.append(animal)
        
        animales = nuevos_animales
        
        # Si no queda ninguno
        if len(animales) == 0:
            print("\nNo se encontro el animal")
            return
        
        # Muestra opciones si ya son pocos
        elif len(animales) > 1:
            if len(animales) < 6:
                print(f"\nAnimales posibles -> {', '.join(animales)}")
    
    # Resultado final
    print("\n---------------------------------------------")
    
    if len(animales) == 1:
        animal_adivinado = animales[0]
        print(f"Tu animal es: {animal_adivinado.lower()}")
    
    print("---------------------------------------------")


# Ejecuta el programa
ARCHIVO_ANIMALES = "tabla.yaml" 

adivinar(ARCHIVO_ANIMALES)