import yaml
import re

archivo_txt = "10msjspam2.txt"

with open(archivo_txt, "r", encoding="utf-8") as f:
    contenido = f.read()

contenido = re.sub(r'(?im)^\s*(SPAM|NO\s*SPAM)\s*$', '', contenido)

mensajes = re.findall(r'"(.*?)"', contenido, re.DOTALL)

resultados = {}

print("=== Clasificador de mensajes (y = spam, n = no spam) ===")

for i, mensaje in enumerate(mensajes, start=1):
    print(f"\nMensaje {i}:\n{'-'*40}")
    print(mensaje.strip())
    print('-'*40)
    
    while True:
        respuesta = input("¿Es spam? (y/n): ").strip().lower()
        if respuesta in ("y", "n"):
            resultados[mensaje.strip()] = "spam" if respuesta == "y" else "no spam"
            break
        else:
            print("Entrada inválida. Escribe 'y' para spam o 'n' para no spam.")

# Guardar resultados en YAML
archivo_salida = "entrenador.yaml"
with open(archivo_salida, "w", encoding="utf-8") as f:
    yaml.dump(resultados, f, allow_unicode=True, sort_keys=False)

print(f"\nClasificación guardada en '{archivo_salida}'")
