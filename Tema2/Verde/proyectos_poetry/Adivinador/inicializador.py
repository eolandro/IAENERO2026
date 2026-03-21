import yaml

def regCaracteristicas(c=10):
    caracteristicas = []
    print("\nIngresa las caracteristicas")
    
    for i in range(1, c+1):
        while True:
            car = input(f"Caracteristica {i}: ").strip()
            if car:
                caracteristicas.append(car)
                break
            else:
                print("Ingresa una caracteristica valida")
                
    return caracteristicas

def animales(claves, numAn=10):
    datos_animales = {}    

    for i in range(1, numAn + 1):
        nombre = input(f"\nAnimal {i}: Ingresa el nombre del animal: ").strip()
        
        if not nombre:
            print("Omitido")
            continue

        datos = {}
        for clave in claves:
            datos[clave] = '' 
        
        datos_animales[nombre] = datos
        
        print("ok")

    return datos_animales

def guardar(datos, nombre_archivo="animales.yaml"):
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            yaml.dump(datos, archivo, default_flow_style=False, allow_unicode=True)
        print(f"\nGuardado en {nombre_archivo}")
    except Exception as e:
        print(f"\nError al guardar el archivo YAML: {e}")


caracteristicas_animales = regCaracteristicas()

if caracteristicas_animales:
    info_animales = animales(caracteristicas_animales)

    if info_animales:
        print(yaml.dump(info_animales, default_flow_style=False, allow_unicode=True))
        guardar(info_animales)
        print("ok")
    else:
        print("Error, no se guardo")
else:
    print("No existen caracteristicas")