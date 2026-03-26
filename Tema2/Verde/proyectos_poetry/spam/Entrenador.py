import yaml
import re

ruta_archivo = "10msjspam2.txt"

# Leer contenido del archivo
with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    texto = archivo.read()

# Quitar etiquetas SPAM / NO SPAM
texto = re.sub(r'(?im)^\s*(SPAM|NO\s*SPAM)\s*$', '', texto)

# Obtener mensajes entre comillas
mensajes_extraidos = re.findall(r'"(.*?)"', texto, re.DOTALL)

clasificacion_final = {}

print("=== Sistema de etiquetado de mensajes ===")

indice = 1
for elemento in mensajes_extraidos:
    mensaje_limpio = elemento.strip()
    
    print(f"\nMensaje #{indice}")
    print("=" * 40)
    print(mensaje_limpio)
    print("=" * 40)
    
    valido = False
    while not valido:
        entrada = input("¿Clasificar como spam? (y/n): ").lower().strip()
        
        if entrada == "y":
            clasificacion_final[mensaje_limpio] = "spam"
            valido = True
        elif entrada == "n":
            clasificacion_final[mensaje_limpio] = "no_spam"
            valido = True
        else:
            print("Opción no válida. Usa 'y' o 'n'.")
    
    indice += 1

# Guardar archivo YAML
ruta_guardado = "entrenador.yaml"
with open(ruta_guardado, "w", encoding="utf-8") as archivo:
    yaml.dump(clasificacion_final, archivo, allow_unicode=True, sort_keys=False)

print(f"\nDatos guardados correctamente en: {ruta_guardado}")