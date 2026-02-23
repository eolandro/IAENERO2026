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



def direccion(Str):
    if not Str:
        return False
    return Str in ["ab", "je", "up", "dw"]



def sens(LStr):
    if not LStr:
        return False 
    match LStr:
        case ['abelardo', dr]:
            return dr in["ab","je","up","dw"]
    return False


def salt(Str):
    if not Str:
        return False
    return Str in ["salta_igual", "salta_dif"]


# NUEVA INSTRUCCIÓN
def desact(Str):
    if not Str:
        return False
    return Str == "negro_desactiva"


def asignacion(LStr):
    if not LStr:
        return False

    match LStr:

        # rX = valor
        case [A, "=", B]:
            return regs(A) and (
                numhex(B) or
                regs(B) or
                sens(B)   
            )

        # rX = abelardo direccion
        case [A, "=", B, C]:
            return regs(A) and sens([B, C])

        # rX = operacion
        case [A, "=", B, C, D]:
            return regs(A) and (
                (regs(B) and oper(C) and regs(D)) or
                (regs(B) and oper(C) and numhex(D)) or
                (numhex(B) and oper(C) and numhex(D)) or
                (numhex(B) and oper(C) and regs(D))
            )

    return False


def saltos(LStr):
    if not LStr:
        return False

    match LStr:
        case [A, B, C, D]:
            return salt(A) and (
                (regs(B) and numhex(C) and numhex(D)) or
                (regs(B) and regs(C) and numhex(D)) or
                (regs(B) and regs(C) and regs(D)) or
                (numhex(B) and regs(C) and regs(D)) or
                (numhex(B) and numhex(C) and regs(D)) or
                (numhex(B) and numhex(C) and numhex(D))
            )

    return False


def procesar_linea(Str):
    if not Str:
        return False

    LStr = Str.strip().split(" ")
    LStr = [s for s in LStr if s]

    match LStr:

        # Instrucciones simples
        case [Ins]:
            return (
                movs(Ins) or
                desact(Ins) or
                sens(Ins)   
            )

        # abelardo direccion
        case ['abelardo', dr]:
            return sens(LStr)

        # Asignaciones
        case [A, "=", B]:
            return asignacion(LStr)

        case [A, "=", B, C]:
            return asignacion(LStr)

        case [A, "=", B, C, D]:
            return asignacion(LStr)

       
        case [A, B, C, D]:
            return saltos(LStr)

    return False