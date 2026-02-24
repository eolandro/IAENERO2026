def numhex(Str):
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
    if not Str:
        return False
    return Str in ["+", "-"]


def movs(Str):
    if not Str:
        return False
    return Str in ["movi", "movd", "mova", "movb"]


def regs(Str):
    if not Str:
        return False
    return Str in ["r0", "r1", "r2", "r3"]


def salt(Str):
    if not Str:
        return False
    return Str in ["salta_igual", "salta_dif"]


# --- Funciones con pequeñas variaciones entre archivos ------

def sens(LStr):
    if not LStr:
        return False
    match LStr:
        case ["abelardo", dr]:
            return dr in ["ab", "je", "up", "dw"]
    return False


def desact(Str):
    if not Str:
        return False
    return Str in ["negro_desactiva", "deactivate", "desactivar"]


# --- Funciones compuestas -----------------------------------

def asignacion(LStr):
    if not LStr:
        return False
    match LStr:

        # rX = valor  (registro o hex)
        case [A, "=", B]:
            return regs(A) and (numhex(B) or regs(B))

        # rX = abelardo dir
        case [A, "=", B, C]:
            return regs(A) and sens([B, C])

        # rX = val oper val  (4 combinaciones: reg/num op reg/num)
        case [A, "=", B, C, D]:
            return (
                regs(A) and
                oper(C) and
                (regs(B) or numhex(B)) and
                (regs(D) or numhex(D))
            )

    return False


def saltos(LStr):
    if not LStr:
        return False
    match LStr:
        case [A, B, C, D]:
            return (
                salt(A) and
                (regs(B) or numhex(B)) and
                (regs(C) or numhex(C)) and
                (regs(D) or numhex(D))
            )
    return False


# --- Función principal --------------------------------------

def procesar_linea(Str):
    if not Str:
        return False

    # Normalizar operadores para tokenizar con o sin espacios
    Str = Str.strip().replace("=", " = ").replace("+", " + ").replace("-", " - ")
    LStr = Str.split()
    LStr = [s for s in LStr if s]

    match LStr:

        case [Ins]:
            return movs(Ins) or desact(Ins)

        case [A, B]:
            return sens(LStr)

        case [A, "=", B]:
            return asignacion(LStr)

        # FIX: caso que faltaba en el original (rX = abelardo dir)
        case [A, "=", B, C]:
            return asignacion(LStr)

        case [A, B, C, D]:
            resultado_salto = saltos(LStr)
            if resultado_salto:
                return resultado_salto
            else:
                return asignacion(LStr)

        case [A, B, C, D, E]:
            return asignacion(LStr)

    return False