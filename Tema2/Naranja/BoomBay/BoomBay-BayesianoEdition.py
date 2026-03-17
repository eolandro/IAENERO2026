import random, numpy, secrets
from ruamel.yaml import YAML
from faker import Faker

#  R010 — Leer tablero desde archivo YAML
yaml = YAML()
yaml.default_flow_style = False
yaml.indent(sequence=4, offset=2)

s = open("./Unidad2/tablero.yaml", "r")
Data = yaml.load(s)
s.close()
print("Tablero cargado desde 'tablero.yaml'")

#  Selección de generador
def generador():
    elec = int(input("Elige un generador:\n- Random(default)(0)\n- numpy(1)\n- faker(2)\n- secrets(3)\n-----> "))
    match elec:
        case 1:
            return numpy.random.choice
        case 2:
            f = Faker()
            return f.random_element
        case 3:
            return secrets.choice
        case _:
            return random.choice

#  Listas de probabilidad del sensor
lista_bomba = [1,1,1,1,1,1,1,1,1,0]   # 90% positivo si hay bomba
lista_vacio = [0,0,0,0,0,0,0,0,1,1]   # 20% positivo si NO hay bomba

#  Cargar tabla desde YAML
tabla = []
cont_celdas = 0

for i in Data["tablero"]:
    tabla.append(i)
    cont_celdas += len(i)

cont_celdas_pas = 0

#  Probabilidades iniciales
p_bomba     = 1 / cont_celdas
p_no_bomba  = 1 - p_bomba

p_bomba_det    = {1: 0.9, 0: 0.1}   # P(det | bomba)
p_no_bomba_det = {1: 0.2, 0: 0.8}   # P(det | no bomba)

#  Visualización del tablero
def mostrar_tablero(tabla, pos_robot):
    rx, ry = pos_robot
    print()
    for x in range(len(tabla)):
        fila_str = ""
        for y in range(len(tabla[x])):
            if (x, y) == (rx, ry):
                fila_str += "🤖 "
            else:
                fila_str += "▪  "
        print(" " + fila_str)
    print()

#  Algoritmo Bayesiano principal
def encuentra_bomba(tabla, p_bomba, cont_celdas, cont_celdas_pas,
                    p_bomba_det, p_no_bomba, p_no_bomba_det, generar):

    for x in range(len(tabla)):
        for y in range(len(tabla[x])):

            mostrar_tablero(tabla, (x, y))
            print(f"📍 Casilla ({x},{y})  |  P(bomba) prior = {p_bomba:.6f}")

            for i in range(3):
                # Simular lectura del sensor
                if tabla[x][y]:
                    det = generar(lista_bomba)
                else:
                    det = generar(lista_vacio)

                # Actualización de Bayes solo si detector positivo
                if det:
                    p_bomba = (p_bomba_det[det] * p_bomba
                               / (p_bomba * p_bomba_det[det]
                                  + p_no_bomba * p_no_bomba_det[det]))
                    p_no_bomba = 1 - p_bomba

                    # R011 — Imprimir P(Bayes) por cada detección positiva
                    print(f"   🔔 Detector positivo  →  "
                          f"P(bomba | evidencia) en ({x},{y}) = {p_bomba:.6f}")

                # Decisión: si supera umbral, declarar bomba
                if p_bomba > 0.5:
                    print(f"\n🚨 ¡BOMBA DETECTADA en ({x},{y})!")
                    return (x, y)

            # Siguiente celda: resetear prior
            cont_celdas_pas += 1
            restantes = cont_celdas - cont_celdas_pas
            if restantes > 0:
                p_bomba    = 1 / restantes
                p_no_bomba = 1 - p_bomba

    return None

#  Ejecución

generar = generador()
bomba_adiv = encuentra_bomba(tabla, p_bomba, cont_celdas, cont_celdas_pas,
                             p_bomba_det, p_no_bomba, p_no_bomba_det, generar)

print("\n" + "="*45)
if not bomba_adiv:
    print("😵 Boome no encontró la bomba.\nAlgunas funciones aún se encuentran en beta xdxdxd")
else:
    if tabla[bomba_adiv[0]][bomba_adiv[1]]:
        print(f"🎉 ¡Boome encontró la bomba en {bomba_adiv}!\n¡Aplaudan señores aplaudan!👏🏻 ")
    else:
        print(f"💥 Boome voló por los aires en {bomba_adiv} :o\nPress F to pay respects 🥲 ")
print("=-"*45)