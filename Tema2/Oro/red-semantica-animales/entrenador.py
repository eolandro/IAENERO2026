from ruamel.yaml import YAML
import math

class Entrenador:

    def __init__(self, archivo_entrada="animales.yaml"):
        self.yaml = YAML()
        self.archivo = archivo_entrada

    def cargar_datos(self):
        with open(self.archivo, 'r', encoding='utf-8') as f:
            return self.yaml.load(f)

    def asignar_pesos_potencia2(self, caracteristicas):
        pesos = {}

        # pesos = {aulla': 1, 'carreras': 2}
        for i, carac in enumerate(caracteristicas):
            pesos[carac] = 2 ** i
        return pesos

    def calcular_valor_animal(self, animal, pesos):
        valor = 0
        for carac, peso in pesos.items():
            if carac in animal['caracteristicas'] and animal['caracteristicas'][carac]:
                valor += peso
        return valor

    def entrenar(self):
        print("=" * 60)
        print(" ENTRENADOR DE BASE DE CONOCIMIENTO  ")
        print("=" * 60)

        datos = self.cargar_datos()
        lista_caracteristicas = datos['caracteristicas_generales']
        animales = datos['animales']


        pesos = self.asignar_pesos_potencia2(lista_caracteristicas)

        # Calcular valor  para cada animal
        animales_con_valor = []
        for animal in animales:
            valor = self.calcular_valor_animal(animal, pesos)

            animales_con_valor.append({
                'nombre': animal['nombre'],
                'valor': valor,
                'caracteristicas': animal['caracteristicas'].copy() # Copy para guardar los datos reales no la referencia
            })

        animales_ordenados = sorted(animales_con_valor,
                                   key=lambda x: x['valor'],
                                   reverse=True)


        print("\n" + "=" * 60)
        print(" TABLA DE ANIMALES ORDENADA POR PESO (MAYOR -> MENOR)")
        print("=" * 60)

        print(f"{'#':<3} {'Animal':<12} {'Valor':<8} Características")
        print("-" * 60)


        for i, animal in enumerate(animales_ordenados):
            activas = [c for c, v in animal['caracteristicas'].items() if v]
            activas_str = ', '.join(activas)[:40]
            print(f"{i+1:<3} {animal['nombre']:<12} {animal['valor']:<8}  {activas_str}")


        # Guardar base entrenada
        datos_entrenados = {
            "metadata": {
                "nombre": "Base de conocimiento ENTRENADA",
                "version": "2.0",
                "num_animales": len(animales),
                "num_caracteristicas": len(lista_caracteristicas),
                "metodo_pesos": "potencias_de_2"
            },
            "caracteristicas": lista_caracteristicas,
            "pesos": pesos,
            "animales": animales_ordenados,
            "tabla_referencia": {
                "max_valor": 2**len(lista_caracteristicas) - 1,
                "bits_necesarios": len(lista_caracteristicas),
                "valores_posibles": 2**len(lista_caracteristicas)
            }
        }

        # Guardar archivo entrenado
        with open("animales_entrenados.yaml", 'w', encoding='utf-8') as f:
            self.yaml.dump(datos_entrenados, f)

        print(f"\n" + "=" * 60)
        print(" ENTRENAMIENTO COMPLETADO")
        print("=" * 60)
        print(f"    Archivo guardado: 'animales_entrenados.yaml'")


if __name__ == "__main__":
    entrenador = Entrenador()
    entrenador.entrenar()
