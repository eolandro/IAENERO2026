class BoomeVM:
    def __init__(self):
        self.R = {"0": 0, "1": 0, "2": 0, "3": 0}
        self.Columna = 0
        self.Fila = 0
        self.Mapa = [["0"] * 25,
                     ["0"] * 25,
                     ["0"] * 25, 
                     ["0"] * 25, 
                     ["0"] * 25]
        self.Mapa[0][1]= "!" # Bomba Yucateca!!
        self.Mapa[0][2]= "!" # Bomba Yucateca!!
        self.Mapa[0][3]= "!" # Bomba Yucateca!!
        self.Vivo = True
        self.instruccionActual = ""
        self.ultimaInstruccion = ""
        self.contadorlineas=0

    def __str__(self):
        Ret = f"Registros\n\nR0: {self.R['0']}\n"
        Ret += f"R1: {self.R['1']}\n"
        Ret += f"R2: {self.R['2']}\n"
        Ret += f"R3: {self.R['3']}\n"
        Mapa = [fila[:] for fila in self.Mapa]  # self.Mapa[::]
        # Mapa[self.Fila][self.Columna] = "Boome"
        Mapa[self.Fila][self.Columna] = "B" # Representancion de Boome

        for fila in Mapa:
            Ret += f"{fila}\n"

        Ret += f"Ultima instrucción: {self.ultimaInstruccion}\n"
        Ret += f"Ultima instrucción: {self.instruccionActual}\n"
        Ret += f"Vivo: {self.Vivo}\n"
        Ret += f"{"-" * 50}\n"

        return Ret  # self.R == > r0

    def movIzquierda(self):
        self.Columna -= 1
        if self.Columna < 0:
            if self.Mapa[self.Fila][0] == '!':
                self.Vivo = False
                print("BOOM! Intentó salir sin desactivar")
            else:
                self.Columna = 0
            return  

    def movDerecha(self):
        self.Columna += 1
        if self.Columna >= len(self.Mapa[self.Fila]):
            if self.Mapa[self.Fila][self.Columna - 1] == '!':  # Bomba en borde
                self.Vivo = False
                print("BOOM! Intentó salir sin desactivar")
            else:
                self.Columna -= 1  # Revierte sin matar
            return

    def movArriba(self):
        self.Fila -= 1
        if self.Fila < 0:
            if self.Mapa[0][self.Columna] == '!':
                self.Vivo = False
                print("BOOM! Intentó salir sin desactivar")
            else:
                self.Fila = 0
            return

    def movAbajo(self):
        self.Fila += 1
        if self.Fila >= len(self.Mapa):
            if self.Mapa[self.Fila - 1][self.Columna] == '!':
                self.Vivo = False
                print("BOOM! Intentó salir sin desactivar")
            else:
                self.Fila -= 1
            return

    def fetchDecodeExecute(self, instruccion):
        if not self.Vivo: 
            return
        if self.Mapa[self.Fila][self.Columna] == '!' and instruccion in ['movi', 'movd', 'mova', 'movb']:
            self.Vivo = False
            return
        
        self.ultimaInstruccion = self.instruccionActual
        self.instruccionActual = instruccion

        if instruccion in ["movi", "movd", "mova", "movb"]: # 1) Movimientos
            match [instruccion]:
                case ["movi"]:
                    self.movIzquierda()
                case ["movd"]:
                    self.movDerecha()
                case ["mova"]:
                    self.movArriba()
                case ["movb"]:
                    self.movAbajo()
            return

        tokens = instruccion.split()  # tokenizacion

        match tokens: # Sensor abelardo
            case [reg, "=", "abelardo", dir]:
                if reg in ["r0", "r1", "r2", "r3"]:
                    idx = reg[1]
                    match dir:
                        case "je":  # derecha
                            if self.Columna + 1 < 25:
                                self.R[idx] = 1 if self.Mapa[self.Fila][self.Columna + 1] == "X" else 0
                            else:
                                self.R[idx] = 0
                        case "dw":  # abajo
                            if self.Fila + 1 < 5:
                                self.R[idx] = 1 if self.Mapa[self.Fila + 1][self.Columna] == "X" else 0
                            else:
                                self.R[idx] = 0
                        case "ab":  # arriba
                            if self.Fila > 0:
                                self.R[idx] = 1 if self.Mapa[self.Fila - 1][self.Columna] == "X" else 0
                            else:
                                self.R[idx] = 0
                        case "up":  # izquierda
                            if self.Columna > 0:
                                self.R[idx] = 1 if self.Mapa[self.Fila][self.Columna - 1] == "X" else 0
                            else:
                                self.R[idx] = 0
                return

        match tokens:# Asignación literal r3=0x0001
            case [reg, "=", valor]:
                if reg in ["r0", "r1", "r2", "r3"] and valor.startswith("0x"):
                    self.R[reg[1]] = int(valor, 16)
                return
            
        match tokens: # Aritmética ejemplo r3=r3+0x0001
            case [reg, "=", src, op, valor]:
                if reg == src and reg in ["r0", "r1", "r2", "r3"] and op in ["+", "-"] and valor.startswith("0x"):
                    val = int(valor, 16)
                    idx = reg[1]
                    if op == "+":
                        self.R[idx] += val
                    else:
                        self.R[idx] -= val
                return
        
        match tokens: # Saltos condicionales
            case ["salta_igual", reg, valor, destino]:
                if reg in ["r0", "r1", "r2", "r3"]:
                    idx = reg[1]
                    val = int(valor, 16)
                    dest = int(destino, 16) - 1  # -1 porque contadorlineas++ después
                    if self.R[idx] == val:
                        self.contadorlineas = dest
                    return
            
            case ["salta_dif", reg, valor, destino]:
                if reg in ["r0", "r1", "r2", "r3"]:
                    idx = reg[1]
                    val = int(valor, 16)
                    dest = int(destino, 16) - 1  # -1 porque contadorlineas++ después
                    if self.R[idx] != val:
                        self.contadorlineas = dest
                    return
        
        match tokens: # Sensor de bomba (solo debajo)
            case [reg, "=", "BombaY", "By"]:
                if reg in ["r0", "r1", "r2", "r3"]:
                    idx = reg[1] # Solo detecta bomba SI Boome está ENCIMA
                    bomba = 1 if self.Mapa[self.Fila][self.Columna] == "!" else 0
                    print(f"DEBUG BombaY: Fila{self.Fila} Col{self.Columna} = '{self.Mapa[self.Fila][self.Columna]}' → R0={bomba}")
                    self.R[idx] = 1 if self.Mapa[self.Fila][self.Columna] == "!" else 0
                return

        match tokens: # Desactivar bomba (solo si está encima)
            case ["desactivar"]:
                if self.Mapa[self.Fila][self.Columna] == "!":
                    self.Mapa[self.Fila][self.Columna] = "0"
                    print("¡BOMBA DESACTIVADA!")
                else:
                    print("No hay bomba debajo")
                return
        
