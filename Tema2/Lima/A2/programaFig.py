import json

class RM_Graph:

    def __init__(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            self.grafo = json.load(f)

    def normalizar(self, resp):
        resp = resp.strip().lower()

        # Normalizar respuestas tipo sí/no
        if resp in ["s", "si", "sí", "yes"]:
            return "S"
        if resp in ["n", "no"]:
            return "N"

        # Si es número, se regresa igual
        return resp

    def preguntar(self, nodo):
        if nodo not in self.grafo:
            print(f"\nLa figura es: {nodo}")
            return

        pregunta = self.grafo[nodo]["pregunta"]
        respuestas = self.grafo[nodo]["respuestas"]

        resp = input(pregunta + " ")
        resp = self.normalizar(resp)

        if resp in respuestas:
            siguiente = respuestas[resp]
            self.preguntar(siguiente)
        else:
            print("Respuesta no válida, intenta de nuevo.")
            self.preguntar(nodo)

    def run(self):
        self.preguntar("P0")


def main():
    grafo = RM_Graph("grafo.json")
    print("\n")
    print("Iniciando programa, adivinaremos tu figura.\n")
    grafo.run()


if __name__ == "__main__":
    main()