# from ruamel.yaml import YAML

# Se movio la importación hacia una clase para optimizar procesos
# que existen en otros programas.
from class_prob.file_manager import FileManager


class Entrenador:
    def __init__(self, filemsj):
        self.filemsj = filemsj
        self.msj = []
        self.filtrado = []

    def load_msj(self):
        """Lee los msj desde el archivo mensajes.txt"""
        self.msj = FileManager.read_txt(self.filemsj)

        if len(self.msj) != 10:
            raise ValueError("El archivo debe contener exactamente 10 mensajes.")

    def filter_msj(self):
        """El supervisor clasifica cada mensaje"""

        print("\n--- Clasificación de Mensajes ---\n")
        print("\n Supervisor: Identifica los mensajes que sean SPAM y marcalos: \n")

        for i, msj in enumerate(self.msj, start=1):
            while True:
                print(f"Mensaje {i}: {msj}")
                resp = input("¿Es spam? (s/n): ").lower().strip()
                if resp in ["s", "n"]:
                    spam = True if resp == "s" else False
                    break
                else:
                    print("Respuesta inválida. Use 's' o 'n'.\n")

            self.filtrado.append({"texto": msj, "spam": spam})

            print()

    def savefilter(self, archivo_salida="entrenamiento.yaml"):
        """Guarda los msj etiquetados en YAML"""
        data = {"msj": self.filtrado}
        FileManager.write_yaml(archivo_salida, data)
        print(f"\nArchivo generado: {archivo_salida}")
        # Nota para mi: Si jala hasta aca, funciono la optimización

    def achambear(self):
        self.load_msj()
        self.filter_msj()
        self.savefilter()


if __name__ == "__main__":
    entrenador = Entrenador("msjtraining.txt")
    entrenador.achambear()
