from ruamel.yaml import YAML

"""Este programa permite identificar una figura geometrica dado una "base",
la cual requiere de un archivo .YAML, en donde preguntara al usuario para acertar
la respuesta."""


class FigGeo:
    def __init__(self, yaml_file):
        yaml = YAML()
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.load(f)

        # Datos del YAML
        # start: P0 (Estado inicial)
        self.start = data["start"]
        # questions: P0,P1,Px...
        self.questions = data["questions"]
        # CI: Circulo; EL: Elipse...
        self.objects = data["objects"]

        # Tabla de adyacencia//Grafo
        self.adjacency = data["graph"]

        # key-value
        # ori -> Nodo Origen
        # res -> Respuesta
        # dest -> Node Destino
        self.kv = {(ori, str(res)): dest for ori, res, dest in self.adjacency}

        self.node = self.start

    def run(self):

        while True:
            # si el nodo es un objeto final
            if self.node in self.objects:
                print("\nObjeto identificado:", self.objects[self.node])
                break

            question = self.questions[self.node]

            # Nota a mi mismo: Deberia de omitir el S/N en la primera pregunta
            # antibin -> "Anti binario (Osea no muestra "S/N en la primera pregunta)"
            antibin = (
                f"{question}: " if self.node == self.start else f"{question} (S/N): "
            )
            ans = input(antibin).strip().upper()

            # ans = input(f"{question} (S/N): ").strip().upper()

            # Transición hacia el siguiente nodo
            next_node = self.kv.get((self.node, ans))

            if next_node is None:
                print("Respuesta no válida para esta pregunta.")
                continue

            self.node = next_node


def main():
    graph = FigGeo("graph.yaml")
    print("Piensa en una figura geométrica.\n")
    graph.run()


if __name__ == "__main__":
    main()
