def numhex(Str):
    if not Str:
        return False
    if Str.startswith("0x"):
        RS = Str[2:]
        if len(RS) in (2, 4):
            try:
                int(RS, 16)
                return True
            except ValueError:
                return False
    return False


def regs(Str):
    return Str in ["r0", "r1", "r2", "r3"]


def movs(Str):
    return Str in ["movi", "movd", "mova", "movb"]


def dirs(Str):
    return Str in ["iz", "de", "ar", "ab"]


def sens(L):
    match L:
        case ["sensor", d]:
            return dirs(d)
    return False


def salt(Str):
    return Str in ["salta_igual", "salta_diferente"]


def desact(Str):
    return Str == "desactiva_mina"


def asignacion(L):
    if not L:
        return False

    match L:
        case [A, "=", B]:
            return regs(A) and (regs(B) or numhex(B))
        case [A, "=", B, C]:
            return regs(A) and sens([B, C])
        case [A, "=", B, Op, C]:
            if not regs(A):
                return False
            if Op not in ["+", "-"]:
                return False
            return (regs(B) or numhex(B)) and (regs(C) or numhex(C))

    return False


def saltos(L):
    match L:
        case [A, B, C, D]:
            return (
                salt(A)
                and (regs(B) or numhex(B))
                and (regs(C) or numhex(C))
                and (regs(D) or numhex(D))
            )
    return False


def procesar_linea(Str):
    if not Str:
        return False

    L = Str.strip().split()

    match L:
        case [x]:
            return movs(x) or desact(x)
        case ["sensor", d]:
            return sens(L)
        case [A, "=", *_]:
            return asignacion(L)
        case [A, B, C, D]:
            return saltos(L)

    return False