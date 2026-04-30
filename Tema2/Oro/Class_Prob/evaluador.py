from ruamel.yaml import YAML

class EvaluadorSpam:
    def __init__(self, archivo_entrada="mensajes_clasificados.yaml"):
        self.yaml = YAML()
        self.archivo = archivo_entrada

    def cargar_mensajes(self):
        with open(self.archivo, 'r', encoding='utf-8') as f:
            data = self.yaml.load(f)
            return data['mensajes_etiquetados']

    def ejecutar_evaluacion(self):
        mensajes = self.cargar_mensajes()
        respuestas_usuario = []
        predicciones_clasificador = []

        print("*** INICIANDO EVALUADOR DE SPAM ***")

        print("Instrucciones: Presiona 's' para SPAM y 'n' para NO SPAM.\n")

        for i, m in enumerate(mensajes):
            texto = m.get('mensaje', '')
            juicio_clasificador = m.get('spam')

            print(f"Mensaje [{i+1}/{len(mensajes)}]:")
            print(f" > {texto}")

            opcion = ""
            while opcion not in ['s', 'n']:
                opcion = input("¿Es spam? (s/n): ").lower()

            juicio_supervisor = 1 if opcion == 's' else 0
            respuestas_usuario.append(juicio_supervisor)
            predicciones_clasificador.append(juicio_clasificador)
            print("-" * 30)

        self.calcular_estadisticas(respuestas_usuario,predicciones_clasificador)

    def calcular_estadisticas(self, reales, predicciones):
        vp = vn = fp = fn = 0

        for r, p in zip(reales, predicciones):
            if r == 1 and p == 1: vp += 1
            if r == 0 and p == 0: vn += 1
            if r == 0 and p == 1: fp += 1
            if r == 1 and p == 0: fn += 1

        total = len(reales)

        # Cálculos con manejo de división por cero
        accuracy = (vp + vn) / total if total > 0 else 0
        precision = vp / (vp + fp) if (vp + fp) > 0 else 0
        recall = vp / (vp + fn) if (vp + fn) > 0 else 0
        prevalence = (vp + fn) / total if total > 0 else 0

        print("\n" + "="*30)
        print(" RESULTADOS DE LA EVALUACIÓN")
        print("="*30)
        print(f"Matriz de Confusión: VP={vp}, VN={vn}, FP={fp}, FN={fn}")
        print("-" * 30)
        print(f"Accuracy:   {accuracy:.2%}")
        print(f"Precision:              {precision:.2%}")
        print(f"Recall:  {recall:.2%}")
        print(f"Prevalence: {prevalence:.2%}")
        print("="*30)

if __name__ == "__main__":
    evaluador = EvaluadorSpam()
    evaluador.ejecutar_evaluacion()
