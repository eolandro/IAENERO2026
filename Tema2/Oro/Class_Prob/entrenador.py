# entrenador.py
from ruamel.yaml import YAML

class Entrenador:

    def __init__(self, archivo_entrada="base_spam.txt"):
        self.yaml = YAML()
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.archivo_entrada = archivo_entrada
        self.etiquetados = []

    def cargar_datos(self):
        with open(self.archivo_entrada, 'r', encoding='utf-8') as archivo:
           lineas = archivo.readlines()
           return lineas

    def ejecutar(self):
        print("*** INICIANDO ENTRENADOR DE SPAM ***")

        lineas = self.cargar_datos()
        respuestas = {}

        for i, linea in enumerate(lineas):
            mensaje = linea.strip()
            ban = 0
            if mensaje:
                print(f"\nMensaje {i+1}: {mensaje}")
                respuesta = input("¿ES SPAM? (s/n): ").lower()

                if respuesta == 's':
                    ban = 1
                else:
                    ban = 0

                self.etiquetados.append({
                    "numero_mensaje":i+1,
                    "mensaje": mensaje,
                    "spam": ban
                })

        datos = {
            "metadata": {
                "nombre": "Base de Mensajes Clasificados",
                "version": "1.0",
                "num_mensajes": len(self.etiquetados),
            },
            "mensajes_etiquetados": self.etiquetados
        }

        with open("base_mensajes.yaml", 'w', encoding='utf-8') as f:
            self.yaml.dump(datos, f)

        print(f"\n Guardado en 'base_mensajes.yaml'")


if __name__ == "__main__":
    entrenador = Entrenador()
    entrenador.ejecutar()

