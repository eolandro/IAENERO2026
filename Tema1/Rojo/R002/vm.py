# vm.py
# COMPLETO, SIN RECORTES

class BoomeVM:
    def __init__(self):
        # Registros generales (r0..r3)
        self.R = {"0": 0, "1": 0, "2": 0, "3": 0}

        # Posición actual en el mapa
        self.Columna = 0
        self.Fila = 0

        # Mapa base: 5 filas x 10 columnas
        self.Mapa = [
            ["0"] * 10,
            ["0"] * 10,
            ["0"] * 10,
            ["0"] * 10,
            ["0"] * 10
        ]

        # Estado de ejecución
        self.ultimaInstruccion = ""
        self.instruccionActual = ""
        self.Vivo = True

        # Indica si el personaje está parado sobre una bomba
        self.EnBomba = False

    def __str__(self):
        Ret = "Registros\n"
        Ret += f"R0: {self.R['0']}\n"
        Ret += f"R1: {self.R['1']}\n"
        Ret += f"R2: {self.R['2']}\n"
        Ret += f"R3: {self.R['3']}\n"
        Ret += f"Posicion (Fila,Col): ({self.Fila},{self.Columna})\n"
        Ret += f"EnBomba: {self.EnBomba}\n"

        # Copia del mapa para mostrar la posición actual con 'B'
        Mapa = [fila[:] for fila in self.Mapa]
        Mapa[self.Fila][self.Columna] = "B"
        for fila in Mapa:
            Ret += f"{fila}\n"

        Ret += f"Ultima Instruccion: {self.ultimaInstruccion}\n"
        Ret += f"Instruccion Actual: {self.instruccionActual}\n"
        Ret += f"Vivo: {self.Vivo}\n"
        Ret += "------------------------------------------------------------"
        return Ret

    def _revisar_bomba_pisada(self):
        # Marca EnBomba si la celda actual es una bomba
        if self.Mapa[self.Fila][self.Columna] == "*":
            self.EnBomba = True

    # Movimientos básicos
    def movIzquierda(self):
        self.Columna -= 1
        if self.Columna < 0:
            self.Columna += 1
            self.Vivo = False

    def movDerecha(self):
        self.Columna += 1
        if self.Columna >= len(self.Mapa[self.Fila]):
            self.Columna -= 1
            self.Vivo = False

    def movArriba(self):
        self.Fila -= 1
        if self.Fila < 0:
            self.Fila += 1
            self.Vivo = False

    def movAbajo(self):
        self.Fila += 1
        if self.Fila >= len(self.Mapa):
            self.Fila -= 1
            self.Vivo = False

    # Sensor "abelardo"
    # Regresa 0 si la casilla consultada está libre ("0")
    # Regresa 1 si está fuera del mapa o si está ocupada por algo distinto de "0"
    def sensorAbelardo(self, dr):
        nf = self.Fila
        nc = self.Columna

        if dr == "ab":
            nf = self.Fila + 1
        elif dr == "up":
            nf = self.Fila - 1
        elif dr == "je":
            nc = self.Columna - 1
        elif dr == "dw":
            nc = self.Columna + 1
        else:
            return 1

        if nf < 0 or nf >= len(self.Mapa):
            return 1
        if nc < 0 or nc >= len(self.Mapa[nf]):
            return 1

        return 0 if self.Mapa[nf][nc] == "0" else 1

    # Ejecuta una instrucción sobre la VM
    def fetchDecodeExecute(self, Instruccion):
        if not self.Vivo:
            return

        self.ultimaInstruccion = self.instruccionActual
        self.instruccionActual = Instruccion.strip()

        # Si está sobre bomba y no se deshabilita, termina la ejecución
        if self.EnBomba and self.instruccionActual != "deshabilitar":
            self.Vivo = False
            return

        LStr = self.instruccionActual.split(" ")
        LStr = [s for s in LStr if s]

        match LStr:
            case [Ins]:
                match Ins:
                    case "movi":
                        self.movIzquierda()
                        if self.Vivo:
                            self._revisar_bomba_pisada()

                    case "movd":
                        self.movDerecha()
                        if self.Vivo:
                            self._revisar_bomba_pisada()

                    case "mova":
                        self.movArriba()
                        if self.Vivo:
                            self._revisar_bomba_pisada()

                    case "movb":
                        self.movAbajo()
                        if self.Vivo:
                            self._revisar_bomba_pisada()

                    case "deshabilitar":
                        # Si hay bomba en la celda actual, se convierte a libre
                        if self.Mapa[self.Fila][self.Columna] == "*":
                            self.Mapa[self.Fila][self.Columna] = "0"
                        self.EnBomba = False

                    case _:
                        self.Vivo = False

            # Asignación: rX = 0xNN  o  rX = rY
            case [A, "=", B]:
                if not (A.startswith("r") and len(A) == 2 and A[1] in self.R):
                    self.Vivo = False
                    return
                regA = A[1]

                if B.startswith("0x"):
                    try:
                        self.R[regA] = int(B, 16)
                    except Exception:
                        self.Vivo = False
                        return
                elif B.startswith("r") and len(B) == 2 and B[1] in self.R:
                    self.R[regA] = self.R[B[1]]
                else:
                    self.Vivo = False
                    return

            # Asignación con sensor: rX = abelardo dr
            case [A, "=", "abelardo", dr]:
                if not (A.startswith("r") and len(A) == 2 and A[1] in self.R):
                    self.Vivo = False
                    return
                regA = A[1]
                self.R[regA] = self.sensorAbelardo(dr)

            case _:
                self.Vivo = False