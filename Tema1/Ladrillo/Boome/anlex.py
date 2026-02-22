import re

REGISTROS = {"R0", "R1", "R2", "R3"}

def es_hexadecimal(token):
    return re.fullmatch(r"H[0-9A-Fa-f]+", token) is not None

def procesar_linea(linea):
    linea = linea.strip()

    if not linea:
        return None

    tokens = linea.split()

    match tokens:

        # Movimiento
        case ["avanza", direccion] if direccion in ["Izq", "Der", "Arr", "Abj"]:
            return tokens

        # Sensor
        case ["sensor", direccion] if direccion in ["Izq", "Der", "Arr", "Abj"]:
            return tokens

        # Saltos
        case ["Scero", etiqueta] if es_hexadecimal(etiqueta):
            return tokens

        case ["Sncero", etiqueta] if es_hexadecimal(etiqueta):
            return tokens

        # Comparación
        case ["cmp", registro] if registro in REGISTROS:
            return tokens

        # Asignación simple
        case [r1, "=", r2] if r1 in REGISTROS and r2 in REGISTROS:
            return tokens

        case [r1, "=", num] if r1 in REGISTROS and es_hexadecimal(num):
            return tokens

        # Operación aritmética
        case [r1, "=", op1, operador, op2] \
            if r1 in REGISTROS and operador in ["+", "-"]:
            return tokens

        case _:
            return None