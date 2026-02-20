def numhex(Str):
    if not Str:
        return False
    if "0x"==Str[0:2]:
        RS=Str[2:]
        LS=len(RS)
        if LS==2 or LS==4:
            try:
                int(RS,16)
                return True
            except ValueError:
                return False
    return False

def oper(Str):
    if not Str:
        return False
    return Str in ["+","-"]

def movs(Str):
    if not Str:
        return False
    return Str in ["movi","movd","mova","movb"]

def regs(Str):
    if not Str:
        return False
    return Str in ["r0","r1","r2","r3"]



def sens(LStr):
    if not LStr:
        return False
    if len(LStr) == 1:
        return LStr[0] in ["ab","je","up","dw"]
    if len(LStr) == 2:
        return LStr[1] in ["ab","je","up","dw"]

    return False


def salt(Str):
    if not Str:
        return False
    return Str in ["salta_igual","salta_dif"]

def asignacion(LStr):
    if not LStr:
        return False
    match LStr:
        case[A,"=",B]:
            return regs(A) and (numhex(B) or regs(B))
        case[A,"=",B,C]:
            return regs(A) and (sens([B,C]))
        case[A,"=",B,C,D]:
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
        case[A,B,C,D]:
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

    LStr=Str.strip().split(" ")
    LStr=[s for s in LStr if s]

    match LStr:
        case [Ins]:
            return movs(Ins) or sens([Ins])

        case[A,"=",B]:
            return asignacion(LStr)

        case [A, "=", B, C]:
            return asignacion(LStr)

        case [A, B, C, D]:
            return saltos(LStr)

        case [A, "=", B, C, D]:
            return asignacion(LStr)

    return False





