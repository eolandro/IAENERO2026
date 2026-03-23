# entrenador.py
# Base de conocimiento: valores de cada animal para cada característica
# 1 = Aplica, 0 = No aplica

from inicializador import ANIMALES, CARACTERISTICAS

#Diccionario principal: animal -> {caracteristica: valor}
BASE_CONOCIMIENTO = {
    #				Colorido 	 Cuadrupedo 	 Bigotes  	  Pequeño 	   Carrera  	Construye 		Largo  	   Gordita(o) 	 Manchas  	   Aullido  	Huevo 	 Salta
    "Perro":   {  "Colorido":1, "Cuadrupedo":1, "Bigotes":1, "Pequeño":1, "Carrera":1, "Construye":0, "Largo":0, "Gordita(o)":1, "Manchas":1, "Aullido":1, "Huevo":0, "Salta":1 },
    "Gato":    {  "Colorido":1, "Cuadrupedo":1, "Bigotes":1, "Pequeño":1, "Carrera":1, "Construye":0, "Largo":0, "Gordita(o)":1, "Manchas":1, "Aullido":0, "Huevo":0, "Salta":1 },
    "Hamster": {  "Colorido":1, "Cuadrupedo":1, "Bigotes":1, "Pequeño":1, "Carrera":1, "Construye":0, "Largo":0, "Gordita(o)":1, "Manchas":0, "Aullido":0, "Huevo":0, "Salta":1 },
    "Sapo":    {  "Colorido":1, "Cuadrupedo":1, "Bigotes":0, "Pequeño":1, "Carrera":0, "Construye":0, "Largo":0, "Gordita(o)":0, "Manchas":1, "Aullido":0, "Huevo":1, "Salta":1 },
    "Caballo": {  "Colorido":1, "Cuadrupedo":1, "Bigotes":0, "Pequeño":0, "Carrera":1, "Construye":0, "Largo":0, "Gordita(o)":0, "Manchas":1, "Aullido":0, "Huevo":0, "Salta":1 },
    "Gallina": {  "Colorido":1, "Cuadrupedo":0, "Bigotes":0, "Pequeño":1, "Carrera":1, "Construye":1, "Largo":0, "Gordita(o)":1, "Manchas":1, "Aullido":0, "Huevo":1, "Salta":1 },
    "Quetzal": {  "Colorido":1, "Cuadrupedo":0, "Bigotes":0, "Pequeño":1, "Carrera":0, "Construye":0, "Largo":1, "Gordita(o)":0, "Manchas":0, "Aullido":0, "Huevo":1, "Salta":1 },
    "Huron":   {  "Colorido":0, "Cuadrupedo":1, "Bigotes":1, "Pequeño":1, "Carrera":1, "Construye":0, "Largo":1, "Gordita(o)":0, "Manchas":1, "Aullido":0, "Huevo":0, "Salta":1 },
    "Castor":  {  "Colorido":0, "Cuadrupedo":1, "Bigotes":1, "Pequeño":1, "Carrera":0, "Construye":1, "Largo":0, "Gordita(o)":1, "Manchas":0, "Aullido":0, "Huevo":0, "Salta":1 },
    "Lobo":    {  "Colorido":0, "Cuadrupedo":1, "Bigotes":1, "Pequeño":0, "Carrera":1, "Construye":0, "Largo":0, "Gordita(o)":0, "Manchas":0, "Aullido":1, "Huevo":0, "Salta":1 },
    "Vaca":    {  "Colorido":0, "Cuadrupedo":1, "Bigotes":0, "Pequeño":0, "Carrera":0, "Construye":0, "Largo":0, "Gordita(o)":1, "Manchas":1, "Aullido":0, "Huevo":0, "Salta":1 },
    "Foca":    {  "Colorido":0, "Cuadrupedo":0, "Bigotes":1, "Pequeño":0, "Carrera":0, "Construye":0, "Largo":0, "Gordita(o)":1, "Manchas":1, "Aullido":1, "Huevo":0, "Salta":1 },
}


def obtener_valor(animal: str, caracteristica: str) -> int:
    """Retorna 1 o 0 para un animal y característica dados."""
    return BASE_CONOCIMIENTO[animal][caracteristica]


def animales_con_caracteristica(caracteristica: str, valor: int, candidatos: list) -> list:
    """Filtra la lista de candidatos según si tienen o no una característica."""
    return [a for a in candidatos if BASE_CONOCIMIENTO[a][caracteristica] == valor]


def mejor_pregunta(candidatos: list, ya_preguntadas: set) -> str:
    import math

    mejor = None
    menor_impureza = float('inf')

    for carac in CARACTERISTICAS:
        if carac in ya_preguntadas:
            continue

        con_si = sum(1 for a in candidatos if BASE_CONOCIMIENTO[a][carac] == 1)
        con_no = len(candidatos) - con_si

        #Calculamos entropía: más cercano a 50/50 = mejor separación
        if con_si == 0 or con_no == 0:
            impureza = float('inf')  #Esta pregunta no divide, la descartamos
        else:
            p_si = con_si / len(candidatos)
            p_no = con_no / len(candidatos)
            impureza = -(p_si * math.log2(p_si) + p_no * math.log2(p_no))
            impureza = -impureza  #Invertimos: queremos MAXIMIZAR entropía (mínima impureza negativa)

        if impureza < menor_impureza:
            menor_impureza = impureza
            mejor = carac

    return mejor
