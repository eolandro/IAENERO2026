# vm.py
# COMPLETO, SIN RECORTES

import random

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

        # Para impresión en consola
        self.ultimaInstruccion = ""
        self.instruccionActual = ""

        # Vida del agente
        self.Vivo = True

        # Si está parado sobre una bomba '*'
        self.EnBomba = False

        # Estado para Bayes
        self.P_D_POS_BOMBA = 0.9
        self.P_D_NEG_BOMBA = 0.1
        self.P_D_POS_NO_BOMBA = 0.2
        self.P_D_NEG_NO_BOMBA = 0.8

        self.total_bombas_reales = 0
        self.total_celdas = len(self.Mapa) * len(self.Mapa[0])
        self.celdas_resueltas = set()
        self.bombas_deshabilitadas = set()
        self.max_deshabilitaciones = 3
        self.deshabilitaciones_usadas = 0
        self._reiniciar_conocimiento()

    def __str__(self):
        Ret = "Registros\n"
        Ret += f"R0: {self.R['0']}\n"
        Ret += f"R1: {self.R['1']}\n"
        Ret += f"R2: {self.R['2']}\n"
        Ret += f"R3: {self.R['3']}\n"
        Ret += f"Posicion (Fila,Col): ({self.Fila},{self.Columna})\n"
        Ret += f"EnBomba: {self.EnBomba}\n"
        Ret += f"Deshabilitaciones: {self.deshabilitaciones_usadas}/{self.max_deshabilitaciones}\n"

        Mapa = [fila[:] for fila in self.Mapa]
        Mapa[self.Fila][self.Columna] = "B"
        for fila in Mapa:
            Ret += f"{fila}\n"

        Ret += f"Ultima Instruccion: {self.ultimaInstruccion}\n"
        Ret += f"Instruccion Actual: {self.instruccionActual}\n"
        Ret += f"Vivo: {self.Vivo}\n"
        Ret += "------------------------------------------------------------"
        return Ret

    # =========================
    # Helpers de tokens (token completo)
    # =========================
    def _es_reg(self, tok: str) -> bool:
        return tok in ["r0", "r1", "r2", "r3"]

    def _reg_key(self, tok: str) -> str:
        # tok es r0..r3
        return tok[1]

    def _valor_token(self, tok: str):
        # Convierte un token a int:
        # - r0..r3 => valor del registro
        # - 0x..   => entero en base 16
        if self._es_reg(tok):
            return self.R[self._reg_key(tok)]
        if tok.startswith("0x"):
            try:
                return int(tok, 16)
            except Exception:
                return None
        return None

    def _coord_vecina(self, dr):
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
            return None

        if nf < 0 or nf >= len(self.Mapa):
            return None
        if nc < 0 or nc >= len(self.Mapa[nf]):
            return None

        return (nf, nc)

    def _reiniciar_conocimiento(self):
        self.celdas_resueltas = set()
        self.bombas_deshabilitadas = set()
        self.deshabilitaciones_usadas = 0
        self.total_celdas = len(self.Mapa) * len(self.Mapa[0])

        if self.Mapa[self.Fila][self.Columna] == "*":
            self.EnBomba = True
        else:
            self.EnBomba = False
            self.celdas_resueltas.add((self.Fila, self.Columna))

    def _prior_bomba_actual(self):
        bombas_restantes = self.total_bombas_reales - len(self.bombas_deshabilitadas)
        desconocidas = self.total_celdas - len(self.celdas_resueltas)

        if desconocidas <= 0:
            return 0.0

        prior = bombas_restantes / desconocidas
        if prior < 0:
            return 0.0
        if prior > 1:
            return 1.0
        return prior

    def _posterior_bayes_d_positivo(self, prior):
        numerador = self.P_D_POS_BOMBA * prior
        denominador = numerador + (self.P_D_POS_NO_BOMBA * (1 - prior))
        if denominador == 0:
            return 0.0
        return numerador / denominador

    def _posterior_bayes_d_negativo(self, prior):
        numerador = self.P_D_NEG_BOMBA * prior
        denominador = numerador + (self.P_D_NEG_NO_BOMBA * (1 - prior))
        if denominador == 0:
            return 0.0
        return numerador / denominador

    def _resolver_bomba_con_bayes(self):
        # Solo aplica si realmente está sobre una bomba
        if self.Mapa[self.Fila][self.Columna] != "*":
            self.EnBomba = False
            return True

        if self.deshabilitaciones_usadas >= self.max_deshabilitaciones:
            print("Sin oportunidades de deshabilitar restantes. Boome muere.")
            return False

        prior = self._prior_bomba_actual()

        # Evidencia del detector sobre la celda actual (bomba real)
        d_positivo = 1 if random.random() < self.P_D_POS_BOMBA else 0

        if d_positivo == 1:
            posterior = self._posterior_bayes_d_positivo(prior)
            print(f"Decision Bayes sobre bomba en ({self.Fila},{self.Columna})")
            print(f"Detector positivo sobre celda actual")
            print(f"Prior actual: {prior:.6f}")
            print(f"P(Bomba|D+) = {posterior:.6f}")

            self.Mapa[self.Fila][self.Columna] = "0"
            self.bombas_deshabilitadas.add((self.Fila, self.Columna))
            self.deshabilitaciones_usadas += 1
            self.celdas_resueltas.add((self.Fila, self.Columna))
            self.EnBomba = False
            return True

        posterior = self._posterior_bayes_d_negativo(prior)
        print(f"Decision Bayes sobre bomba en ({self.Fila},{self.Columna})")
        print(f"Detector negativo sobre celda actual")
        print(f"Prior actual: {prior:.6f}")
        print(f"P(Bomba|D-) = {posterior:.6f}")
        print("No se deshabilita la bomba. Boome muere.")
        return False

    def cargar_mapa(self, mapa):
        if not mapa or not mapa[0]:
            self.Vivo = False
            return

        ancho = len(mapa[0])
        for fila in mapa:
            if len(fila) != ancho:
                self.Vivo = False
                return

        self.Mapa = [fila[:] for fila in mapa]
        self.Fila = 0
        self.Columna = 0
        self.Vivo = True
        self.ultimaInstruccion = ""
        self.instruccionActual = ""
        self.total_bombas_reales = sum(1 for fila in self.Mapa for c in fila if c == "*")
        self._reiniciar_conocimiento()

    def insertar_bombas_aleatorias(self, cantidad=3):
        # Limpia bombas existentes del mapa base
        for i in range(len(self.Mapa)):
            for j in range(len(self.Mapa[i])):
                if self.Mapa[i][j] == "*":
                    self.Mapa[i][j] = "0"

        candidatas = []
        for i in range(len(self.Mapa)):
            for j in range(len(self.Mapa[i])):
                if (i, j) != (self.Fila, self.Columna):
                    candidatas.append((i, j))

        if not candidatas:
            self.total_bombas_reales = 0
            self._reiniciar_conocimiento()
            return

        cantidad_real = min(cantidad, len(candidatas))
        seleccionadas = random.sample(candidatas, cantidad_real)

        for i, j in seleccionadas:
            self.Mapa[i][j] = "*"

        self.total_bombas_reales = cantidad_real
        self._reiniciar_conocimiento()

    def detectorProbabilistico(self, dr):
        coord = self._coord_vecina(dr)
        hay_bomba = False

        if coord is not None:
            f, c = coord
            hay_bomba = self.Mapa[f][c] == "*"

        prob_positivo = self.P_D_POS_BOMBA if hay_bomba else self.P_D_POS_NO_BOMBA
        d_positivo = 1 if random.random() < prob_positivo else 0

        if d_positivo == 1:
            prior = self._prior_bomba_actual()
            posterior = self._posterior_bayes_d_positivo(prior)

            if coord is None:
                destino = "fuera del mapa"
            else:
                destino = f"({coord[0]},{coord[1]})"

            print(f"Detector positivo en direccion {dr} sobre casilla {destino}")
            print(f"Prior actual: {prior:.6f}")
            print(f"Bayes D+ -> P(Bomba|D+) = {posterior:.6f}")

        return d_positivo

    # =========================
    # MOVIMIENTOS (si sale del mapa -> muere, sin error)
    # =========================
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

    # =========================
    # SENSOR (abelardo)
    # 0 = libre ("0")
    # 1 = bloqueado (fuera del mapa o != "0")
    # =========================
    def sensorAbelardo(self, dr):
        coord = self._coord_vecina(dr)
        if coord is None:
            return 1

        nf, nc = coord

        return 0 if self.Mapa[nf][nc] == "0" else 1

    # =========================
    # BOMBAS
    # =========================
    def _revisar_bomba_pisada(self):
        if self.Mapa[self.Fila][self.Columna] == "*":
            self.EnBomba = True
        else:
            self.celdas_resueltas.add((self.Fila, self.Columna))

    # =========================
    # SALTOS (en la VM)
    # =========================
    def _ejecutar_salto(self, tokens, pc, n):
        # tokens = [op, x, y, z]
        op, x, y, z = tokens

        vx = self._valor_token(x)
        vy = self._valor_token(y)
        vz = self._valor_token(z)

        if vx is None or vy is None or vz is None:
            self.Vivo = False
            return pc

        hacer_salto = (vx == vy) if op == "salta_igual" else (vx != vy)

        if hacer_salto:
            if vz < 0 or vz >= n:
                self.Vivo = False
                return pc
            return vz

        return pc + 1

    # =========================
    # EXECUTE (1 instrucción) - sin excepciones
    # =========================
    def fetchDecodeExecute(self, Instruccion):
        if not self.Vivo:
            return

        self.ultimaInstruccion = self.instruccionActual
        self.instruccionActual = Instruccion.strip()

        # Decisión automática por Bayes al estar sobre bomba
        if self.EnBomba:
            if not self._resolver_bomba_con_bayes():
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
                        # Solo hay 3 oportunidades de desactivar bombas reales
                        if self.Mapa[self.Fila][self.Columna] == "*":
                            if self.deshabilitaciones_usadas >= self.max_deshabilitaciones:
                                self.Vivo = False
                                return

                            self.Mapa[self.Fila][self.Columna] = "0"
                            self.bombas_deshabilitadas.add((self.Fila, self.Columna))
                            self.deshabilitaciones_usadas += 1
                            self.celdas_resueltas.add((self.Fila, self.Columna))

                        self.EnBomba = False

                    case _:
                        self.Vivo = False

            # Asignación: rX = 0xNN  o  rX = rY
            case [A, "=", B]:
                if not self._es_reg(A):
                    self.Vivo = False
                    return
                regA = self._reg_key(A)

                if B.startswith("0x"):
                    try:
                        self.R[regA] = int(B, 16)
                    except Exception:
                        self.Vivo = False
                        return
                elif self._es_reg(B):
                    self.R[regA] = self.R[self._reg_key(B)]
                else:
                    self.Vivo = False
                    return

            # Asignación con sensor: rX = abelardo dr
            case [A, "=", "abelardo", dr]:
                if not self._es_reg(A):
                    self.Vivo = False
                    return
                regA = self._reg_key(A)
                self.R[regA] = self.sensorAbelardo(dr)

            # Asignación con detector bayesiano: rX = detector dr
            case [A, "=", "detector", dr]:
                if not self._es_reg(A):
                    self.Vivo = False
                    return
                regA = self._reg_key(A)
                self.R[regA] = self.detectorProbabilistico(dr)

            # Asignación aritmética: rX = rY +/- (rZ | 0xNN)
            case [A, "=", B, OP, C]:
                if not self._es_reg(A) or not self._es_reg(B):
                    self.Vivo = False
                    return
                if OP not in ["+", "-"]:
                    self.Vivo = False
                    return

                valor_c = self._valor_token(C)
                if valor_c is None:
                    self.Vivo = False
                    return

                regA = self._reg_key(A)
                valor_b = self.R[self._reg_key(B)]

                if OP == "+":
                    self.R[regA] = valor_b + valor_c
                else:
                    self.R[regA] = valor_b - valor_c

            case _:
                self.Vivo = False

    # =========================
    # STEP: ejecuta 1 instrucción y regresa el nuevo PC
    # =========================
    def step(self, Instruccion, pc, n):
        if not self.Vivo:
            return pc

        instruccion = Instruccion.strip()
        tokens = [t for t in instruccion.split(" ") if t]

        # Registrar instrucción actual para consola
        self.ultimaInstruccion = self.instruccionActual
        self.instruccionActual = instruccion

        # Si es salto, lo resuelve la VM
        if len(tokens) == 4 and tokens[0] in ["salta_igual", "salta_dif"]:
            return self._ejecutar_salto(tokens, pc, n)

        # Si no es salto, ejecuta normal
        self.fetchDecodeExecute(instruccion)
        return pc + 1