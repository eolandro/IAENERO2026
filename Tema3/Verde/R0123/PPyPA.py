import json

def pp(inicio,fin,grafo_):
    with open(grafo_, 'r') as json_:
        grafo = json.load(json_)

    pila = [(grafo, False)]

    while pila:
        nodo, empezar = pila.pop()
        if nodo["name"] == inicio:
            empezar = True
        if empezar and nodo["name"] == fin:
            return True
        if empezar or nodo["name"] != inicio:
            hijos = nodo.get("children", [])
            for i in range(len(hijos)-1, -1, -1):
                pila.append((hijos[i], empezar))

    return False

def pa(inicio,fin,grafo_):
    with open(grafo_, 'r') as json_:
        grafo = json.load(json_)

    cola = [(grafo, False)]
    while cola:
        nodo, empezar = cola.pop(0)
        if nodo["name"] == inicio:
            empezar = True
        if empezar and nodo["name"] == fin:
            return True
        if empezar or nodo["name"] != inicio:
            hijos = nodo.get("children", [])
            for hijo in hijos:
                cola.append((hijo, empezar))

    return False

def main():
    print("\n Ingrese: pp(inicial,final,grafo.json) - ejemplo: pp('A','AC','grafo.json')")
    print(" Ingrese: pa(inicial,final,grafo.json) - ejemplo: pa('A','AC','grafo.json')")
    print(" Salir ingrese bye\n")
    while True:
        R = input(' >> ')
        if R == 'bye':
            break
        print(eval(R))

if __name__=='__main__':
    main()
