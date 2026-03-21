class Adivinador:
    def __init__(self):
        self.pregunta= { }
        self.Transcisiones= []

    def datos(self,json,param):
        self.pregunta=json
        self.Transcisiones=param

    def preguntas(self):

        origenes = [t[0] for t in self.Transcisiones]
        nodo_actual = origenes[0]  # Empezar desde el primer nodo(transación)
        R = True
        while R:
            # Si llegamos a un nodo hoja (ya no hay pregunta)
            if nodo_actual not in self.pregunta or not self.pregunta[nodo_actual].endswith('?'):
                print(f"\n Resultado: {self.pregunta.get(nodo_actual, nodo_actual)}")
                R = False
                break
            # Mostrar pregunta y las opciones posibles según las transiciones
            opciones = [t[1] for t in self.Transcisiones if t[0] == nodo_actual]
            pregunta = self.pregunta[nodo_actual]
            print(f"\n{pregunta}")
            print("Opciones:", ", ".join(opciones))
            # El while pa que pida una respuesta válida
            while True:
                respuesta = input("Elige una opción: ").strip()
                if respuesta in opciones:
                    break
                print("Opción inválida, intenta de nuevo.")
            # Buscar la transición correspondiente
            siguienteNodo = None
            for origen, condicion, destino in self.Transcisiones:
                if origen == nodo_actual and respuesta == condicion:
                    siguienteNodo = destino
                    break
            #Actualizal el nodo
            if siguienteNodo:
                nodo_actual = siguienteNodo