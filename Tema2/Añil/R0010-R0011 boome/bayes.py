import random

def detector(valor):
    Vacias10 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    Bombas10 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    
    if valor == 1:
        return random.choice(Bombas10)
    else:
        return random.choice(Vacias10)

def leertablero(nombre_archivo):
    tab = []
    try:
        with open(nombre_archivo, "r") as f:
            for linea in f:
                fila = [int(x) for x in linea.split()]
                if fila:
                    tab.append(fila)
    except FileNotFoundError:
        return None
    return tab

def mostrartab(tab):
    print("\nTABLERO ACTUAL:")
    for fila in tab:
        linea = ""
        for casilla in fila:
            if casilla == 1:
                linea = linea + "X "
            else:
                linea = linea + ". "
        print(linea)

def calcularbayes(probactual):
    pdetbomba = 0.9
    pdetvacio = 0.2
    num = pdetbomba * probactual
    den = (pdetbomba * probactual) + (pdetvacio * (1 - probactual))
    if den == 0:
        return 0
    return num / den

def analisis(vreal, probinit, umbral, mlecturas):
    prob = probinit
    positi = 0
    for lec in range(mlecturas):
        res = detector(vreal)
        if res == 1:
            positi = positi + 1
            prob = calcularbayes(prob)
            print(f"    Lectura {positi}: Probabilidad = {prob:.4f}")
            if prob >= umbral:
                break
        else:
            break
    return prob, positi

def ejecutar():
    umbral = 0.51
    mdesactivar = 3
    
    print("=" * 50)
    print("BOOM + BAYES: Sistema de Deteccion de Bombas")
    print("=" * 50)
    
    mi_tab = leertablero("tablero.txt")
    
    if mi_tab is None:
        filas, cols, nbombas_total = 5, 10, 3
        mi_tab = []
        for i in range(filas): mi_tab.append([0]*cols)
        p = 0
        while p < nbombas_total:
            f, c = random.randint(0, filas-1), random.randint(0, cols-1)
            if mi_tab[f][c] == 0:
                mi_tab[f][c] = 1
                p += 1
    else:
        filas = len(mi_tab)
        cols = len(mi_tab[0])
        nbombas_total = sum(sum(f) for f in mi_tab)

    tcasillas = filas * cols
    
    print(f"Tablero: {filas}x{cols} ({tcasillas} casillas)")
    print(f"Bombas totales: {nbombas_total}")
    print(f"Umbral: {umbral} | Intentos Max: {mdesactivar}")
    
    mostrartab(mi_tab)
    
    usadas = 0
    desactivadas = 0
    falsas = 0
    revisadas = 0 
    
    print("\nANALIZANDO CASILLAS...")
    
    for i in range(filas):
        for j in range(cols):
            if usadas >= mdesactivar:
                print("\nSe agotaron los intentos de desactivacion!")
                break
            
            b_restantes = nbombas_total - desactivadas
            c_restantes = tcasillas - revisadas
            pinit = b_restantes / c_restantes if c_restantes > 0 else 0
            
            vreal = mi_tab[i][j]
            pfinal, lecturas = analisis(vreal, pinit, umbral, 3)
            revisadas += 1 
            
            if lecturas > 0:
                print(f"\nCasilla [{i},{j}] - P_Base: {pinit:.4f} - Real: {'BOMBA' if vreal == 1 else 'VACIO'}")
                if pfinal >= umbral:
                    usadas = usadas + 1
                    print(f"  DECISION: DESACTIVAR (P={pfinal:.4f} >= {umbral})")
                    print(f"  Intento #{usadas} de {mdesactivar}")
                    if vreal == 1:
                        desactivadas = desactivadas + 1
                        print(f"  RESULTADO: Bomba desactivada!")
                    else:
                        falsas = falsas + 1
                        print(f"  RESULTADO: Falsa alarma")
                else:
                    print(f"  DECISION: IGNORAR (P={pfinal:.4f} < {umbral})")
        if usadas >= mdesactivar: 
            break
    
    print("\n" + "=" * 50)
    print("RESUMEN FINAL")
    print("=" * 50)
    print(f"Bombas en tablero: {nbombas_total}")
    print(f"Bombas desactivadas: {desactivadas}")
    print(f"Falsas alarmas: {falsas}")
    print(f"Intentos usados: {usadas}/{mdesactivar}")
    
    if desactivadas == nbombas_total:
        print("\nEXITO Todas las bombas fueron desactivadas!")
    else:
        print(f"\nBOOM! Quedan {nbombas_total - desactivadas} bomba(s) activas.")

if __name__ == "__main__":
    ejecutar()