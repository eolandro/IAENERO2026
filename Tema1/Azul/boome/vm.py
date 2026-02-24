class BoomeVM:
    def __init__(self):
        # Registros de proposito general
        self.R = {"0": 0, "1": 0, "2": 0, "3": 0}
        # Posicion de boome
        self.Columna = 0
        self.Fila = 0
        # Mapa: "0" = nada, "/" = pared, "1" = bomba
        self.Mapa = [
            ["0", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
            ["0", "0", "/", "0", "1", "0", "0", "0", "/", "0"],
            ["0", "0", "0", "0", "/", "0", "0", "0", "0", "0"],
            ["0", "0", "1", "0", "0", "0", "/", "0", "1", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        ]
        # Estado de boome
        self.Vivo = True
        self.sobreBomba = False
        # Control de instrucciones
        self.ultimaInstruccion = ""
        self.InstruccionActual = ""
        # Program counter para saltos
        self.pc = 0
        # Lista de instrucciones del programa
        self.programa = []

    # Representacion del estado actual de boome
    def __str__(self):
        ret = f"Registros\nR0: {self.R['0']}\n"
        ret += f"R1: {self.R['1']}\n"
        ret += f"R2: {self.R['2']}\n"
        ret += f"R3: {self.R['3']}\n"
        # Copia del mapa para mostrar posicion
        mapa = [fila[:] for fila in self.Mapa]
        mapa[self.Fila][self.Columna] = "B"
        for fila in mapa:
            ret += f"{fila}\n"
        ret += f"Ultima instruccion: {self.ultimaInstruccion}\n"
        ret += f"Instruccion actual: {self.InstruccionActual}\n"
        ret += f"Vivo: {self.Vivo}\n"
        ret += "-----------------------------------------------\n"
        return ret

    # Obtiene el valor de un registro o numero hexadecimal
    def obtener_valor(self, token):
        # Si es un registro, retorna su valor
        if token in ["r0", "r1", "r2", "r3"]:
            return self.R[token[1]]
        # Si es numhex, convierte a entero
        if token[:2] == "0x":
            return int(token[2:], 16)
        return 0

    # Mueve a boome a la izquierda
    def movIzquierda(self):
        nueva_col = self.Columna - 1
        # Verifica si se sale del borde
        if nueva_col < 0:
            self.Vivo = False
            return
        # Verifica si hay obstaculo
        if self.Mapa[self.Fila][nueva_col] == "/":
            self.Vivo = False
            return
        # Verifica si estaba sobre bomba sin desactivar
        self._verificar_salida_bomba()
        if not self.Vivo:
            return
        self.Columna = nueva_col
        # Verifica si pisa una bomba
        self._verificar_piso_bomba()

    # Mueve a boome a la derecha
    def movDerecha(self):
        nueva_col = self.Columna + 1
        # Verifica si se sale del borde
        if nueva_col >= len(self.Mapa[self.Fila]):
            self.Vivo = False
            return
        # Verifica si hay obstaculo
        if self.Mapa[self.Fila][nueva_col] == "/":
            self.Vivo = False
            return
        # Verifica si estaba sobre bomba sin desactivar
        self._verificar_salida_bomba()
        if not self.Vivo:
            return
        self.Columna = nueva_col
        # Verifica si pisa una bomba
        self._verificar_piso_bomba()

    # Mueve a boome hacia arriba
    def movArriba(self):
        nueva_fila = self.Fila - 1
        # Verifica si se sale del borde
        if nueva_fila < 0:
            self.Vivo = False
            return
        # Verifica si hay obstaculo
        if self.Mapa[nueva_fila][self.Columna] == "/":
            self.Vivo = False
            return
        # Verifica si estaba sobre bomba sin desactivar
        self._verificar_salida_bomba()
        if not self.Vivo:
            return
        self.Fila = nueva_fila
        # Verifica si pisa una bomba
        self._verificar_piso_bomba()

    # Mueve a boome hacia abajo
    def movAbajo(self):
        nueva_fila = self.Fila + 1
        # Verifica si se sale del borde
        if nueva_fila >= len(self.Mapa):
            self.Vivo = False
            return
        # Verifica si hay obstaculo
        if self.Mapa[nueva_fila][self.Columna] == "/":
            self.Vivo = False
            return
        # Verifica si estaba sobre bomba sin desactivar
        self._verificar_salida_bomba()
        if not self.Vivo:
            return
        self.Fila = nueva_fila
        # Verifica si pisa una bomba
        self._verificar_piso_bomba()

    # Verifica si boome pisa una bomba al llegar a una celda
    def _verificar_piso_bomba(self):
        if self.Mapa[self.Fila][self.Columna] == "1":
            self.sobreBomba = True

    # Si boome estaba sobre una bomba y se mueve sin desactivarla, c muere
    def _verificar_salida_bomba(self):
        if self.sobreBomba:
            self.Vivo = False

    # Desactiva la bomba en la celda actual
    def desactivar_bomba(self):
        if self.Mapa[self.Fila][self.Columna] == "1":
            self.Mapa[self.Fila][self.Columna] = "0"
            self.sobreBomba = False

    # Sensor abelardo: lee la celda adyacente en la direccion dada
    # Retorna 1 si hay bomba u obstaculo, 0 si libre o fuera del mapa
    def sensor_abelardo(self, direccion):
        fila = self.Fila
        col = self.Columna
        # Calcula la celda a revisar segun la direccion
        if direccion == "ab":
            col -= 1
        elif direccion == "je":
            col += 1
        elif direccion == "up":
            fila -= 1
        elif direccion == "dw":
            fila += 1
        # Fuera del mapa se considera obstaculo
        if fila < 0 or fila >= len(self.Mapa):
            return 1
        if col < 0 or col >= len(self.Mapa[0]):
            return 1
        # Revisa el contenido de la celda
        celda = self.Mapa[fila][col]
        if celda in ["/", "1"]:
            return 1
        return 0

    # Ejecuta una instruccion tokenizada
    def fetchDecodeExecute(self, tokens):
        if not self.Vivo:
            return
        # Actualiza historial de instrucciones
        self.ultimaInstruccion = self.InstruccionActual
        self.InstruccionActual = " ".join(tokens)

        # Movimientos (1 token)
        if len(tokens) == 1 and tokens[0] in ["movi", "movd", "mova", "movb"]:
            if tokens[0] == "movi":
                self.movIzquierda()
            elif tokens[0] == "movd":
                self.movDerecha()
            elif tokens[0] == "mova":
                self.movArriba()
            elif tokens[0] == "movb":
                self.movAbajo()
            self.pc += 1
            return

        # Asignacion simple: reg = valor (3 tokens)
        if len(tokens) == 3 and tokens[1] == "=":
            reg = tokens[0][1]
            self.R[reg] = self.obtener_valor(tokens[2])
            self.pc += 1
            return

        # Asignacion con sensor: reg = abelardo dir (4 tokens)
        if len(tokens) == 4 and tokens[1] == "=" and tokens[2] == "abelardo":
            reg = tokens[0][1]
            self.R[reg] = self.sensor_abelardo(tokens[3])
            self.pc += 1
            return

        # Saltos condicionales: salta_igual/salta_dif val1 val2 destino (4 tokens)
        if len(tokens) == 4 and tokens[0] in ["salta_igual", "salta_dif"]:
            val1 = self.obtener_valor(tokens[1])
            val2 = self.obtener_valor(tokens[2])
            destino = self.obtener_valor(tokens[3])
            if tokens[0] == "salta_igual" and val1 == val2:
                self.pc = destino
            elif tokens[0] == "salta_dif" and val1 != val2:
                self.pc = destino
            else:
                self.pc += 1
            return

        # Asignacion con operacion: reg = val oper val (5 tokens)
        if len(tokens) == 5 and tokens[1] == "=" and tokens[3] in ["+", "-"]:
            reg = tokens[0][1]
            val_izq = self.obtener_valor(tokens[2])
            val_der = self.obtener_valor(tokens[4])
            if tokens[3] == "+":
                self.R[reg] = val_izq + val_der
            else:
                self.R[reg] = val_izq - val_der
            self.pc += 1
            return

        # Instruccion no reconocida
        self.pc += 1

    # Ejecuta el programa completo instruccion por instruccion
    def ejecutar(self):
        print(self)
        while self.pc < len(self.programa) and self.Vivo:
            tokens = self.programa[self.pc]
            self.fetchDecodeExecute(tokens)
            print(self)