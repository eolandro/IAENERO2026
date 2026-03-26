class Adivinador:
    def __init__(self):
        # Diccionario donde:
        # clave = nodo
        # valor = pregunta o resultado
        self.pregunta = {}

        # Lista de transiciones:
        # [origen, respuesta, destino]
        self.Transcisiones = []

    def datos(self, json, param):
        # Carga los datos desde el archivo externo
        self.pregunta = json
        self.Transcisiones = param

    def preguntas(self):

        # Obtiene todos los nodos origen
        origenes = [t[0] for t in self.Transcisiones]

        # Empieza desde el primer nodo
        nodo_actual = origenes[0]

        R = True

        while R:

            # Si ya no es pregunta, es resultado final
            if nodo_actual not in self.pregunta or not self.pregunta[nodo_actual].endswith('?'):
                print(f"\n Resultado: {self.pregunta.get(nodo_actual, nodo_actual)}")
                R = False
                break

            # Obtiene las opciones posibles desde ese nodo
            opciones = [t[1] for t in self.Transcisiones if t[0] == nodo_actual]

            # Muestra la pregunta
            pregunta = self.pregunta[nodo_actual]
            print(f"\n{pregunta}")
            print("Opciones:", ", ".join(opciones))

            # Pide una respuesta válida
            while True:
                respuesta = input("Elige una opción: ").strip()
                if respuesta in opciones:
                    break
                print("Opción inválida, intenta de nuevo.")

            # Busca a qué nodo ir según la respuesta
            siguienteNodo = None
            for origen, condicion, destino in self.Transcisiones:
                if origen == nodo_actual and respuesta == condicion:
                    siguienteNodo = destino
                    break

            # Cambia al siguiente nodo
            if siguienteNodo:
                nodo_actual = siguienteNodo