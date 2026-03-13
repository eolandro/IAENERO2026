# Adivinador de animales
import json
import pandas as pd


class Adivinador:
    def __init__(self):
        self.df = None

    def procesar_matriz_json(self, nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            self.df = pd.DataFrame(datos)
            print(" --- Matriz Cargada --- ")
            print(self.df)

    def validador(self, tipo, mensaje):
        while True:
            try:
                valor = tipo(input(mensaje))
                return valor
            except ValueError:
                print(f" Por favor, ingresa un valor válido del tipo {tipo.__name__}. ")

    def jugar_adivinanza(self):
        caracteristicas = [
            c for c in self.df.columns if c not in ["animal", "peso_total"]
        ]
        i = 0
        while len(self.df) > 1 and i < len(caracteristicas):
            col = caracteristicas[i]
            # Valores únicos en la columna actual
            valores_unicos = self.df[col].unique()
            # Todos iguales, ignorar
            if len(valores_unicos) == 1:
                i += 1
                continue
            respuesta = self.validador(int, f"¿El animal tiene {col}? (0/1): ")
            # Depurado
            self.df = self.df[self.df[col] == respuesta]
            if self.df.empty:
                print("No encontré ningún animal con esas características.")
                return
            print(f"Animales restantes: {self.df['animal'].tolist()}")
            i += 1

        # Fin
        if len(self.df) == 1:
            print(
                f"\n El animal en el que estás pensando es: {self.df.iloc[0]['animal']} "
            )
        elif len(self.df) > 1:
            print(f"\nTodavía tengo dudas entre: {self.df['animal'].tolist()}")
            lista_final = self.df["animal"].tolist()
            encontrado = False
            # Animales restantes
            for j in range(len(lista_final) - 1):
                confirmacion = self.validador(
                    int, f"¿Es un {lista_final[j]}? (0: No / 1: Sí): "
                )
                if confirmacion == 1:
                    print(f"\n Tu animal es: {lista_final[j]}")
                    encontrado = True
                    break
            # Descarte final
            if not encontrado:
                print(f"\n Descarte, tu animal es: {lista_final[-1]}")


objadi = Adivinador()
objadi.procesar_matriz_json("matriz_ordenada.json")
objadi.jugar_adivinanza()
