import random
import yaml
import math

# ---------------------------------
# PARÁMETROS DETERMINISTAS (Reducción de Entropía)
# ---------------------------------
P_DET_SI = 0.95   # Mayor precisión reduce el ruido
P_DET_NO = 0.05   # Menor probabilidad de falsos positivos

class Nodo:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0  
        self.h = 0  
        self.f = 0  

    def __eq__(self, otro):
        return self.pos == otro.pos

def heuristica(a, b):
    # Distancia Manhattan para cuadrículas
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(mapa, inicio, fin):
    """Implementación de A* para navegación sin desorden."""
    filas, cols = len(mapa), len(mapa[0])
    open_list = [Nodo(inicio)]
    closed_list = set()

    while open_list:
        actual = min(open_list, key=lambda n: n.f)
        open_list.remove(actual)
        closed_list.add(actual.pos)

        if actual.pos == fin:
            camino = []
            while actual:
                camino.append(actual.pos)
                actual = actual.parent
            return camino[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            v_pos = (actual.pos[0] + dx, actual.pos[1] + dy)
            
            # El valor 2 en el mapa representa un obstáculo (entropía física)
            if not (0 <= v_pos[0] < filas and 0 <= v_pos[1] < cols) or \
               mapa[v_pos[0]][v_pos[1]] == 2 or v_pos in closed_list:
                continue

            vecino = Nodo(v_pos, actual)
            vecino.g = actual.g + 1
            vecino.h = heuristica(v_pos, fin)
            vecino.f = vecino.g + vecino.h

            if any(n for n in open_list if vecino == n and vecino.g > n.g):
                continue
            open_list.append(vecino)
    return None

def actualizar_bayes(prior, real):
    # Simulamos 3 lecturas para estabilizar la probabilidad
    evidencias = [1 if (random.random() < P_DET_SI if real == 1 else random.random() < P_DET_NO) else 0 for _ in range(3)]
    p1, p0 = prior, 1 - prior
    for e in evidencias:
        if e == 1:
            p1 *= P_DET_SI
            p0 *= P_DET_NO
        else:
            p1 *= (1 - P_DET_SI)
            p0 *= (1 - P_DET_NO)
    return p1 / (p1 + p0) if (p1 + p0) > 0 else 0

def mostrar_estado(mapa, robot, visitadas, bombas):
    print("\n--- MAPA DE ESTADO ---")
    for i, fila in enumerate(mapa):
        r = ""
        for j, val in enumerate(fila):
            if (i, j) == robot: r += " R "
            elif (i, j) in bombas: r += "[X]"
            elif val == 2: r += "###"
            elif (i, j) in visitadas: r += " . "
            else: r += " - "
        print(r)

def simulador():
    with open("tablero.yaml", "r") as f:
        mapa = yaml.safe_load(f)["mapa"]
    
    filas, cols = len(mapa), len(mapa[0])
    creencias = [[0.1 for _ in range(cols)] for _ in range(filas)]
    pos_robot = (0, 0)
    visitadas, bombas_encontradas = set(), set()
    objetivos_pendientes = [(i, j) for i, r in enumerate(mapa) for j, c in enumerate(r) if c == 1]

    while objetivos_pendientes:
        # Seleccionar el objetivo más cercano 
        objetivos_pendientes.sort(key=lambda obj: heuristica(pos_robot, obj))
        meta = objetivos_pendientes[0]
        
        ruta = a_estrella(mapa, pos_robot, meta)
        if ruta:
            for paso in ruta:
                pos_robot = paso
                visitadas.add(paso)
                # Al llegar, validamos con Bayes
                if pos_robot == meta:
                    prob = actualizar_bayes(creencias[paso[0]][paso[1]], mapa[paso[0]][paso[1]])
                    if prob > 0.8:
                        bombas_encontradas.add(paso)
                        objetivos_pendientes.pop(0)
                        print(f"Bomba desactivada en {paso} con Prob: {prob:.2f}")
                mostrar_estado(mapa, pos_robot, visitadas, bombas_encontradas)
        else:
            print(f"Ruta bloqueada hacia {meta}")
            break

if __name__ == "__main__":
    simulador()