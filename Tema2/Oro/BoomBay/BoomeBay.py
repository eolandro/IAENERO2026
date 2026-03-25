import json
import random
from colorama import init, Fore, Back, Style

def crear_tablero_limpio():
    tablero = {}
    letras = ['A', 'B', 'C', 'D', 'E']
    for fila in range(1, 11):
        for col in letras:
            tablero[f"{col}{fila}"] = 0
    return tablero

def guardar_tablero(tablero):
    with open('tablero.json', 'w', encoding='utf-8') as archivo:
        json.dump(tablero, archivo, indent=2)

def plantar_bomba(tablero):
    casillas_vacias = [casilla for casilla, valor in tablero.items() if valor == 0]
    bomba = random.choice(casillas_vacias)
    tablero[bomba] = 1
    print(f"Bomba plantada en: {bomba}")

def detector_bomba(valor_real):

    vacias_10 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    bombas_10 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    
    if valor_real == 1:  # Hay bomba
        return random.choice(bombas_10)
    else:  # No hay bomba
        return random.choice(vacias_10)

def probabilidad_bayesiana(prob_anterior, mediciones):
    
    # ¿QUE PROBABILIDAD CALCULAMOS?
    # P(Bomba| D+) = ?

    # ¿Como se calcula eso?

    #               P(D+|Bomba)*P(Bomba)
    # -------------------------------------
    #     P(D+| Bomba) * P(Bomba) + P(D+| No Bomba) * P(No hay Bomba)

    # Donde  
    # P(D+|Bomba) =  0.9 Porque hay 9  de cada 10 veces atine que hay bomba dado que si hay una bomba
    # P(D+ | No hay bomba) =  Porque 2 de cada 10 veces se equivocara  en detectar que es seguro
    # P(Bomba) = 1/50  porque en un inicio  hay 0.02  probs de que haya una bomba en todo el tablero 
    # P(No hay bomba) = 49/50
    # Solo en la primera iteracion es 1/50

    # Primera iteracion
    #               0.9 * 0.02
    # -------------------------------------  = 0.08 aprox
    #     (0.9 * 0.02) + (0.2 *0.98)


    p_detectar_bomba = 0.9
    p_falso_positivo = 0.2

    prob_actual = prob_anterior
    
    for medicion in mediciones:
        if medicion == 1:
            numerador  =                    (p_detectar_bomba * prob_actual)
            denominador =  (p_detectar_bomba * prob_actual) + (p_falso_positivo * (1 - prob_actual))
            prob_actual  =  numerador /denominador

    return prob_actual

def verificar_casilla_bayesiana(tablero, casilla, desactivaciones, prob_inicial):
    
    # Verificar que hay en la casilla
    valor_real = tablero[casilla]
    
    # Tomar las 3 mediciones o detecciones
    mediciones = []
    for _ in range(3):
        medicion = detector_bomba(valor_real)
        mediciones.append(medicion)
    
    print(f"Mediciones en {casilla}: {mediciones}")
    
    # Si hubo al menos una detección positiva
    if 1 in mediciones:
        probabilidad = probabilidad_bayesiana(prob_inicial, mediciones)
        print(f"Probabilidad bayesiana calculada: {probabilidad:.1%}")
        
        # Caso 1: Hay bomba real Y la probabilidad supera el umbral
        if valor_real == 1 and probabilidad >= 0.5:
            if desactivaciones > 0:
                print(f"Bomba detectada en {casilla} con {probabilidad:.1%} — desactivando")
                tablero[casilla] = 0
                print(f"Bomba desactivada. Quedan {desactivaciones - 1} desactivaciones")
                return True, probabilidad, desactivaciones - 1
            else:
                print(f"Bomba detectada en {casilla} con {probabilidad:.1%} pero sin desactivaciones")
                print(f"Boome pisa la bomba")
                return False, probabilidad, desactivaciones

        # Caso 2: Hay bomba pero la probabilidad es baja (el detector no fue convincente)
        elif valor_real == 1 and probabilidad < 0.5:
            print(f"Bomba en {casilla} pero probabilidad {probabilidad:.1%} no supera el umbral")
            print(f"Boome pisa la bomba sin saberlo")
            return False, probabilidad, desactivaciones

        # Caso 3: No hay bomba real (falso positivo del detector)
        else:
            print(f"No hay bomba real en {casilla} - fue un falso positivo")
            return True, probabilidad, desactivaciones
            
    else:
        if valor_real == 1:
            print(f"Detector falló completamente — Boome pisa la bomba en {casilla}")
            return False, 0, desactivaciones
        
        print("No hubo detecciones positivas, se asume seguro")
        return True, 0, desactivaciones

def obtener_siguiente(casilla, direccion):
    letras = ['A', 'B', 'C', 'D', 'E']
    
    col = casilla[0]
    fila = int(casilla[1:])
    idx = letras.index(col)
    
    if direccion == 'derecha':
        if idx < 4:
            return f"{letras[idx + 1]}{fila}", 'derecha', False
        else:
            if fila == 10:
                return None, None, True
            return f"E{fila + 1}", 'izquierda', False
    else:
        if idx > 0:
            return f"{letras[idx - 1]}{fila}", 'izquierda', False
        else:
            if fila == 10:
                return None, None, True
            return f"A{fila + 1}", 'derecha', False

def imprimir_tablero(tablero, boome_pos=None):
    letras = ['A', 'B', 'C', 'D', 'E']
    
    print("\n   A B C D E")
    for fila in range(1, 11):
        print(f"{fila:2} ", end=" ")
        for col in letras:
            casilla = f"{col}{fila}"
            if boome_pos == casilla:
                print(Fore.BLUE + "B" + Style.RESET_ALL, end = " ")
            elif tablero[casilla] == 1:
                 print(Fore.RED + "1" + Style.RESET_ALL, end = " ")
            else:
                print("0", end=" ")
        print()
    print()

def mover_boome():
    tablero = crear_tablero_limpio()
    plantar_bomba(tablero)
    
    print("=== TABLERO INICIAL ===")
    imprimir_tablero(tablero)
    casilla_actual = "A1"
    direccion = 'derecha'
    movimientos = 0
    ruta = []
    posicion_anterior = None
    desactivaciones = 3
    
    total_bombas = sum(1 for valor in tablero.values() if valor == 1)
    total_casillas = len(tablero)  # 50 casillas
    
    # Probabilidad inicia real  en la primera iteracion seria 1/50
    prob_actual = total_bombas / total_casillas
    print(f"Probabilidad inicial de bomba: {prob_actual:.1%} ({total_bombas} bombas en {total_casillas} casillas)")
    
    while True:
        movimientos += 1
        print(f"\n--- Movimiento {movimientos}: {casilla_actual} ---")
        print(f"Probabilidad actual (antes de verificar): {prob_actual:.2%}")
        
        sobrevive, probabilidad, desactivaciones = verificar_casilla_bayesiana(
            tablero, casilla_actual, desactivaciones, prob_actual
        )
        
        if not sobrevive:
            print(f"\nBoome murio en {casilla_actual}")
            print(f"Probabilidad bayesiana final: {probabilidad:.1%}")
            print(f"Movimientos realizados: {movimientos}")
            print(f"Casillas recorridas: {len(ruta)}")
            return False
        
        if tablero[casilla_actual] != 1 and tablero[casilla_actual] != "B":
            casillas_revisadas = len(ruta) + 1
            casillas_restantes = total_casillas - casillas_revisadas
            
            bombas_restantes = total_bombas - (3 - desactivaciones)
            
            if casillas_restantes > 0:
                prob_actual = bombas_restantes / casillas_restantes
                print(f" Actualizacion: {bombas_restantes} bombas en {casillas_restantes} casillas restantes")
                print(f"Nueva probabilidad: {prob_actual:.2%}")
            else:
                prob_actual = 0
        
        # Limpiar la casilla anterior
        if posicion_anterior:
            tablero[posicion_anterior] = 0
        
        # Marcar posición actual de Boome
        ruta.append(casilla_actual)
        tablero[casilla_actual] = "B"
        posicion_anterior = casilla_actual
        
        imprimir_tablero(tablero, casilla_actual)
        
        # Avanzar a la siguiente casilla
        siguiente, nueva_dir, completado = obtener_siguiente(casilla_actual, direccion)
        
        if completado:
            print(f"\n ¡Boome completó el tablero! ")
            print(f"Casillas recorridas: {len(ruta)} de 50")
            print(f"Desactivaciones usadas: {3 - desactivaciones}")
            print(f"Bombas restantes: {total_bombas - (3 - desactivaciones)}")
            guardar_tablero(tablero)
            return True
        
        casilla_actual = siguiente
        direccion = nueva_dir

def main():
    mover_boome()

if __name__ == "__main__":
    main()