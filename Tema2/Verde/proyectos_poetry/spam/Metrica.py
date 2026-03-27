import yaml
import re

ruta_datos = "10msjspam.txt"
ruta_predicciones = "clasificador.yaml"
ruta_salida = "metricas_evaluacion.yaml"

# Leer mensajes (SIN usar etiquetas del archivo)
with open(ruta_datos, "r", encoding="utf-8") as archivo:
    texto_base = archivo.read()

# Extraer solo mensajes
mensajes = re.findall(r'"(.*?)"', texto_base, re.DOTALL)

print("\n=== Evaluación manual de mensajes ===")

valores_reales = []

# 🔥 AQUÍ SE LE PREGUNTA AL USUARIO
for i, mensaje in enumerate(mensajes, 1):
    limpio = mensaje.strip().replace('\n', ' ')
    
    print(f"\nMensaje #{i}")    
    print("-" * 40)
    print(limpio)
    print("-" * 40)
    
    while True:
        entrada = input("¿Es spam? (y/n): ").lower().strip()
        
        if entrada == "y":
            valores_reales.append("spam")
            break
        elif entrada == "n":
            valores_reales.append("no_spam")
            break
        else:
            print("Opción inválida. Usa 'y' o 'n'.")

# Leer clasificaciones del modelo
with open(ruta_predicciones, "r", encoding="utf-8") as archivo:
    predicciones = yaml.safe_load(archivo)

# Inicializar contadores
tp = fp = tn = fn = 0

def normalizar(cadena):
    return cadena.strip().replace('\n', ' ')

# Comparar resultados
lista_predicciones = list(predicciones.values())

for i, etiqueta_real in enumerate(valores_reales):
    
    clave = f"mensaje_{i+1}"
    
    if clave not in predicciones:
        continue
    
    etiqueta_predicha = predicciones[clave]["tipo"]

    if etiqueta_real == "spam":
        if etiqueta_predicha == "spam":
            tp += 1
        else:
            fn += 1
    else:
        if etiqueta_predicha == "spam":
            fp += 1
        else:
            tn += 1

# Cálculo de métricas
total = tp + fp + tn + fn

acc = (tp + tn) / total if total > 0 else 0
prec = tp / (tp + fp) if (tp + fp) != 0 else 0
rec = tp / (tp + fn) if (tp + fn) != 0 else 0
prev = (tp + fn) / total if total > 0 else 0

resultado_metricas = {
    "accuracy": round(acc, 3),
    "precision": round(prec, 3),
    "recall": round(rec, 3),
    "prevalence": round(prev, 3)
}

# Guardar métricas
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    yaml.dump(resultado_metricas, archivo, allow_unicode=True, sort_keys=False)

print("\nMétricas calculadas correctamente:")
#print(resultado_metricas)
#{'accuracy': 0.6, 'precision': 0.667, 'recall': 0.4, 'prevalence': 0.5}