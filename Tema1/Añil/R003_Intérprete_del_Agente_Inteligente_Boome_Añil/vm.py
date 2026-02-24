class BoomeVM:

    def __init__(self):
        self.R = {"r0":0,"r1":0,"r2":0,"r3":0}

        self.Fila = 0
        self.Col = 0

        self.Mapa = [
            ["0","0","0","0","0","0","0","0","X","0"],
            ["0","0","X","0","0","0","0","0","0","0"],
            ["0","0","M","0","0","M","0","X","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","X","0","0","0","0","M","0"]
        ]

        self.Vivo = True
        self.SobreMina = False
        self.ultima = ""
        self.actual = ""

    # ---------------- REPRESENTACION ----------------

    def __str__(self):
        txt = "\nRegistros:\n"
        for k in self.R:
            txt += f"{k.upper()}: 0x{self.R[k]:04X}\n"

        M = [f[:] for f in self.Mapa]
        M[self.Fila][self.Col] = "B"

        for f in M:
            txt += str(f) + "\n"

        txt += f"Ultima: {self.ultima}\n"
        txt += f"Actual: {self.actual}\n"
        txt += f"Vivo: {self.Vivo}\n"
        txt += "-"*40
        return txt

    # ---------------- MOVIMIENTOS ----------------

    def mover(self, nueva_fila, nueva_col):
        if nueva_fila < 0 or nueva_fila >= len(self.Mapa):
            self.Vivo = False
            return
        if nueva_col < 0 or nueva_col >= len(self.Mapa[0]):
            self.Vivo = False
            return

        celda = self.Mapa[nueva_fila][nueva_col]

        self.Fila = nueva_fila
        self.Col = nueva_col

        if celda == "X":
            self.Vivo = False
        elif celda == "M":
            self.SobreMina = True

    def movIzquierda(self):
        self.mover(self.Fila, self.Col - 1)

    def movDerecha(self):
        self.mover(self.Fila, self.Col + 1)

    def movArriba(self):
        self.mover(self.Fila - 1, self.Col)

    def movAbajo(self):
        self.mover(self.Fila + 1, self.Col)

    # ---------------- SENSOR ----------------

    def sensor(self, direccion):
        self.R["r0"] = 0

        movimientos = {
            "iz": (0,-1),
            "de": (0,1),
            "ar": (-1,0),
            "ab": (1,0)
        }

        df, dc = movimientos[direccion]
        nf = self.Fila + df
        nc = self.Col + dc

        if nf < 0 or nf >= len(self.Mapa) or nc < 0 or nc >= len(self.Mapa[0]):
            self.R["r0"] = 1
        elif self.Mapa[nf][nc] != "0":
            self.R["r0"] = 1

    # ---------------- SALTOS ----------------

    def salta_igual(self, reg, valor_hex, destino_hex):
        if self.R[reg] == int(valor_hex,16):
            return int(destino_hex,16)
        return None

    def salta_diferente(self, reg, valor_hex, destino_hex):
        if self.R[reg] != int(valor_hex,16):
            return int(destino_hex,16)
        return None

    # ---------------- EJECUCION ----------------

    def ejecutar(self, ins):
        self.ultima = self.actual
        self.actual = ins

        if not self.Vivo:
            return None

        if self.SobreMina and ins != "desactiva_mina":
            print(" BOOME EXPLOTO ")
            self.Vivo = False
            return None

        if ins == "desactiva_mina":
            if self.SobreMina:
                self.Mapa[self.Fila][self.Col] = "0"
                self.SobreMina = False
                print(" MINA DESACTIVADA ")
            return None

        partes = ins.split()

        if ins in ["movi","movd","mova","movb"]:
            {
                "movi": self.movIzquierda,
                "movd": self.movDerecha,
                "mova": self.movArriba,
                "movb": self.movAbajo
            }[ins]()
            return None

        if partes[0] == "sensor":
            self.sensor(partes[1])
            return None

        if len(partes) == 3:
            destino = partes[0]
            op = partes[2]
            valor = self.R[op] if op.startswith("r") else int(op,16)
            self.R[destino] = valor & 0xFFFF
            return None

        if len(partes) == 5:
            destino = partes[0]
            op1 = partes[2]
            operador = partes[3]
            op2 = partes[4]

            v1 = self.R[op1] if op1.startswith("r") else int(op1,16)
            v2 = self.R[op2] if op2.startswith("r") else int(op2,16)

            if operador == "+":
                resultado = v1 + v2
            else:
                resultado = v1 - v2

            self.R[destino] = resultado & 0xFFFF
            return None

        if partes[0] == "salta_igual":
            return self.salta_igual(partes[1], partes[2], partes[3])

        if partes[0] == "salta_diferente":
            return self.salta_diferente(partes[1], partes[2], partes[3])

        return None