import random
import json

def hill(inicio, final, grafo_,steps):
    with open(grafo_, 'r') as json_:
        grafo = json.load(json_)

    visitados = []

    for paso in range(steps+1):
        visitados.append(inicio)
        print(f"Actual: {inicio}")
        if inicio == final:
            return True
        # Obtener vecinos
        vecinos = list(grafo.get(inicio, {}).items())  # (nodo, peso)
        if not vecinos:
            return False
        # Evitar ciclos recientes
        vecinos = [(v, val) for v, val in vecinos if v not in visitados[-2:]]
        if not vecinos:
            return False
        # Elegir mejor vecino
        mejor = vecinos[0]
        for vecino, valor in vecinos:
            if valor < mejor[1]:
                mejor = (vecino, valor)
            elif valor == mejor[1]:
                mejor = random.choice([mejor, (vecino, valor)])

        #print(f"Elegido: {mejor[0]} con valor {mejor[1]}")

        inicio = mejor[0]

        # Limitar memoria de 3
        if len(visitados) > 3:
            visitados = visitados[-3:]
    print("Se alcanzó el límite de pasos")
    return False

def main():
    print(" Ingrese: hill(inicial,final,grafo2.json,pasos) - ejemplo: hill('A','J','grafo2.json',5)")
    print(" Salir ingrese bye\n")
    while True:
        inicio = input(' >> ')
        if inicio == 'bye':
            break
        print(eval(inicio))

if __name__=='__main__':
    main()