# import re
# import nltk
# from nltk.corpus import stopwords
# from ruamel.yaml import YAML

# Se reemplazaron las importaciones por clases para que el programa sea mas accesible
# (Insisto, espero que asi sea)
from class_prob.file_manager import FileManager
from class_prob.text_processor import TextProcessor


class Clasificador:
    def __init__(self, archivo_prob, archivo_msj):
        self.archivo_prob = archivo_prob
        self.archivo_msj = archivo_msj
        self.tabla = {}
        self.mensajes = []
        self.resultados = []

        # De legado: La tabla de stopwords y nltk se movieron a la importacion
        # "TextProcessor"
        self.processor = TextProcessor()

    def cargar_probabilidades(self):
        data = FileManager.read_yaml(self.archivo_prob)
        self.tabla = data["tokens"]

    def cargar_mensajes(self):
        self.mensajes = FileManager.read_txt(self.archivo_msj)

    def clasificar(self):
        # El umbral se modifica dependiendo de la sensibilidad
        # para clasificar los nuevos mensajes
        umbral = 0.05

        for msj in self.mensajes:
            # De legado: El proceso de refinar se movio a la importacion
            # "TextProcessor", esto conlleva a:
            # Stopwords_manual, NLTK, tokens con len <=2
            tokens = self.processor.tokenizar(msj)
            probabilidades = []

            for t in tokens:
                if t in self.tabla:
                    prob = self.tabla[t]["prob_spam"]
                    probabilidades.append(prob)

            if probabilidades:
                promedio = sum(probabilidades) / len(probabilidades)
                # El metodo de concenso es Promedio de Probabilidad
                decision = promedio >= umbral
            else:
                decision = False

            self.resultados.append({"texto": msj, "spam": decision})

    def guardar_yaml(self, salida="clasificados.yaml"):
        data = {"msj_clasificados": self.resultados}
        FileManager.write_yaml(salida, data)
        print(f"\nArchivo generado: {salida}")
        # Nota para mi mismo: ... Creo que ya sabes lo que pasa hasta aca.

    def vivemuere(self):
        self.cargar_probabilidades()
        self.cargar_mensajes()
        self.clasificar()
        self.guardar_yaml()


if __name__ == "__main__":
    clas = Clasificador("probabilidades.yaml", "msjforeval.txt")
    clas.vivemuere()
