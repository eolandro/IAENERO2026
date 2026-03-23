import yaml
import re
from collections import Counter

ruta_entrada = "entrenador.yaml"

# Cargar datos
with open(ruta_entrada, "r", encoding="utf-8") as archivo:
    registros = yaml.safe_load(archivo)

palabras_ignoradas = {
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre",
    "hacia", "hasta", "para", "por", "según", "sin", "so", "sobre", "tras",
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "e",
    "que", "se", "su", "sus", "al", "del", "es", "ha", "han", "como", "más",
    "muy", "pero", "si", "no", "lo", "le", "les", "ya", "te", "tu",
    "esto", "eso", "aquí", "allí", "ser", "estar", "son", "fue", "fueron"
}

# Filtrar solo mensajes spam
lista_spam = []
for texto, categoria in registros.items():
    if categoria == "spam":
        lista_spam.append(texto)

def dividir_texto(cadena):
    palabras = re.findall(r'\b[a-záéíóúñ]+\b', cadena.lower())
    resultado = []
    for palabra in palabras:
        if palabra not in palabras_ignoradas:
            resultado.append(palabra)
    return resultado

# Tokenizar mensajes
tokens = []
for mensaje in lista_spam:
    tokens.append(dividir_texto(mensaje))

# Unir todas las palabras
acumulado = []
for grupo in tokens:
    for palabra in grupo:
        acumulado.append(palabra)

conteo = Counter(acumulado)

total_spam = len(lista_spam)
modelo_palabras = {}

for palabra, cantidad in conteo.items():
    presencia = 0
    for grupo in tokens:
        if palabra in grupo:
            presencia += 1
    
    prob = presencia / total_spam if total_spam > 0 else 0
    
    modelo_palabras[palabra] = {
        "conteo": cantidad,
        "prob": round(prob, 4)
    }

# Ordenar manualmente
ordenado = sorted(modelo_palabras.items(), key=lambda x: x[1]["prob"], reverse=True)

top_palabras = {}
limite = 15
contador = 0

for palabra, datos in ordenado:
    if contador >= limite:
        break
    top_palabras[palabra] = datos
    contador += 1

# Guardar resultado
ruta_salida = "tokenizador.yaml"
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    yaml.dump(top_palabras, archivo, allow_unicode=True, sort_keys=False)

print(f"\nArchivo generado: {ruta_salida} con las palabras más relevantes.\n")