import os
import yaml

# ============================================================
# RM_Graph - Razonamiento Monótono
# Programa para clasificar figuras geométricas usando un grafo
# ============================================================

def cargar_grafo(archivo="grafo.yaml"):
    ruta = os.path.join(os.path.dirname(__file__), archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ============================================================
# MANEJADORES DE TIPO DE NODO
# Cada función se encarga de manejar un tipo de pregunta
# y devuelve el siguiente nodo o el resultado.
# Así evitamos tener muchos if-else en el programa.
# ============================================================

def handler_binario(nodo, grafo):
    """Nodo con una pregunta simple de sí o no."""
    while True:
        resp = input(f"  {nodo['pregunta']} (s/n): ").strip().lower()
        if resp in ("s", "si", "sí"):
            return nodo["si"]
        elif resp in ("n", "no"):
            return nodo["no"]
        print("  Responde s o n")

def handler_multiple(nodo, grafo):
    """Nodo con varias opciones posibles (se usa un diccionario para evitar if-else)."""
    opciones = nodo["opciones"]
    claves = "/".join(opciones.keys())
    while True:
        resp = input(f"  {nodo['pregunta']} ({claves}): ").strip()
        if resp in opciones:
            return opciones[resp]
        print(f"  Opción inválida. Escribe una de: {claves}")

# Aquí relacionamos el tipo de nodo con la función que lo maneja
# R005: se minimiza el uso de if, el tipo de nodo decide el handler
HANDLERS = {
    "binario":   handler_binario,
    "multiple":  handler_multiple,
}

def obtener_handler(nodo):
    """Devuelve la función que corresponde según el tipo de nodo (por defecto binario)."""
    tipo = nodo.get("tipo", "binario")
    return HANDLERS[tipo]

# ============================================================
#                      MOTOR DE INFERENCIA
# ============================================================

def es_resultado(nodo_id, grafo):
    """Regresa True si el nodo actual ya es un resultado final."""
    return nodo_id in grafo["resultados"]

def mostrar_resultado(resultado_id, grafo):
    res = grafo["resultados"][resultado_id]
    print("\n" + "=" * 45)
    print(f"  FIGURA: {res['nombre'].upper()}")
    print(f"  {res['descripcion']}")
    print("=" * 45)

def recorrer_grafo(grafo):
    """
    Motor de inferencia: se encarga de recorrer el grafo.
    Cada nodo usa el handler que le corresponde para decidir
    cuál será el siguiente paso.
    """
    nodo_id = grafo["inicio"]
    pasos = 0

    print("\nPiensa en una figura geométrica y responde:\n")

    while not es_resultado(nodo_id, grafo):
        nodo = grafo["nodos"][nodo_id]
        handler = obtener_handler(nodo)
        pasos += 1
        print(f"Pregunta {pasos}:")
        nodo_id = handler(nodo, grafo)
        print()

    mostrar_resultado(nodo_id, grafo)
    print(f"  Preguntas realizadas: {pasos}\n")

# ============================================================
#                           MAIN
# ============================================================

def main():
    print("\n" + "=" * 45)
    print("  RM_Graph - Razonamiento Monótono con Grafos")
    print("  Clasificador de Figuras Geométricas")
    print("=" * 45)

    grafo = cargar_grafo()
    figuras = list(grafo["resultados"].keys())
    print(f"\nFiguras registradas: {len(figuras)}")
    for fid in figuras:
        r = grafo["resultados"][fid]
        print(f"  {r['nombre']}")

    while True:
        recorrer_grafo(grafo)
        otra = input("Jugar de nuevo? (s/n): ").strip().lower()
        if otra not in ("s", "si"):
            print("\nFin del programa.")
            break

if __name__ == "__main__":
    main()
