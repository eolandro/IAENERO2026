class BoomeVM:

    def __init__(self):
        # Registros de 16 bits
        self.R = {"0":0x0000,"1":0x0000,"2":0x0000,"3":0x0000}

        self.Columna = 0
        self.Fila = 0

        self.Mapa = [
            ["0"]*10,
            ["0"]*10,
            ["0"]*10,
            ["0"]*10,
            ["0"]*10
        ]

        # Bombas
        self.Mapa[0][1] = "X"
        self.Mapa[4][9] = "X"

        self.ultimaInstruccion = ""
        self.InstruccionActual = ""
        self.Vivo = True
        self.SobreBomba = False


    # =====================================
    # PRINT ESTADO (REGISTROS EN HEX)
    # =====================================

    def __str__(self):
        Ret = "\nRegistros:\n"

        
        r0 = self.R["0"] if isinstance(self.R["0"], int) else 0
        r1 = self.R["1"] if isinstance(self.R["1"], int) else 0
        r2 = self.R["2"] if isinstance(self.R["2"], int) else 0
        r3 = self.R["3"] if isinstance(self.R["3"], int) else 0

        Ret += f"R0 0x{r0:04X}\n"
        Ret += f"R1 0x{r1:04X}\n"
        Ret += f"R2 0x{r2:04X}\n"
        Ret += f"R3 0x{r3:04X}\n"

        M = [fila[:] for fila in self.Mapa]
        M[self.Fila][self.Columna] = "B"

        for fila in M:
            Ret += f"{fila}\n"

        Ret += f"Ultima instrucción: {self.ultimaInstruccion}\n"
        Ret += f"Instrucción actual: {self.InstruccionActual}\n"
        Ret += f"Vivo: {self.Vivo}\n"
        Ret += "--------------------------------------"
        return Ret


    # =====================================
    # BOMBA
    # =====================================

    def checarBomba(self):
        if self.Mapa[self.Fila][self.Columna] == "X":
            self.SobreBomba = True
            print(" Boome está sobre una bomba...")


    # =====================================
    # MOVIMIENTOS
    # =====================================

    def movIzquierda(self):
        self.Columna -= 1
        if self.Columna < 0:
            self.Columna = 0
            self.Vivo = False

    def movDerecha(self):
        self.Columna += 1
        if self.Columna >= len(self.Mapa[0]):
            self.Columna -= 1
            self.Vivo = False

    def movArriba(self):
        self.Fila -= 1
        if self.Fila < 0:
            self.Fila = 0
            self.Vivo = False

    def movAbajo(self):
        self.Fila += 1
        if self.Fila >= len(self.Mapa):
            self.Fila -= 1
            self.Vivo = False


    # =====================================
    # SENSORES (R0 = 0x1 si hay bomba)
    # =====================================

    def sensIzquierda(self):
        c = self.Columna - 1
        if c < 0 or self.Mapa[self.Fila][c] != "0":
            self.R["0"] = 0x0001
        else:
            self.R["0"] = 0x0000

    def sensDerecha(self):
        c = self.Columna + 1
        if c >= len(self.Mapa[0]) or self.Mapa[self.Fila][c] != "0":
            self.R["0"] = 0x0001
        else:
            self.R["0"] = 0x0000

    def sensArriba(self):
        f = self.Fila - 1
        if f < 0 or self.Mapa[f][self.Columna] != "0":
            self.R["0"] = 0x0001
        else:
            self.R["0"] = 0x0000

    def sensAbajo(self):
        f = self.Fila + 1
        if f >= len(self.Mapa) or self.Mapa[f][self.Columna] != "0":
            self.R["0"] = 0x0001
        else:
            self.R["0"] = 0x0000


    # =====================================
    # SALTOS
    # =====================================

    def salta_igual(self, r, val, dir):
        if self.R[r] == int(val,16):
            return int(dir,16)
        return None

    def salta_dif(self, r, val, dir):
        if self.R[r] != int(val,16):
            return int(dir,16)
        return None


    # =====================================
    # EJECUCIÓN
    # =====================================

    def fetchDecodeExecute(self, Ins):

        if not self.Vivo:
            return None

        # Si está sobre bomba y no desactiva = muerte
        if self.SobreBomba and Ins != "negro_desactiva":
            self.Vivo = False
            print(" Boome explotó por no desactivar!")
            return None

        self.ultimaInstruccion = self.InstruccionActual
        self.InstruccionActual = Ins


        # ---- DESACTIVAR BOMBA ----
        if Ins == "negro_desactiva":
            if self.SobreBomba:
                print(" Bomba desactivada!")
                self.Mapa[self.Fila][self.Columna] = "0"
                self.SobreBomba = False
            return None


        # ---- MOVIMIENTOS ----
        if Ins in ["movi","movd","mova","movb"]:
            match Ins:
                case "movi":
                    self.movIzquierda()
                case "movd":
                    self.movDerecha()
                case "mova":
                    self.movArriba()
                case "movb":
                    self.movAbajo()

            if self.Vivo:
                self.checarBomba()
            return None


        # ---- SENSORES ----
        if Ins in ["abelardo je","abelardo dw","abelardo up","abelardo ab"]:
            match Ins:
                case "abelardo je":
                    self.sensIzquierda()
                case "abelardo dw":
                    self.sensDerecha()
                case "abelardo up":
                    self.sensArriba()
                case "abelardo ab":
                    self.sensAbajo()
            return None


        # ---- SALTOS ----
        parts = Ins.split()
        if len(parts) == 4:
            if parts[0] == "salta_igual":
                return self.salta_igual(parts[1][1], parts[2], parts[3])

            if parts[0] == "salta_dif":
                return self.salta_dif(parts[1][1], parts[2], parts[3])


        # ---- ASIGNACION CON SUMA ----
        if len(parts) == 5 and parts[1] == "=" and parts[3] == "+":
            reg = parts[0][1]

            val1 = parts[2]
            val2 = parts[4]

            # ---- Primer operando ----
            if val1.startswith("0x"):
                v1 = int(val1,16)
            elif val1.startswith("r"):
                v1 = self.R[val1[1]]
                if not isinstance(v1, int):
                    return None
            else:
                return None

            # ---- Segundo operando ----
            if val2.startswith("0x"):
                v2 = int(val2,16)
            elif val2.startswith("r"):
                v2 = self.R[val2[1]]
                if not isinstance(v2, int):
                    return None
            else:
                return None

            self.R[reg] = (v1 + v2) & 0xFFFF
            return None


        # ---- ASIGNACION NORMAL ----
        if len(parts) == 3 and parts[1] == "=":
            reg = parts[0][1]
            val = parts[2]

            if val.startswith("0x"):
                self.R[reg] = int(val,16) & 0xFFFF

            elif val.startswith("r"):
                self.R[reg] = self.R[val[1]] & 0xFFFF

            elif val in ["je","dw","up","ab"]:   
                self.R[reg] = val               

            return None