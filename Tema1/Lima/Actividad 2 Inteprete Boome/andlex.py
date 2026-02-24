def numhex(Str):
    if not Str:
        return False
    if "0x"== Str[0:2]:
        RS =Str[2:]
        LS =len(RS)
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
    match LStr:
        case ['abelardo',dr]:
            return dr in ["ab","je","up","dw"]
        # Sensor de bomba
        case ['BombaY', 'By']:
            return True
        case _:
            return False
    return False

def salt(Str):
    if not Str:
        return False
    return Str in ["salta_igual","salta_dif"]

def asignacion(LStr):
    if not LStr:
        return False
    match LStr:
        case [A,"=",B]:
            return regs(A) and (numhex(B) or regs(B))
        case [A,"=",B,C,D]:
            return regs(A) and regs(B) and oper(C) and (numhex(D) or regs(D))
        case [A,"=",B,C,D]:
            return numhex(A) and numhex(B) and oper(C) and (numhex(D) or regs(D))
        case [A, "=", B, S]:
            return regs(A) and sens([B, S])
        case [A,B,C,D]:
            return salt(A) and (numhex(B) or regs(B)) and (numhex(C) or regs(C)) and (numhex(D) or regs(D))         
        case [A, '', B, S]:
            return regs(A) and sens([B, S])
    return False

def procesar_linea(Str):
    if not Str:
        return False
    Str=Str.strip()
    if not Str:
        return False
    Str = Str.replace("=", " = ").replace("+", " + ").replace("-", " - ")
    LStr = Str.split()
    LStr = [s for s in LStr if s]
    match LStr:
        case[Ins]:
            return movs(Ins) or Ins == "desactivar"
        case[A,"=",B]:
            return asignacion(LStr)
        case [A,"=",B,C,D]:
            return asignacion(LStr)
        case [A,B,C,D]:
            return asignacion(LStr)
        case [A, "", B, S]:  # Para r0 BombaY By
            return regs(A) and sens([B, S])
    return False



