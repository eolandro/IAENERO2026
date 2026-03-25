# inicializador.py
from ruamel.yaml import YAML

class Inicializador:
    def __init__(self):
        self.yaml = YAML()
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.animales = []
        self.respuestas = {'s': True, 'n': False}

    def preguntar_si_no(self, mensaje):
        while True:
            resp = input(f"{mensaje} (s/n): ").strip().lower()
            if resp in self.respuestas:
                return self.respuestas[resp]
            print("  Responde 's' o 'n'")

    def ejecutar(self):
        print("=" * 60)
        print(" INICIALIZADOR DE BASE DE CONOCIMIENTO")
        print("=" * 60)

        # Cantidad de animales
        while True:
            try:
                num = int(input("\n ¿CUÁNTOS ANIMALES? (mínimo 6): "))
                if num >= 6:
                    break
                print(f" mínimo 6 (diste {num})")
            except ValueError:
                print(" número válido")

        # Evitar duplicados automáticamente
        todas_caracts = set()

        # Ciclo por cada animal
        for i in range(num):
            print(f"\n--- Animal {i+1}/{num} ---")
            nombre = input("  Nombre: ").strip().lower()
            while not nombre:
                nombre = input("  Nombre (obligatorio): ").strip().lower()


            carac = input(f"  Una característica de {nombre}: ").strip().lower()
            while not carac:
                carac = input(f"  Característica (obligatoria): ").strip().lower()

            # Dejamos la caracteristica inicial vacia
            todas_caracts.add(carac)
            self.animales.append({
                "nombre": nombre,
                "caracteristicas": {carac: None}
            })

        todas_caracts = sorted(todas_caracts)


        print("\n Completar matriz (responde 's' o 'n')")
        for animal in self.animales:
            print(f"\n {animal['nombre'].upper()}")
            caracteristicas_completas = {}

            # Preguntar todas las caracterisiticas
            for carac in todas_caracts:
                valor = self.preguntar_si_no(f"  ¿{carac}?")
                caracteristicas_completas[carac] = valor

            animal["caracteristicas"] = caracteristicas_completas

        print("\n" + "=" * 60)
        print(" MATRIZ DE CARACTERÍSTICAS")
        print("=" * 60)

        # Encabezado
        print(f"{'Animal':<12}", end="")
        for c in todas_caracts:
            print(f"{c[:8]:>8}", end="")
        print("\n" + "-" * 60)

        # Datos
        for animal in self.animales:
            print(f"{animal['nombre']:<12}", end="")
            for c in todas_caracts:
                valor = animal['caracteristicas'][c]
                print(f"{'1' if valor else '0':>8}", end="")
            print()

        #  Guardar YAML
        datos = {
            "metadata": {
                "nombre": "Base de conocimiento - Animales",
                "version": "1.0",
                "num_animales": len(self.animales),
                "total_caracts": len(todas_caracts),
            },
            "caracteristicas_generales": todas_caracts,
            "animales": self.animales
        }

        with open("animales.yaml", 'w', encoding='utf-8') as f:
            self.yaml.dump(datos, f)

        print(f"\n Guardado en 'animales.yaml'")
        print(f"   Animales: {len(self.animales)}")
        print(f"   Características: {len(todas_caracts)}")
        print(f"   Total valores: {len(self.animales) * len(todas_caracts)}")

if __name__ == "__main__":
    inicializador = Inicializador()
    inicializador.ejecutar()

