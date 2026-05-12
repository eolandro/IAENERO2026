# R007: Come Solo 
ETIQUETAS = "123456789ABCDEF"

# Diccionario compacto de movimientos: origen: [(intermedia, destino), ...]
MOVS = {
    0: [(1,3), (2,5)], 1: [(3,6), (4,8)], 2: [(4,7), (5,9)],
    3: [(1,0), (4,5), (6,10), (7,12)], 4: [(7,11), (8,13)],
    5: [(2,0), (4,3), (8,12), (9,14)], 6: [(3,1), (7,8)],
    7: [(4,2), (8,9)], 8: [(4,1), (7,6)], 9: [(5,2), (8,7)],
    10: [(6,3), (11,12)], 11: [(7,4), (12,13)],
    12: [(7,3), (8,5), (11,10), (13,14)], 13: [(8,4), (12,11)],
    14: [(9,5), (13,12)]
}

def imprimir_triangulo(t):
    """Dibuja el triángulo evaluando si hay ficha (etiqueta) o está vacío (.)."""
    s = [ETIQUETAS[i] if t[i] else '.' for i in range(15)]
    print(f"            {s[0]}\n           / \\\n          {s[1]}   {s[2]}\n         / \\ / \\\n        {s[3]}   {s[4]}   {s[5]}\n       / \\ / \\ / \\\n      {s[6]}   {s[7]}   {s[8]}   {s[9]}\n     / \\ / \\ / \\ / \\\n    {s[10]}   {s[11]}   {s[12]}   {s[13]}   {s[14]}")

def resolver(t, pasos):
    """Backtracking recursivo para encontrar la primera solución."""
    if sum(t) == 1: 
        return True
    
    for o, saltos in MOVS.items():
        if t[o]: # Solo evaluar si hay ficha en el origen
            for i, d in saltos:
                if t[i] and not t[d]: # Intermedia ocupada y destino libre
                    t[o], t[i], t[d] = False, False, True  # Saltar
                    pasos.append((o, d))
                    
                    if resolver(t, pasos): return True
                    
                    t[o], t[i], t[d] = True, True, False   # Backtrack
                    pasos.pop()
    return False

# --- Programa Principal ---
print("\n=== R007: Come Solo (Triángulo) ===\nPosiciones de referencia:")
imprimir_triangulo([True] * 15)

# Bucle para pedir posición
while True:
    entrada = input("\n¿Qué posición estará vacía inicialmente? (1-F): ").strip().upper()
    if len(entrada) == 1 and entrada in ETIQUETAS:
        pos_vacia = ETIQUETAS.index(entrada)
        break
    print("  [!] Entrada no válida. Usa un carácter del 1 al F.")

# Preparar el tablero e iniciar búsqueda
tablero = [True] * 15
tablero[pos_vacia] = False
pasos = []

print(f"\nCalculando solución para vacío en '{entrada}'...\n")

if resolver(tablero, pasos):
    # Reconstruir los pasos para la impresión gráfica
    t_actual = [True] * 15
    t_actual[pos_vacia] = False
    
    print("~~~ Estado Inicial ~~~")
    imprimir_triangulo(t_actual)
    
    for num, (o, d) in enumerate(pasos, 1):
        # Aplicamos el movimiento visualmente
        # Encontramos la casilla intermedia buscando en las reglas
        inter = next(i for inter, dest in MOVS[o] if dest == d for i in [inter])
        t_actual[o], t_actual[inter], t_actual[d] = False, False, True
        
        print(f"\n >Paso {num}: {ETIQUETAS[o]} salta hacia {ETIQUETAS[d]} <")
        imprimir_triangulo(t_actual)
        
    print("\n¡Puzzle resuelto!")
else:
    print(f"No tiene solución posible empezando con '{entrada}' vacía.")