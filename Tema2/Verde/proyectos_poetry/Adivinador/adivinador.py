import yaml
import os
import random



def adivinar(archivo_datos="tabla.yaml"):

    preguntas = {
    "colorido": "¿Tu animal es colorido?",
    "cuadrupedo": "¿Tu animal es cuadrúpedo?",
    "bigotes": "¿Tu animal tiene bigotes?",
    "pequeño": "¿Tu animal es pequeño?",
    "carrera": "¿Tu animal corre rápido?",
    "construye": "¿Tu animal construye cosas?",
    "largo": "¿Tu animal es de cuerpo largo?",
    "gordita": "¿Tu animal es gordito?",
    "machas": "¿Tu animal tiene manchas?",
    "aullido": "¿Tu animal aúlla?",
    "huevo": "¿Tu animal pone huevos?",
    "salta": "¿Tu animal salta?"
    }

    if not os.path.exists(archivo_datos):
        print(f"Error. El archivo no se encontro")
        return

    try:
        with open(archivo_datos, 'r', encoding='utf-8') as file:
            datos_animales = yaml.safe_load(file)
            
            if not datos_animales:
                print("Error. El archivo YAML de datos esta vacio")
                return
    except Exception as e:
        print(f"Error: {e}")
        return

    animales = list(datos_animales.keys())
    
    
    existentes = list(next(iter(datos_animales.values())).keys())
    print("\nSelecciona 1 para si o 0 para no")
    
    while len(animales) > 1:
        
        util = []
        
        for clave in existentes:
            valores = set()
            
            for animal in animales:
                valor = datos_animales[animal].get(clave)
                if valor is not None:
                    valores.add(valor)
            
            if len(valores) > 1:
                util.append(clave)
            
        caracteristica = random.choice(util)
        #quita la pregunta
        existentes.remove(caracteristica)
                
        while True:
            r = input(f"\n{preguntas[caracteristica]} ").strip().lower()
            
            if r in ['0', '1']:
                respuesta = int(r)
                break
            else:
                print("Respuesta incorrecta. Ingresa 1 para Si o 0 para No")

        nuevos_animales = []
        
        for animal in animales:
            v = datos_animales[animal].get(caracteristica, -1)
            
            if v == respuesta:
                nuevos_animales.append(animal)
        
        animales = nuevos_animales
        
        if len(animales) == 0:
            print("\nNo se encontro el animal")
            return
        elif len(animales) > 1:
            if len(animales) < 6:
                print(f"\nAnimales posibles -> {', '.join(animales)}")
            
    print("\n---------------------------------------------")
    if len(animales) == 1:
        animal_adivinado = animales[0]
        print(f"Tu animal es: {animal_adivinado.lower()}")
    print("---------------------------------------------")




    
ARCHIVO_ANIMALES = "tabla.yaml" 
    
adivinar(ARCHIVO_ANIMALES)