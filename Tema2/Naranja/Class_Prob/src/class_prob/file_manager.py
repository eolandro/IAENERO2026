from ruamel.yaml import YAML


class FileManager:
    @staticmethod
    def read_yaml(archivo):
        """Este metodo se encarga de leer cualquier archivo YAML"""
        yaml = YAML()
        with open(archivo, "r", encoding="utf-8") as f:
            data = yaml.load(f)
        return data

    @staticmethod
    def write_yaml(archivo, data):
        """Este metodo se encarga de escribir en cualquier archivo YAML"""
        yaml = YAML()
        with open(archivo, "w", encoding="utf-8") as f:
            yaml.dump(data, f)

    @staticmethod
    def read_txt(archivo):
        """Este metodo permite escribir en archivos con extension TXT"""
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = [line.strip() for line in f.readlines() if line.strip()]
        return contenido

    @staticmethod
    def print_prob_table(tabla):
        """Este metodo solo es estetico; Permite imprimir la tabla de probabilidades"""
        print("\n===== TABLA DE PROBABILIDADES =====\n")
        header = f"{'TOKEN':<15}{'P(SPAM)':<10}{'SPAM_FREQ':<12}{'NO_SPAM_FREQ'}"

        print(header)
        print("-" * len(header))

        for token, datos in sorted(tabla.items()):
            prob = datos["prob_spam"]
            spam = datos["spam_freq"]
            nospam = datos["no_spam_freq"]

            print(f"{token:<15}{prob:<10}{spam:<12}{nospam}")
