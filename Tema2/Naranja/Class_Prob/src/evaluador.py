# from ruamel.yaml import YAML

# Se cambio la importación para mas accesibilidad hacia los programas anteriores
from class_prob.file_manager import FileManager


class Evaluador:
    def __init__(self, archivo_clasificados):
        self.archivo_clasificados = archivo_clasificados
        self.mensajes = []
        self.resultados = []

        # TP -> True positive
        self.TP = 0

        # TN -> True Negative
        self.TN = 0

        # FP -> False Positive
        self.FP = 0

        # FN -> False Negative
        self.FN = 0

    def loadclasificados(self):
        data = FileManager.read_yaml(self.archivo_clasificados)
        self.mensajes = data["msj_clasificados"]

    def evaluacion(self):
        print("\n===== Evaluación =====\n")
        print(
            "\n Esta vez tienes que elegir si los mensajes mostrados son SPAM o no \n"
        )

        for i, item in enumerate(self.mensajes, start=1):
            texto = item["texto"]
            pred = item["spam"]

            while True:
                print(f"\nMensaje {i}:\n{texto}\n")
                resp = input("¿Es spam real? (s/n): ").lower().strip()

                if resp in ["s", "n"]:
                    real = True if resp == "s" else False
                    break
                else:
                    print("Respuesta inválida. Use 's' o 'n'.")

            if pred and real:
                self.TP += 1
            elif not pred and not real:
                self.TN += 1
            elif pred and not real:
                self.FP += 1
            elif not pred and real:
                self.FN += 1

            self.resultados.append(
                {"texto": texto, "spam_predicho": pred, "spam_real": real}
            )

    def metricas(self):
        total = self.TP + self.TN + self.FP + self.FN
        accuracy = (self.TP + self.TN) / total if total else 0
        precision = self.TP / (self.TP + self.FP) if (self.TP + self.FP) else 0
        recall = self.TP / (self.TP + self.FN) if (self.TP + self.FN) else 0
        prevalence = (self.TP + self.FN) / total if total else 0
        return accuracy, precision, recall, prevalence

    # Nota a mi mismo, puede y solo puede que las impresiones largas las pueda mover a otro lugar
    def impresultados(self):
        accuracy, precision, recall, prevalence = self.metricas()
        print("\n===== MATRIZ DE CONFUSIÓN =====\n")

        print(f"TP: {self.TP}")
        print(f"TN: {self.TN}")
        print(f"FP: {self.FP}")
        print(f"FN: {self.FN}")

        print("\n===== TABLA =====\n")
        print("                REAL")
        print("             Spam   NoSpam")
        print(f"PRED Spam      {self.TP}      {self.FP}")
        print(f"PRED NoSpam    {self.FN}      {self.TN}")

        print("\n===== MÉTRICAS =====\n")
        print(f"Accuracy   : {accuracy:.2f}")
        print(f"Precision  : {precision:.2f}")
        print(f"Recall     : {recall:.2f}")
        print(f"Prevalence : {prevalence:.2f}")

        return accuracy, precision, recall, prevalence

    def saveyaml(self):
        accuracy, precision, recall, prevalence = self.metricas()

        # Para debug//logs: rescomparador muestra las comparaciones entre la respuesta del supervisor
        # contra el archivo de clasificación.
        FileManager.write_yaml("rescomparador.yaml", {"evaluacion": self.resultados})

        evaluacion = {
            "confusion_matrix": {
                "TP": self.TP,
                "TN": self.TN,
                "FP": self.FP,
                "FN": self.FN,
            },
            "metrics": {
                "accuracy": round(accuracy, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "prevalence": round(prevalence, 4),
            },
        }

        # Para debug//logs: Evaluación guarda las metricas generadas para una evaluación (valga la redundancia)
        FileManager.write_yaml("evaluacion.yaml", evaluacion)

        print("\n //Para debug//logs// Archivos generados:")
        print("rescomparador.yaml")
        print("evaluacion.yaml")
        # Nota para mi mismo: Si llegamos hasta aca, significa que funcionarón los 4 programas
        # y las bibliotecas.

        # Pd. Creo que le eche mas ganas a la documentación de lo que deberia.

    def eslahoradepapear(self):
        self.loadclasificados()
        self.evaluacion()
        self.impresultados()
        self.saveyaml()


if __name__ == "__main__":
    evaluador = Evaluador("clasificados.yaml")
    evaluador.eslahoradepapear()
