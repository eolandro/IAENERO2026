import re
import nltk
from nltk.corpus import stopwords


class TextProcessor:
    def __init__(self):
        """Este metodo es el encargado de identificar las "stopwords",usando una tabla manual y la libreria
        NLTK para refinar el resultado"""
        self.stopwords_manual = {
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
            "de",
            "del",
            "a",
            "ante",
            "con",
            "contra",
            "desde",
            "durante",
            "en",
            "entre",
            "hacia",
            "hasta",
            "para",
            "por",
            "segun",
            "sin",
            "sobre",
            "tras",
            "y",
            "o",
            "pero",
            "aunque",
            "si",
            "que",
            "como",
            "muy",
            "ya",
            "tambien",
            "solo",
            "aqui",
            "alli",
            "ahi",
            "este",
            "esta",
            "estos",
            "estas",
            "ese",
            "esa",
            "eso",
            "mi",
            "tu",
            "su",
            "sus",
            "lo",
            "le",
            "les",
        }

        nltk.download("stopwords", quiet=True)
        self.stopwords_nltk = set(stopwords.words("spanish"))

    def tokenizar(self, texto):
        """Este metodo, apesar de enfocarse como parte esencial del detokenizador, se ocupa de igual manera
        para el clasificador, el cual se encarga del filtrado de stopwords"""
        texto = texto.lower()

        palabras = re.findall(r"\b\w+\b", texto)
        tokens = [p for p in palabras if p not in self.stopwords_manual]
        tokens = [p for p in tokens if p not in self.stopwords_nltk]
        tokens = [t for t in tokens if len(t) > 2]
        return tokens
