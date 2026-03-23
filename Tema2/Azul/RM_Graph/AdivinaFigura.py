"""
AdivinaFigura.py
Clasificador de figuras geométricas usando un árbol de decisión
cargado desde un archivo JSON externo (figuras.json).
"""

import json
import sys

ARCHIVO_ARBOL = "figuras.json"


def cargar_arbol(ruta: str) -> tuple[dict, dict]:
    """Lee el JSON y devuelve (preguntas, transiciones)."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        sys.exit(f"[Error] No se encontró '{ruta}'. Asegúrate de que esté en la misma carpeta.")
    except json.JSONDecodeError as e:
        sys.exit(f"[Error] El archivo '{ruta}' tiene formato inválido: {e}")

    preguntas = datos["Preguntas"]

    transiciones = {
        (origen, respuesta): destino
        for origen, respuesta, destino in datos["Transiciones"]
    }
    return preguntas, transiciones


def obtener_opciones(nodo: str, transiciones: dict) -> list[str]:
    """Devuelve las respuestas válidas desde el nodo actual."""
    return [resp for (origen, resp) in transiciones if origen == nodo]


def pedir_respuesta(opciones: list[str]) -> str:
    """Solicita al usuario una respuesta válida sin if-else en cadena."""
    opciones_lower = {op.lower(): op for op in opciones}
    prompt = f"  Opciones: {' | '.join(opciones)}\n  > "

    while True:
        entrada = input(prompt).strip().lower()
        respuesta_valida = opciones_lower.get(entrada)
        if respuesta_valida:
            return respuesta_valida
        print(f"Respuesta no reconocida. Elige entre: {opciones}")


def recorrer_arbol(preguntas: dict, transiciones: dict) -> str:
    """Recorre el árbol de decisión y retorna la figura clasificada."""
    nodo = "A"

    while True:
        opciones = obtener_opciones(nodo, transiciones)

        #Nodo hoja: no hay transiciones salientes - es un resultado
        if not opciones:
            return preguntas[nodo]

        print(f"\n  {preguntas[nodo]}")
        respuesta = pedir_respuesta(opciones)
        nodo = transiciones[(nodo, respuesta)]



BIENVENIDA = """
     ADIVINA LA FIGURA GEOMÉTRICA :)

Piensa en una figura y responde las preguntas.
Figuras posibles:
  • Curvas  : Círculo, Elipse
  • 3 lados : Equilátero, Isósceles, Rectángulo, Escaleno
  • 4 lados : Cuadrado, Rombo, Romboide, Rectángulo,
              Paralelogramo, Trapecio, Trapecio Rectángulo,
              Cuadrilátero Irregular
  • 5 lados : Pentágono Regular / Irregular
  • 6 lados : Hexágono Regular / Irregular
  • 8 lados : Octágono Regular / Irregular
  • 10 lados: Decágono Regular / Irregular, Estrella de 5 Picos
"""

RESPUESTAS_SI = {"si", "s", "sí"}


def jugar(preguntas: dict, transiciones: dict) -> None:
    """Bucle principal del juego."""
    print(BIENVENIDA)

    while True:
        figura = recorrer_arbol(preguntas, transiciones)
        print(f"\nLa figura es: {figura}\n")

        print("¿Deseas jugar de nuevo? (Sí / No)")
        opcion = input("  > ").strip().lower()
        if opcion not in RESPUESTAS_SI:
            print("\nFin del programa\n")
            break


def main() -> None:
    preguntas, transiciones = cargar_arbol(ARCHIVO_ARBOL)
    jugar(preguntas, transiciones)


if __name__ == "__main__":
    main()
