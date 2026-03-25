# detokenizador.py
from ruamel.yaml import YAML
import spacy
import sys
import re

class Detokenizador:

    def __init__(self, archivo_entrada="base_mensajes.yaml"):
        self.yaml = YAML()
        self.archivo = archivo_entrada
        self.nlp = spacy.load("es_core_news_sm")
        # Patrón para detectar URLs y dominios
        self.url_pattern = re.compile(r'https?://|www\.|\.[a-z]{2,}/|\.com|\.net|\.org', re.IGNORECASE)

    def cargar_datos(self):
        with open(self.archivo, 'r', encoding='utf-8') as f:
            data = self.yaml.load(f)
            return data['mensajes_etiquetados']

    def es_url_o_dominio(self, token):
        token_text = token.text.lower()
        if self.url_pattern.search(token_text):
            return True
        # Verificar si tiene puntos y es alfanumérico (probable dominio)
        if '.' in token_text and len(token_text) > 3:
            # Si tiene formato de dominio
            parts = token_text.split('.')
            if len(parts) >= 2 and len(parts[-1]) in [2, 3, 4]:  # .com, .net, .org, .es, etc.
                return True
        return False

    def extraer_tokens(self, texto):
        if not isinstance(texto, str):
            return []

        doc = self.nlp(texto.lower())
        tokens_relevantes = []

        for token in doc:

            if self.es_url_o_dominio(token):
                continue

            if token.like_num or (token.text.isdigit() or
                (len(token.text) > 0 and token.text.replace('.', '').replace(',', '').isdigit())):
                continue

            # Mantener solo sustantivos, verbos, adjetivos y nombres propios
            if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'PROPN']:
                if len(token.lemma_) >= 3:  # Ignorar palabras muy cortas
                    tokens_relevantes.append(token.lemma_)

        return tokens_relevantes

    def calcular_probabilidades_condicionales(self, mensajes):

        total_mensajes = len(mensajes)

        # Contar cuantos mensajes son spam y cuales no
        total_spam = 0
        for mensaje in mensajes:
            if mensaje.get('spam') == 1:
                total_spam += 1

        total_no_spam = total_mensajes - total_spam

        # Probabilidades a priori
        probabilidad_spam = total_spam / total_mensajes if total_mensajes > 0 else 0
        probabilidad_no_spam = total_no_spam / total_mensajes if total_mensajes > 0 else 0

        # CONTAR LA FRECUENCIA DE LOS TOKENS(PALABRAS)
        frecuencia_spam = {}
        frecuencia_no_spam = {}

        for mensaje_actual in mensajes:
            texto = mensaje_actual.get('mensaje', '')
            palabras = self.extraer_tokens(texto)

            es_spam = mensaje_actual.get('spam')

            if es_spam == 1:
                #  contar palabras en frecuencia_spam
                for palabra in palabras:
                    frecuencia_spam[palabra] = frecuencia_spam.get(palabra, 0) + 1
            else:
                #  contar palabras en frecuencia_no_spam
                for palabra in palabras:
                    frecuencia_no_spam[palabra] = frecuencia_no_spam.get(palabra, 0) + 1

        # CALCULAR LAS PROBABILIDADES CONDICIONALES
        todas_las_palabras = set(frecuencia_spam.keys()) | set(frecuencia_no_spam.keys())

        # Diccionario  P(Spam | Palabra)
        probabilidad_spam_por_palabra = {}

        # Suavizado Laplace
        SMOOTHING = 1

        for palabra in todas_las_palabras:
            conteo_spam = frecuencia_spam.get(palabra, 0)
            conteo_no_spam = frecuencia_no_spam.get(palabra, 0)

            # Calcular P(Palabra | Spam)  ¿Qué tan probable es ver esta palabra en un mensaje spam?
            prob_palabra_dado_spam = (conteo_spam + SMOOTHING) / (total_spam + 2 * SMOOTHING)

            # Calcular P(Palabra | No Spam) ¿Qué tan probable es ver esta palabra en un mensaje no spam?
            prob_palabra_dado_no_spam = (conteo_no_spam + SMOOTHING) / (total_no_spam + 2 * SMOOTHING)

            # Teorema de Bayes

            #           [P(Palabra|Spam) * P(Spam)]
            # ------------------------------------------------------
            #[P(Palabra|Spam)*P(Spam) + P(Palabra|NoSpam)*P(NoSpam)]

            numerador = prob_palabra_dado_spam * probabilidad_spam
            denominador = numerador + (prob_palabra_dado_no_spam * probabilidad_no_spam)

            # Evitar división por cero
            if denominador == 0:
                prob_spam_si_palabra = 0.5
            else:
                prob_spam_si_palabra = numerador / denominador

            probabilidad_spam_por_palabra[palabra] = prob_spam_si_palabra

        try:
            with open("tokens.yaml", 'w', encoding='utf-8') as archivo:
                self.yaml.dump(probabilidad_spam_por_palabra, archivo)
        except Exception as error:
            print(f"Error al guardar el archivo: {error}")

    def ejecutar(self):
        mensajes = self.cargar_datos()
        probabilidades = self.calcular_probabilidades_condicionales(mensajes)
        print(f"\n Archivo 'tokens.yaml' generado correctamente")

if __name__ == "__main__":
    detoken = Detokenizador()
    detoken.ejecutar()
