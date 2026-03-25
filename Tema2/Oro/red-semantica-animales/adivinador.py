from ruamel.yaml import YAML
import math

class Adivinador:

    def __init__(self, archivo_entrada="animales_entrenados.yaml"):
        self.yaml = YAML()
        self.archivo = archivo_entrada


    def cargar_datos(self):
        with open(self.archivo, 'r', encoding='utf-8') as f:
            return self.yaml.load(f)


    def calcular_ganancia_informacion(self,animales_posibles,carac):

        animal_si = 0
        animal_no = 0

        entropia_inicial = -(len(animales_posibles)) * (1/len(animales_posibles)) * math.log2(1/len(animales_posibles))

        for  animal in animales_posibles:

            #print(animal['nombre'], carac, animal['caracteristicas'][carac])

            if carac in animal['caracteristicas'] and animal['caracteristicas'][carac]:
                animal_si += 1
            else:
                animal_no += 1


        if animal_si == 0:
            entropia_si = 0
        else:
            entropia_si = -animal_si * (1/animal_si) * math.log2(1/animal_si)

        if animal_no == 0:
            entropia_no = 0
        else:
            entropia_no = -(animal_no) * (1/animal_no) * math.log2(1/animal_no)

        entropia_promedio = ((animal_si/len(animales_posibles)) * entropia_si)  + ((animal_no/len(animales_posibles)) * entropia_no)
        ganancia = entropia_inicial - entropia_promedio

        #print(ganancia,"\n")
        return ganancia


    def obtener_mejor_caracteristica(self,Lista_carac,animales_posibles):

        mejor_caracteristica = ""
        mayor_ganancia = -1

        for c in  Lista_carac:
            ganancia = self.calcular_ganancia_informacion(animales_posibles,c)

            if ganancia > mayor_ganancia:
                mayor_ganancia = ganancia
                mejor_caracteristica = c

        return mejor_caracteristica


    def adivinar(self):

        datos = self.cargar_datos()
        animales_posibles = datos['animales']
        Lista_carac = datos['caracteristicas']
        preguntas_hechas = []

        while (len(animales_posibles)>1):

            carac_disponibles = [c for c in Lista_carac if c not in preguntas_hechas]

            if not carac_disponibles:
                break

            mejor_caracteristica = self.obtener_mejor_caracteristica(carac_disponibles,animales_posibles)
            preguntas_hechas.append(mejor_caracteristica)

            r = input(f"Tu animal tiene la carcacterisitca de {mejor_caracteristica} (S/N) ").strip().upper()

            if r == 'S':
                animales_posibles = [animal for animal in animales_posibles if animal['caracteristicas'][mejor_caracteristica] == True]
                print(animales_posibles)
            else:
                # Filtra animales que NO tienen la característica = False
                animales_posibles = [animal for animal in animales_posibles if animal['caracteristicas'][mejor_caracteristica] == False]
                #print(animales_posibles)


        if len(animales_posibles) == 1:
            print(f" ¡ADIVINÉ! El animal que pensaste es: {animales_posibles[0]['nombre'].upper()}")

        elif len(animales_posibles) == 0:
            print(" No encontré ningún animal con esas características.")

if __name__ == "__main__":
    adivino = Adivinador()
    adivino.adivinar()




"""
Animales ovíparos (SÍ): quetzal, sapo, gallina → 3 animales
Animales no ovíparos (NO): los otros 9 animales

Entropía del grupo SÍ = -3 × (1/3 × log₂(1/3)) = 1.58 bits
Entropía del grupo NO = -9 × (1/9 × log₂(1/9)) = 3.17 bits

Entropía promedio después = (3/12)×1.58 + (9/12)×3.17 = 2.77 bits

GANANCIA = Entropía inicial - Entropía promedio
         = 3.58 - 2.77 = 0.81 bits
"""


"""
Para CADA pregunta que harás:
1. Toma el conjunto ACTUAL de animales posibles
2. Para CADA característica no preguntada aún:
   - Cuenta cuántos animales tienen SÍ esa característica
   - Cuenta cuántos tienen NO
   - Evalúa qué TAN BALANCEADA es la división
3. Elige la característica con la división MÁS BALANCEADA
4. Haz la pregunta sobre ESA característica
5. Según respuesta, filtra el conjunto
6. Repite hasta tener 1 animal
"""
