# import re
# import nltk
# from nltk.corpus import stopwords
# from ruamel.yaml import YAML

# Se cambiaron las importaciones por clases que tienen
# codigo repetido para mas accesibilidad (y espero que optimización)

from class_prob.file_manager import FileManager
from class_prob.text_processor import TextProcessor
from collections import defaultdict


class DeTokenizador:
    def __init__(self, archivo_yaml):
        self.archivo_yaml = archivo_yaml
        self.mensajes = []
        self.tokens_spam = defaultdict(int)
        self.tokens_no_spam = defaultdict(int)
        # De legado: stopwords_manual y nltk se movieron a TextProcessor
        self.tabla_prob = {}
        self.processor = TextProcessor()

    def cargar_yaml(self):
        data = FileManager.read_yaml(self.archivo_yaml)
        self.mensajes = data["msj"]

    def procesar_mensajes(self):
        for item in self.mensajes:
            texto = item["texto"]
            spam = item["spam"]
            tokens = self.processor.tokenizar(texto)

            for t in tokens:
                if spam:
                    self.tokens_spam[t] += 1
                else:
                    self.tokens_no_spam[t] += 1

    def calcular_probabilidades(self):
        # Nota para mi mismo: Ya entendi el porque la probabilidad de "No-Spam" es importante,
        # si no se considera la tabla marca una probabilidad muy sesgada.
        vocabulario = set(self.tokens_spam.keys()) | set(self.tokens_no_spam.keys())

        for token in vocabulario:
            spam_freq = self.tokens_spam[token]
            no_spam_freq = self.tokens_no_spam[token]
            total = spam_freq + no_spam_freq
            prob_spam = spam_freq / total if total > 0 else 0

            self.tabla_prob[token] = {
                "prob_spam": round(prob_spam, 4),
                "spam_freq": spam_freq,
                "no_spam_freq": no_spam_freq,
            }

    def guardar_yaml(self, salida="probabilidades.yaml"):
        data = {"tokens": self.tabla_prob}
        FileManager.write_yaml(salida, data)
        # Nota para mi mismo: Si llegas hasta aqui e imprime todo
        # significa que ya estamos del otro lado...
        print(f"\nTabla de probabilidades generada: {salida}")

    def stonks(self):
        self.cargar_yaml()
        self.procesar_mensajes()
        self.calcular_probabilidades()
        # Esto solo imprime la tabla de probabilidades
        FileManager.print_prob_table(self.tabla_prob)
        self.guardar_yaml()


if __name__ == "__main__":
    detok = DeTokenizador("entrenamiento.yaml")
    detok.stonks()
