import yaml
import os


def entrenar(archivo_entrada, archivo_salida="pass.yaml"):

    if not os.path.exists(archivo_entrada):
        print("El archivo no se encontro")
        return

    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as file:
            datos = yaml.safe_load(file)
            
            if not datos or not isinstance(datos, dict):
                print("Error, archivo vacio")
                return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    datos_caracteristicas = {}

    for animal, caracteristicas in datos.items():
        if not isinstance(caracteristicas, dict):
            print("Omitir animal. Formato incorrecto")
            continue
            
        resp = {}
                
        for carac in caracteristicas.items():
            
            while True:
                respuesta = input(f"   ¿{animal} tiene la caracteristica '{carac}'? -> ").strip()
                
                if respuesta in ['0', '1']:
                    resp[carac] = int(respuesta)
                    break
                else:
                    print("Respuesta incorrecta")
        
        datos_caracteristicas[animal] = resp

    try:
        with open(archivo_salida, 'w', encoding='utf-8') as file:
            yaml.dump(datos_caracteristicas, file, default_flow_style=False, allow_unicode=True)
        
        print(f"\nGuardado en {archivo_salida}")
    except Exception as e:
        print(f"Error al guardar archivo: {e}")




NOMBRE_ARCHIVO_ENTRADA = "animales.yaml"  


NOMBRE_ARCHIVO_SALIDA = "tabla.yaml"

entrenar(NOMBRE_ARCHIVO_ENTRADA, NOMBRE_ARCHIVO_SALIDA)