def numhex(Str):
    # Valida hex con prefijo 0x y longitud 2 o 4 (ej: 0x0A, 0x00FF)
    if not Str:
        return False
    if "0x" == Str[0:2]:
        RS = Str[2:]
        LS = len(RS)
        if LS == 2 or LS == 4:
            try:
                int(RS, 16)
                return True
            except ValueError:
                return False
    return False


def oper(Str):
    # Operadores permitidos
    if not Str:
        return False
    return Str in ["+", "-"]


def movs(Str):
    # Instrucciones de movimiento válidas
    if not Str:
        return False
    return Str in ["movi", "movd", "mova", "movb"]


def regs(Str):
    # Registros válidos
    if not Str:
        return False
    return Str in ["r0", "r1", "r2", "r3"]


def sens(LStr):
    # Sensor: abelardo + dirección (ab/je/up/dw)
    if not LStr:
        return False
    match LStr:
        case ["abelardo", dr]:
            return dr in ["ab", "je", "up", "dw"]
    return False


def salt(Str):
    # Saltos disponibles
    if not Str:
        return False
    return Str in ["salta_igual", "salta_dif"]


def asignacion(LStr):
    if not LStr:
        return False

    match LStr:
        # rX = 0x0A  o  rX = rY
        case [A, "=", B]:
            return regs(A) and (numhex(B) or regs(B))

        # rX = abelardo dw
        case [A, "=", B, C]:
            return regs(A) and sens([B, C])

    return False


def deshabilitar_bomba(LStr):
    # Instrucción especial de 1 palabra
    if not LStr:
        return False
    match LStr:
        case ["deshabilitar"]:
            return True
    return False


def saltos(LStr):
    # Formato: salta_igual X Y Z  /  salta_dif X Y Z
    # X, Y, Z pueden ser registro o hexadecimal
    if not LStr:
        return False
    match LStr:
        case [OP, X, Y, Z]:
            if not salt(OP):
                return False
            okX = regs(X) or numhex(X)
            okY = regs(Y) or numhex(Y)
            okZ = regs(Z) or numhex(Z)
            return okX and okY and okZ
    return False


def procesar_linea(Str):
    # Recibe una línea, la tokeniza y valida si corresponde a una instrucción válida
    if not Str:
        return False

    LStr = Str.strip().split(" ")
    LStr = [s for s in LStr if s]

    match LStr:
        # Instrucciones de 1 token
        case [Ins]:
            return movs(Ins) or deshabilitar_bomba(LStr)

        # Asignaciones
        case [A, "=", *_]:
            return asignacion(LStr)

        # Saltos (4 tokens)
        case [OP, _, _, _]:
            return saltos(LStr)

    return False