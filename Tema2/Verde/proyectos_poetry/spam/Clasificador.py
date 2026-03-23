import yaml
import re

ruta_modelo = "tokenizador.yaml"
ruta_entrada = "10msjspam.txt"
ruta_resultado = "clasificador.yaml"

# Cargar probabilidades
with open(ruta_modelo, "r", encoding="utf-8") as archivo:
    modelo = yaml.safe_load(archivo)

# Leer mensajes
with open(ruta_entrada, "r", encoding="utf-8") as archivo:
    texto_completo = archivo.read()

# Eliminar etiquetas SPAM / NO SPAM
texto_limpio = re.sub(r'(?im)^\s*(SPAM|NO\s*SPAM)\s*$', '', texto_completo)

# Extraer mensajes entre comillas
lista_mensajes = re.findall(r'"(.*?)"', texto_limpio, re.DOTALL)

print(f"\nTotal de mensajes encontrados: {len(lista_mensajes)}\n")

palabras_vacias = {
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre",
    "hacia", "hasta", "para", "por", "según", "sin", "so", "sobre", "tras",
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "e",
    "que", "se", "su", "sus", "al", "del", "es", "ha", "han", "como", "más",
    "muy", "pero", "si", "no", "lo", "le", "les", "ya", "te", "tu",
    "esto", "eso", "aquí", "allí", "ser", "estar", "son", "fue", "fueron"
}

def procesar_texto(cadena):
    # Separar palabras y filtrar
    palabras = re.findall(r'\b[a-záéíóúñ]+\b', cadena.lower())
    resultado = []
    for palabra in palabras:
        if palabra not in palabras_vacias:
            resultado.append(palabra)
    return resultado

salida = {}

for texto in lista_mensajes:
    palabras_clave = procesar_texto(texto)
    
    valores = []
    for palabra in palabras_clave:
        if palabra in modelo:
            valores.append(modelo[palabra]["probabilidad"])
    
    # Cambio en lógica: evitar división directa
    promedio = (sum(valores) / len(valores)) if len(valores) > 0 else 0.0
    
    etiqueta = "spam" if promedio >= 0.5 else "no_spam"
    
    salida[texto] = {
        "score": round(promedio * 100, 2),
        "tipo": etiqueta
    }

# Guardar resultados
with open(ruta_resultado, "w", encoding="utf-8") as archivo:
    yaml.dump(salida, archivo, allow_unicode=True, sort_keys=False)

print(f"Clasificación completada. Archivo generado: {ruta_resultado}\n")