"""
Entrenador 
Carga mensajes de entrada y el supervisor los etiqueta como spam o no_spam.
Genera un archivo YAML con los mensajes etiquetados.
"""

import os
from ruamel.yaml import YAML


yaml = YAML()
yaml.preserve_quotes = True

# Rutas de archivos
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ENTRADA = os.path.join(DATA_DIR, "mensajes_entrada.yml")
SALIDA = os.path.join(DATA_DIR, "mensajes_etiquetados.yml")


def cargar_mensajes(ruta):
    """Carga mensajes desde un archivo YAML."""
    with open(ruta, "r", encoding="utf-8") as f:
        datos = yaml.load(f)
    return datos["mensajes"]


def etiquetar_mensajes(mensajes):
    """
    Muestra cada mensaje al supervisor y pregunta si es spam o no.
    Retorna lista de mensajes con su etiqueta.
    """
    etiquetados = []
    print("\n" + "=" * 60)
    print("  ENTRENADOR - Clasificación del Supervisor")
    print("=" * 60)
    print("Clasifica cada mensaje como 'spam' o 'no_spam'.\n")

    for msg in mensajes:
        print(f"--- Mensaje {msg['id']} ---")
        print(f"  \"{msg['texto']}\"")

        while True:
            respuesta = input("  ¿Es spam? (s/n): ").strip().lower()
            if respuesta in ("s", "n"):
                break
            print("  Por favor responde 's' para spam o 'n' para no_spam.")

        etiqueta = "spam" if respuesta == "s" else "no_spam"
        etiquetados.append({
            "id": msg["id"],
            "texto": msg["texto"],
            "etiqueta": etiqueta,
        })
        print(f"  -> Etiquetado como: {etiqueta}\n")

    return etiquetados


def guardar_etiquetados(etiquetados, ruta):
    """Guarda los mensajes etiquetados en un archivo YAML."""
    datos = {"mensajes_etiquetados": etiquetados}
    with open(ruta, "w", encoding="utf-8") as f:
        yaml.dump(datos, f)
    print(f"Archivo generado: {ruta}")


def ejecutar():
    """Ejecuta la etapa de entrenamiento completa."""
    mensajes = cargar_mensajes(ENTRADA)
    etiquetados = etiquetar_mensajes(mensajes)
    guardar_etiquetados(etiquetados, SALIDA)
    return etiquetados


if __name__ == "__main__":
    ejecutar()
