# clasificador.py
from ruamel.yaml import YAML
import spacy
import re
import statistics

class ClasificadorSpam:

    def __init__(self, archivo_tokens="tokens.yaml", archivo_mensajes_nuevos="nuevos_mensajes.txt"):
        self.yaml = YAML()
        self.archivo_tokens = archivo_tokens
        self.archivo_mensajes = archivo_mensajes_nuevos
        self.nlp = spacy.load("es_core_news_sm")
        self.tokens_probabilidad = {}
        self.url_pattern = re.compile(r'https?://|www\.|\.[a-z]{2,}/|\.com|\.net|\.org', re.IGNORECASE)
        self.umbral_spam = 0.51

    def cargar_probabilidades(self):
        with open(self.archivo_tokens, 'r', encoding='utf-8') as f:
            self.tokens_probabilidad = self.yaml.load(f)
        print(f"Cargadas {len(self.tokens_probabilidad)} probabilidades")
        return True

    def cargar_mensajes_nuevos(self):
        mensajes = []
        with open(self.archivo_mensajes, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        for i, linea in enumerate(lineas[:10], 1):
            mensaje = linea.strip()
            if mensaje:
                mensajes.append({
                    "numero_mensaje": i,
                    "mensaje": mensaje
                })
        print(f"Cargados {len(mensajes)} mensajes")
        return mensajes

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

    # Crear arreglo de probs por mensaje
    def calcular_probabilidad_mensaje(self, tokens):
        probabilidades = []

        for token in tokens:
            if token in self.tokens_probabilidad:
                probabilidades.append(self.tokens_probabilidad[token])
            else:
                probabilidades.append(0.5)
        if not probabilidades:
            return 0.5

        return statistics.median(probabilidades)

    def clasificar_mensaje(self, mensaje):
        tokens = self.extraer_tokens(mensaje)
        probabilidad = self.calcular_probabilidad_mensaje(tokens)
        es_spam = 1 if probabilidad >= self.umbral_spam else 0
        return es_spam, probabilidad, tokens

    def generar_salida_yaml(self, mensajes_clasificados):
        output = {
            "metadata": {
                "nombre": "Base de Mensajes Etiquetados por el Clasificador",
                "version": "1.0",
                "num_mensajes": len(mensajes_clasificados)
            },
            "mensajes_etiquetados": []
        }

        for mensaje in mensajes_clasificados:
            output["mensajes_etiquetados"].append({
                "numero_mensaje": mensaje["numero_mensaje"],
                "mensaje": mensaje["mensaje"],
                "spam": mensaje["spam_clasificado"]
            })

        with open("mensajes_clasificados.yaml", 'w', encoding='utf-8') as f:
            self.yaml.dump(output, f)

        print("Archivo generado: mensajes_clasificados.yaml")

    def mostrar_resultados(self, mensajes_clasificados):
        print("\n" + "-"*50)
        spam_count = sum(1 for m in mensajes_clasificados if m["spam_clasificado"] == 1)

        print(f"Total: {len(mensajes_clasificados)} | SPAM: {spam_count} | NO SPAM: {len(mensajes_clasificados)-spam_count}")
        print(f"Umbral: {self.umbral_spam*100}% | Método: Mediana")
        print("-"*50)

        for mensaje in mensajes_clasificados:
            estado = "SPAM" if mensaje["spam_clasificado"] == 1 else "NO SPAM"
            prob = mensaje["probabilidad"] * 100
            print(f"#{mensaje['numero_mensaje']}: {estado} ({prob:.0f}%) - {mensaje['mensaje'][:150]}")

    def ejecutar(self):
        print("Clasificador Spam - Método Mediana")
        print("-"*50)

        self.cargar_probabilidades()
        mensajes_nuevos = self.cargar_mensajes_nuevos()

        if not mensajes_nuevos:
            print("No hay mensajes para clasificar")
            return

        mensajes_clasificados = []
        for mensaje in mensajes_nuevos:
            es_spam, probabilidad, tokens = self.clasificar_mensaje(mensaje["mensaje"])
            mensajes_clasificados.append({
                "numero_mensaje": mensaje["numero_mensaje"],
                "mensaje": mensaje["mensaje"],
                "spam_clasificado": es_spam,
                "probabilidad": probabilidad,
                "tokens": tokens
            })

        self.generar_salida_yaml(mensajes_clasificados)
        self.mostrar_resultados(mensajes_clasificados)


if __name__ == "__main__":
    clasificador = ClasificadorSpam()
    clasificador.ejecutar()
