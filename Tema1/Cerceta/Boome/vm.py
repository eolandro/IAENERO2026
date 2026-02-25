DESPLAZA = {
    "je": (0, 1),  # derecha
    "up": (0, -1),  # izquierda
    "ab": (-1, 0),  # arriba
    "dw": (1, 0),  # abajo
}


class BoomeVM:
    def __init__(self, filas=5, columnas=25, cantidad_bombas=8):
        self.filas = filas
        self.columnas = columnas

        self.R = {"r0": 0, "r1": 0, "r2": 0, "r3": 0}
        self.Fila = 0
        self.Col = 0

        self.Mapa = []
        for _ in range(self.filas):
            self.Mapa.append(["."] * self.columnas)

        self.semilla = 12345
        self.colocar_bombas(cantidad_bombas)

        self.Vivo = True
        self.ultimaInstruccion = ""
        self.instruccionActual = ""

    def __str__(self):
        s = ""
        s += "Registros:\n"
        s += (
            "  r0="
            + str(self.R["r0"])
            + "  r1="
            + str(self.R["r1"])
            + "  r2="
            + str(self.R["r2"])
            + "  r3="
            + str(self.R["r3"])
            + "\n"
        )
        s += "Mapa:\n"

        copia = []
        for fila in self.Mapa:
            copia.append(fila[:])

        copia[self.Fila][self.Col] = "B"
        for r in range(self.filas):
            s += "  " + " ".join(copia[r]) + "\n"

        s += "Última: " + self.ultimaInstruccion + "\n"
        s += "Actual : " + self.instruccionActual + "\n"
        s += "Vivo   : " + str(self.Vivo) + "\n"
        s += "-" * 50 + "\n"
        return s

    def dentro(self, r, c):
        return 0 <= r < self.filas and 0 <= c < self.columnas

    def celda(self, r, c):
        if not self.dentro(r, c):
            return " "
        return self.Mapa[r][c]

    def hex_a_int(self, h):
        return int(h, 16)

    def obtener(self, reg):
        return self.R[reg]

    def asignar(self, reg, val):
        self.R[reg] = int(val)

    # Pseudoaleatorio sin imports
    def siguiente_numero(self):
        self.semilla = (self.semilla * 1103515245 + 12345) % 2147483648
        return self.semilla

    def colocar_bombas(self, cantidad):
        puestas = 0
        while puestas < cantidad:
            r = self.siguiente_numero() % self.filas
            c = self.siguiente_numero() % self.columnas

            if r == self.Fila and c == self.Col:
                continue
            if self.Mapa[r][c] == "!":
                continue

            self.Mapa[r][c] = "!"
            puestas += 1

    # Bomba ABAJO
    def hay_bomba_abajo(self):
        r = self.Fila + 1
        c = self.Col
        if not self.dentro(r, c):
            return 0
        return 1 if self.Mapa[r][c] == "!" else 0

    def desactivar_bomba_abajo(self):
        r = self.Fila + 1
        c = self.Col
        if self.dentro(r, c) and self.Mapa[r][c] == "!":
            self.Mapa[r][c] = "."

    # Movimiento
    def mover(self, dr, dc):
        if not self.Vivo:
            return

        nr = self.Fila + dr
        nc = self.Col + dc

        # Salir del mapa: NO muere, NO se mueve
        if not self.dentro(nr, nc):
            return

        self.Fila = nr
        self.Col = nc

        # Pisar bomba: SÍ muere
        if self.Mapa[self.Fila][self.Col] == "!":
            self.Vivo = False
            print("BOOM! Pisó una bomba")

    def execute(self, tokens, pc):
        if not self.Vivo:
            return pc + 1

        self.ultimaInstruccion = self.instruccionActual
        if tokens:
            self.instruccionActual = " ".join(tokens)
        else:
            self.instruccionActual = ""

        if not tokens:
            return pc + 1

        # Movimientos
        if len(tokens) == 1 and tokens[0] in ["movi", "movd", "mova", "movb"]:
            ins = tokens[0]
            if ins == "movi":
                self.mover(0, -1)
            elif ins == "movd":
                self.mover(0, 1)
            elif ins == "mova":
                self.mover(-1, 0)
            elif ins == "movb":
                self.mover(1, 0)
            return pc + 1

        # Desactivar bomba ABAJO
        if len(tokens) == 1 and tokens[0] == "desactivar":
            self.desactivar_bomba_abajo()
            return pc + 1

        # Saltos
        if len(tokens) == 4 and tokens[0] in ["salta_igual", "salta_dif"]:
            op = tokens[0]
            reg = tokens[1]
            val_hex = tokens[2]
            dest_hex = tokens[3]

            val = self.hex_a_int(val_hex)
            dest = self.hex_a_int(dest_hex) - 1

            rv = self.obtener(reg)

            if op == "salta_igual":
                if rv == val:
                    return dest
            else:
                if rv != val:
                    return dest

            return pc + 1

        # Asignación: r0 = 0x.. | r0 = r1 | r0 = bomba (ABAJO)
        if len(tokens) == 3 and tokens[1] == "=":
            reg = tokens[0]
            rhs = tokens[2]

            if rhs.startswith("0x"):
                self.asignar(reg, self.hex_a_int(rhs))
            elif rhs in self.R:
                self.asignar(reg, self.obtener(rhs))
            elif rhs == "bomba":
                self.asignar(reg, self.hay_bomba_abajo())

            return pc + 1

        # Sensor direccional: r0 = bomba je|up|ab|dw
        if len(tokens) == 4 and tokens[1] == "=" and tokens[2] == "bomba":
            reg = tokens[0]
            dire = tokens[3]
            dr, dc = DESPLAZA[dire]
            rr = self.Fila + dr
            cc = self.Col + dc
            self.asignar(reg, 1 if self.celda(rr, cc) == "!" else 0)
            return pc + 1

        # Aritmética
        if len(tokens) == 5 and tokens[1] == "=":
            destino = tokens[0]
            a = tokens[2]
            op = tokens[3]
            b = tokens[4]

            valor_a = self.obtener(a)
            if b.startswith("0x"):
                valor_b = self.hex_a_int(b)
            else:
                valor_b = self.obtener(b)

            if op == "+":
                self.asignar(destino, valor_a + valor_b)
            else:
                self.asignar(destino, valor_a - valor_b)

            return pc + 1

        return pc + 1
