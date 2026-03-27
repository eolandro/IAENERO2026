import json
import pandas as pd

def cargar_dataset():
    try:
        with open('adivinar_dataset.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data['animales'])
        return df, data
    except FileNotFoundError:
        print(" Ejecuta inicializador.py primero")
        return None, None

def agregar_animal(data):
    attrs = data['atributos']  # Solo atributos binarios
    nombre = input(" Nuevo animal: ").strip().title()
    if nombre in data['animales']['animal']:
        print(" Ya existe")
        return data
    
    nuevo = {'animal': nombre}
    print("1=Sí 0=No:")
    for attr in attrs:
        nuevo[attr] = int(input(f"  {attr}: "))
    
    data['animales']['animal'].append(nombre)
    for attr in attrs:
        data['animales'][attr].append(nuevo[attr])
    data['total_animales'] += 1
    
    print(f" Agregado {nombre}")
    return data

def guardar(data):
    with open('adivinar_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(" Guardado")

def entrenar():
    df, data = cargar_dataset()
    if df is None: return
    
    while True:
        accion = input("\n1=Agregar 2=Ver 3=Guardar/Salir: ")
        if accion == '1':
            data = agregar_animal(data)
        elif accion == '2':
            print("\nAnimales:", data['animales']['animal'])
            print("Total:", data['total_animales'])
        elif accion == '3':
            guardar(data)
            break

if __name__ == "__main__":
    entrenar()
