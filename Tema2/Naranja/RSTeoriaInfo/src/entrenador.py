#Entrenador
import json
import pandas as pd

class Entrenador:
    def __init__(self):
        self.matriz = []
        
    def procesar_datos(self, nombre_archivo):
        
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo) 
                df = pd.DataFrame(datos)
                print(" --- Datos Cargados --- ");
                print(df);

            #adyacencia (Crosstab)
            # Esto cruza 'animal' (filas) contra 'caracteristica' (columnas)
                self.matriz = pd.crosstab(df['animal'], df['caracteristica'])
                #Primero va la fila, despues la columna o laterabilidad,luefo va margin=True para mostrar totales, y luego va el valor de la tabla que es 1 o 0 dependiendo si coincide o no.
                #self.matriz=pd.crosstab(df['animal'], df['caracteristica'], margins=True, margins_name="Total", dropna=False)
                #El dropna=False es para incluir las filas o columnas que no tengan datos (si hay animales sin ciertas características o características sin animales).

    def validador(self, tipo, mensaje):
        while True:
            try: 
                valor = tipo(input(mensaje));
                return valor
            except ValueError:
                print(f" Por favor, ingresa un valor válido del tipo {tipo.__name__}. ");
    
    def agregar_peso(self):
        pesos = [];
        for i, col in enumerate(self.matriz.columns):
            peso = 2 ** i;
            pesos.append(peso);
        #print("Pesos de las características:", pesos)
        pesos.reverse()
        self.matriz.loc["pesos"] = pesos
        #print("Matriz con pesos agregados:")
        #print(self.matriz)
        
    def entrenador(self):
        for animal in self.matriz.index:
            for caracteristica in self.matriz.columns:
                if self.matriz.at[animal, caracteristica] == 0:
                    respuesta = self.validador(int, f"¿El animal '{animal}' tiene la característica '{caracteristica}'? (1/0): ");
                    if respuesta == 1:
                        self.matriz.at[animal, caracteristica] = 1
        self.agregar_peso();
        print("Matriz actualizada después del entrenamiento y con pesos:");
        #print("Matriz actualizada:");
        print(self.matriz);
    
    def calcular_peso(self):
        for animal in self.matriz.index[:-1]:
            peso_total = 0;
            for caracteristica in self.matriz.columns:
                if self.matriz.at[animal, caracteristica] == 1:
                    peso_total += self.matriz.at["pesos", caracteristica];
            self.matriz.at[animal, "peso_total"] = peso_total;
        print(" Matriz con peso total de cada animal: ");
        print(self.matriz);
        self.matriz = self.matriz.drop("pesos");
    
    def ordenar(self):
        self.matriz = self.matriz.sort_values(by="peso_total", ascending=False);
        print(" Matriz ordenada por peso total: ");
        print(self.matriz);
        
        
    def guardar_json(self, nombre_archivo):
        datos_json = self.matriz.reset_index().to_dict(orient='records')
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos_json, archivo, ensure_ascii=False, indent=4)
        print(f"Archivo '{nombre_archivo}' guardado exitosamente.") 

    def main(self):
        nombre_archivo = "ver1.json";
        self.procesar_datos(nombre_archivo);
        self.entrenador();
        self.calcular_peso();
        self.ordenar();
        self.guardar_json("matriz_ordenada.json");
        #Matris a excel
        self.matriz.to_excel("matriz_ordenada.xlsx", index=True);
        print("Archivo 'matriz_ordenada.xlsx' guardado exitosamente.");
        

objent = Entrenador();
objent.main();
    