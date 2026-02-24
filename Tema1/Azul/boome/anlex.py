# Valida numero hexadecimal: 0xAB o 0xABCD
def numhex(s):
    if not s:
        return False
    # Debe empezar con "0x"
    if s[:2] != "0x":
        return False
    resto = s[2:]
    # Solo 2 o 4 digitos hexadecimales
    if len(resto) not in [2, 4]:
        return False
    try:
        int(resto, 16)
        return True
    except ValueError:
        return False

# Valida operadores: + o -
def oper(s):
    if not s:
        return False
    return s in ["+", "-"]

# Valida movimientos: movi, movd, mova, movb
def movs(s):
    if not s:
        return False
    return s in ["movi", "movd", "mova", "movb"]

# Valida registros: r0, r1, r2, r3
def regs(s):
    if not s:
        return False
    return s in ["r0", "r1", "r2", "r3"]

# Valida sensor: abelardo con direccion (ab, je, up, dw)
# `ab`: Izquierda (col - 1) 
# `je`: Derecha (col + 1) 
# `up`: Arriba (fila - 1)
# `dw`: Abajo (fila + 1) 

def sens(tokens):
    if not tokens or len(tokens) != 2:
        return False
    return tokens[0] == "abelardo" and tokens[1] in ["ab", "je", "up", "dw"]

# Valida saltos: salta_igual o salta_dif
def salt(s):
    if not s:
        return False
    return s in ["salta_igual", "salta_dif"]

# Valida asignaciones
# Formas:
#   r0 = 0xAB          -> [reg, "=", numhex]
#   r0 = r1             -> [reg, "=", reg]
#   r0 = abelardo up    -> [reg, "=", "abelardo", dir]
#   r0 = r1 + r2        -> [reg, "=", reg/num, oper, reg/num]
def asignacion(tokens):
    if not tokens:
        return False
    # Forma: reg = valor (3 tokens)
    if len(tokens) == 3:
        a, eq, b = tokens
        if eq != "=":
            return False
        return regs(a) and (numhex(b) or regs(b))
    # Forma: reg = abelardo dir (4 tokens)
    if len(tokens) == 4:
        a, eq, b, c = tokens
        if eq != "=":
            return False
        return regs(a) and sens([b, c])
    # Forma: reg = val oper val (5 tokens)
    if len(tokens) == 5:
        a, eq, b, op, d = tokens
        if eq != "=":
            return False
        if not regs(a) or not oper(op):
            return False
        # 4 combinaciones: reg+reg, reg+num, num+num, num+reg
        val_b = regs(b) or numhex(b)
        val_d = regs(d) or numhex(d)
        return val_b and val_d
    return False

# Valida saltos condicionales
# Forma: salta_igual/salta_dif val1 val2 destino (4 tokens)
# val1, val2, destino pueden ser reg o numhex
def saltos(tokens):
    if not tokens or len(tokens) != 4:
        return False
    s, b, c, d = tokens
    if not salt(s):
        return False
    # Cada argumento puede ser registro o numhex
    val_b = regs(b) or numhex(b)
    val_c = regs(c) or numhex(c)
    val_d = regs(d) or numhex(d)
    return val_b and val_c and val_d

# Procesa una linea y valida su estructura
# Retorna True si la linea es valida, False si no
def procesar_linea(linea):
    if not linea:
        return False
    # Separar tokens por espacios
    tokens = linea.strip().split()
    tokens = [t for t in tokens if t]
    if not tokens:
        return False
    # 1 token -> movimiento
    if len(tokens) == 1:
        return movs(tokens[0])
    # 2 tokens -> sensor suelto (abelardo dir)
    if len(tokens) == 2:
        return sens(tokens)
    # 3 tokens -> asignacion simple (reg = val)
    if len(tokens) == 3:
        return asignacion(tokens)
    # 4 tokens -> asignacion con sensor o salto condicional
    if len(tokens) == 4:
        if asignacion(tokens):
            return True
        return saltos(tokens)
    # 5 tokens -> asignacion con operacion
    if len(tokens) == 5:
        return asignacion(tokens)
    return False
