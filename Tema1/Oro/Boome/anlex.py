def numhex(Str):
    if not Str:
        return None
    if "0x" == Str[0:2]:
        RS = Str[2:]
        LS = len(RS)
        if LS == 2 or LS ==4:
            try:
                int(RS,16)
                return {"tipo": "hex", "valor": Str}
            except ValueError:
                return None
    return None

# Operador
def oper(Str):
    if not Str:
        return None
    if Str in ["+","-"]:
        return {"tipo": "operador", "valor": Str}
    return None

# MOVI -> MOVER A LA IZQ
# MOVA -> MOVER ARRIBA
# MOVD -> MOVER A LA DER
# MOVB -> MOVER ABAJO

def movs(Str):
    if not Str:
        return None

    if Str in ["movi", "mova", "movd", "movb"]:
        return {"tipo": "movimiento", "valor": Str}
    return None

# REGISTROS
def regs(Str):
    if not Str:
        return None
    if  Str in ["r0", "r1", "r2", "r3"]:
        return {"tipo": "registro", "valor": Str}
    return None

# SENSOR
# dr es direccion
def sens(LStr):
    if not LStr:
        return None
    match LStr:
        case ["abelardo", dr]:
            if dr in ["ab","je","up","dw"]:
                return {"tipo": "sensor", "direccion": dr}
    return None

# SALTOS
def salt(Str):
    if not Str:
        return None

    if Str in ["salta_igual", "salta_dif"]:
        return {"tipo": "salto", "condicion": Str}

    return None

def saltos(LStr):

    if not LStr:
        return None

    match LStr:

        case [A,B,C,D]:

            info_salto = salt(A) # validar que el salto tenga informacion

            if not info_salto:
                return None

            # Verificar operandos
            if ((regs(B) or numhex(B)) and  (regs(C) or numhex(C)) and (regs(D) or numhex(D))):
                return { "tipo": "salto", "condicion": A, "operando1": B, "operando2": C, "destino": D}

    return None



def asignacion(LStr):
    if not LStr:
        return None

    match LStr:

        # r0 = 0x01  o r1 = r2

        case [A,"=",B]:
            if regs(A) and (numhex(B) or regs(B)):
                return { "tipo": "asignacion_simple", "destino": A, "fuente" : B }


        case [A,"=",B,C]:
            if regs(A):
                sensor_info = sens([B,C])
                if sensor_info:
                    return {
                        "tipo": "asignacion_sensor",
                        "destino": A,
                        "direccion": C  # Solo guardamos la dirección
                    }

        # Caso para 5 elementos

        #r0 = r1 + r2 (Reg, Oper, Reg)

        #r0 = r1 + 0x0A (Reg, Oper, Hex)

        #r0 = 0x0A + 0x0B (Hex, Oper, Hex)

        #r0 = 0x0A + r1 (Hex, Oper, Reg)


        case [A,"=",B,C,D]:


            base = regs(A) and oper(C)
            operandos_validos = (regs(B) or numhex(B)) and  (regs(D) or numhex(D))

            if base and operandos_validos:
                return {"tipo": "operacion", "destino": A, "operando1": B, "operador": C, "operando2": D}

    return None


# Funcion principal

def procesar_linea(Str):
    if not Str:
        return False
    LStr = Str.strip().split(" ") # Se limpian los espacios
    LStr = [s for s in LStr if s]

    # Casos para procesar operaciones

    match LStr:

        case [Ins]:
            return movs(Ins)

        case [A,B]:
            return sens(LStr)

        case [A, "=", B]:
            return asignacion(LStr)

        case[A,B,C,D]:

            resultado_salto = saltos(LStr)

            if resultado_salto:
                return resultado_salto

            else:
                return asignacion(LStr)

        case [A,B,C,D,E]:
            return asignacion(LStr)


    return None
