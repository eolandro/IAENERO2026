MOVS = ["movi", "movd", "mova", "movb"]
REGS = ["r0", "r1", "r2", "r3"]
SALTOS = ["salta_igual", "salta_dif"]
DIRS = ["je", "up", "ab", "dw"]


def tokenizar(linea):
    if "#" in linea:
        linea = linea.split("#", 1)[0]
    linea = linea.strip()
    if linea == "":
        return []

    linea = linea.replace("=", " = ")
    linea = linea.replace("+", " + ")
    linea = linea.replace("-", " - ")

    partes = linea.split()
    tokens = []
    for p in partes:
        if p != "":
            tokens.append(p)
    return tokens


def es_registro(s):
    return s in REGS


def es_hex(s):
    if not s:
        return False
    if len(s) < 3:
        return False
    if s[0:2] != "0x":
        return False
    try:
        int(s, 16)
        return True
    except:
        return False


def es_direccion(s):
    return s in DIRS


def validar(tokens):
    if not tokens:
        return True, ""

    # Instrucciones simples
    if len(tokens) == 1:
        ins = tokens[0]
        if ins in MOVS:
            return True, ""
        if ins == "desactivar":
            return True, ""
        return False, "Instrucción desconocida"

    # Saltos: salta_igual r0 0x01 0x000A
    if len(tokens) == 4 and tokens[0] in SALTOS:
        reg = tokens[1]
        val = tokens[2]
        destino = tokens[3]
        if not es_registro(reg):
            return False, "Salto: registro inválido"
        if not es_hex(val):
            return False, "Salto: valor inválido (usa 0x...)"
        if not es_hex(destino):
            return False, "Salto: destino inválido (usa 0x...)"
        return True, ""

    # Asignación: r0 = 0x.. | r0 = r1 | r0 = bomba
    if len(tokens) == 3 and tokens[1] == "=":
        reg = tokens[0]
        rhs = tokens[2]
        if not es_registro(reg):
            return False, "Asignación: LHS debe ser r0..r3"
        if es_hex(rhs) or es_registro(rhs) or rhs == "bomba":
            return True, ""
        return False, "Asignación: RHS inválido"

    # Sensor direccional: r0 = bomba je
    if len(tokens) == 4 and tokens[1] == "=":
        reg = tokens[0]
        sens = tokens[2]
        dire = tokens[3]
        if not es_registro(reg):
            return False, "Sensor: LHS inválido"
        if sens != "bomba":
            return False, "Sensor: solo se soporta 'bomba'"
        if not es_direccion(dire):
            return False, "Sensor: dirección inválida (je|up|ab|dw)"
        return True, ""

    # Aritmética: r0 = r1 + 0x01 | r0 = r1 - r2
    if len(tokens) == 5 and tokens[1] == "=":
        dst = tokens[0]
        a = tokens[2]
        op = tokens[3]
        b = tokens[4]
        if not es_registro(dst):
            return False, "Aritmética: destino inválido"
        if not es_registro(a):
            return False, "Aritmética: primer operando debe ser registro"
        if op not in ["+", "-"]:
            return False, "Aritmética: operador inválido"
        if not (es_hex(b) or es_registro(b)):
            return False, "Aritmética: segundo operando debe ser hex o registro"
        return True, ""

    return False, "Sintaxis inválida"


def procesar_linea(linea):
    tokens = tokenizar(linea)
    ok, _ = validar(tokens)
    return ok
