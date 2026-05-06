"""
    A* 
    La eficacia del algoritmo A* procede de su evaluación inteligente de trayectorias
    mediante tres componentes clave: g(n), h(n) y f(n). Estos componentes trabajan 
    juntos para guiar el proceso de búsqueda hacia los caminos más prometedores.

    * Coste del camino g(n)
    * Función heurística h(n)
    * Coste total estimado f(n)

"""

import json
import math 
import matplotlib.pyplot as plt
import numpy as np

def mostrar_mapa_con_ruta(mapa, ruta, inicio, goal):
    # Convertir a numpy array
    mapa_np = np.array(mapa, dtype=float)
    
    # Crear matriz de colores: 0=blanco, 1=negro
    colores = np.where(mapa_np == 1, 0, 1)  # 1=libre, 0=obstáculo
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Mostrar mapa
    cmap = plt.cm.colors.ListedColormap(['#2B2B2B', '#F5F5F5'])
    ax.imshow(colores, cmap=cmap, origin='upper')
    
    # Marcar ruta
    for i, (f, c) in enumerate(ruta):
        if (f, c) != tuple(inicio) and (f, c) != tuple(goal):
            ax.add_patch(plt.Circle((c, f), 0.3, color='#3498DB', alpha=0.7))
    
    # Marcar inicio
    ax.add_patch(plt.Circle((inicio[1], inicio[0]), 0.4, color='#2ECC71', alpha=0.8))
    ax.text(inicio[1], inicio[0], 'INICIO', ha='center', va='center', fontsize=8, color='white', weight='bold')
    
    # Marcar goal
    ax.add_patch(plt.Circle((goal[1], goal[0]), 0.4, color='#E74C3C', alpha=0.8))
    ax.text(goal[1], goal[0], 'BOMBA', ha='center', va='center', fontsize=8, color='white', weight='bold')
    
    # Configurar grid
    ax.set_xticks(np.arange(-0.5, len(mapa[0]), 1))
    ax.set_yticks(np.arange(-0.5, len(mapa), 1))
    ax.grid(True, color='gray', linestyle='-', linewidth=0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    plt.title(f'Ruta A* - Costo: {len(ruta)-1} pasos', fontsize=14, weight='bold')
    plt.tight_layout()
    plt.show()


def buscar_objetivo(tablero,target):
    f = 0
    while True:
        if target in tablero[f]:
            c = tablero[f].index(target)
            return f,c
        else:
            f += 1
    
def A_Star(boome,goal,mapa,Lista_abierta,Lista_cerrada): 
    f, c = boome['c_nodo']

    # Estos son los posbiles movimientos que pueden ser 
    movs_adyacentes = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(1,-1),(1,1),(-1,1)]          
    vecinos = []

    for m in range (len(movs_adyacentes)):
        f_nueva = f + movs_adyacentes[m][0]
        c_nueva = c + movs_adyacentes[m][1]

        # Obtener las coordenadas de los  nodos ya visitados
        coords_cerradas = [nodo['c_nodo'] for nodo in Lista_cerrada]

        # Obtener las coordenadas de la lista abierta
        coords_abiertas = [n['c_nodo'] for n in Lista_abierta]
       
        # Descartar que este fuera de los bordes y que no haya obstaculos y no este en la ListaCerrada
        if (f_nueva<= 4 and f_nueva>=0) and (c_nueva<= 9 and c_nueva>=0) and (mapa[f_nueva][c_nueva] == 0) and  ((f_nueva, c_nueva) not in coords_cerradas) :
            
            # Solo para ver el costo de moverse desde el origen hacia los vecinos
            if m > 3:
                g_actual = 14
            else:
                g_actual = 10

            # Calculo del costo
            g_nodo = boome['g_nodo'] + g_actual
            # Calculo de la heuristica
            h_nodo = 10 * max(abs(f_nueva - goal[0]), abs(c_nueva - goal[1]))
            # Calculo del f_nodo
            f_nodo = g_nodo + h_nodo
            
            if (f_nueva, c_nueva)  not in coords_abiertas:
                vecino = {'c_nodo': (f_nueva,c_nueva), 'g_nodo':g_nodo, 'h_nodo':h_nodo, 'f':f_nodo, 'padre': boome }
                vecinos.append(vecino)

            else:

                for pos, nodo in enumerate(Lista_abierta):
                    if nodo['c_nodo'] == (f_nueva, c_nueva):
                        break

                g_nodo_anterior = Lista_abierta[pos]['g_nodo']
                
                if g_nodo < g_nodo_anterior:
                    Lista_abierta[pos]['g_nodo'] = g_nodo
                    Lista_abierta[pos]['h_nodo'] = h_nodo
                    Lista_abierta[pos]['f'] = f_nodo
                    Lista_abierta[pos]['padre'] = boome
    return vecinos

with open('tablero.json', 'r', encoding='utf-8') as file:
    datos = json.load(file)
    mapa = datos['mapa']

    fb, cb = buscar_objetivo(mapa, "B")
    fg, cg = buscar_objetivo(mapa, "G")

    # Limpiar el mapa
    mapa = [[0 if celda in ("B", "G") else celda for celda in fila] for fila in mapa]

    boome = {'c_nodo': (fb, cb), 'g_nodo': 0, 'f': 0}
    goal = (fg, cg)
    Lista_abierta = [boome]
    Lista_cerrada = []

while Lista_abierta:
    
    current = Lista_abierta[0]
    Lista_abierta.pop(0)
    Lista_cerrada.append(current)
    
    if current['c_nodo'] == goal:
        break
    
    vecinos = A_Star(current, goal, mapa, Lista_abierta, Lista_cerrada)
    Lista_abierta.extend(vecinos)
    Lista_abierta = sorted(Lista_abierta, key=lambda x: x['f'])

if current['c_nodo'] == goal:
    print("\n=== BOMBA ENCONTRADA ===")
    # Reconstruir ruta
    camino = []
    nodo = current
    while nodo:
        camino.append(nodo['c_nodo'])
        nodo = nodo.get('padre')
    camino.reverse()
    print(f"Ruta: {camino}")
    print(f"Pasos: {len(camino)-1}")
    print(f"Costo: {current['g_nodo']}")
    mostrar_mapa_con_ruta(mapa, camino, (fb,cb), goal)
else:
    print("\n=== NO HAY RUTA DISPONIBLE ===")
    print(f"No se pudo llegar a {goal}")