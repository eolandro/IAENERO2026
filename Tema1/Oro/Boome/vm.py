class BoomeVM:

    def __init__(self):

        """

        Registro: Es como la memoria RAM del robot, pero solo hay 4 espacios.

        Registros del boome - self.R es un diccionario que guarda 4 registros:

            "0" (r0) empieza en 0

            "1" (r1) empieza en 1

            "2" (r2) empieza en 2

            "3" (r3) empieza en 3
        """

        self.R = {"r0":0,"r1":0,"r2":0,"r3":0}

        # Posición inicial del robot
        self.Columna = 0
        self.Fila = 0

        # Crear el mapa 5 X 10
        self.Mapa = [
            ["0", "2", "2", "2", "2", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "1", "0", "0", "0"],
            ["0", "1", "0", "2", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "2", "0", "1", "0", "0"]
        ]


        self.obstaculo = "1"
        self.bomba = "2"

        # La ultima construccion que se ejecuto
        self.ultimaInstruccion = ""
        self.Vivo = True
        self.InstruccionActual = ""

    def __str__(self):

        Ret = f"Registros\nR0: {self.R["r0"]}\n"
        Ret += f"R1: {self.R["r1"]} \n"
        Ret += f"R2: {self.R["r2"]} \n"
        Ret += f"R3: {self.R["r3"]} \n"

        # [:] Sirve específicamente para crear una copia superficial
        Mapa = [fila[:] for fila in self.Mapa]

        Mapa[self.Fila][self.Columna] = "B"

        for fila in Mapa:
            Ret += f'{fila}\n'

        Ret += f'Ultima instruccion : {self.ultimaInstruccion}\n'
        Ret += f'Instruccion actual : {self.InstruccionActual}\n'
        Ret += f'Vivo : {self.Vivo}\n'
        Ret += f'----------------------------------------------\n'
        return Ret


    def movIzquierda(self):

        self.Columna = self.Columna -1

        if self.Columna  < 0:
            print("Boome se ha salido del mapa")
            self.Vivo = False
            self.Columna = self.Columna + 1

        else:

            self.detectar_bomba()

            if  self.Mapa[self.Fila][self.Columna]== self.obstaculo:
                self.Vivo = False
                print("Boome se ha estrellado")


    def movDerecha(self):

        self.Columna = self.Columna + 1

        if self.Columna  >= len(self.Mapa[self.Fila]):
            print("Boome se ha salido del mapa")
            self.Vivo = False
            self.Columna = self.Columna - 1

        else:

            self.detectar_bomba()

            if  self.Mapa[self.Fila][self.Columna] == self.obstaculo:
                self.Vivo = False
                print("Boome se ha estrellado")

    def movArriba(self):

        self.Fila = self.Fila -1

        self.detectar_bomba()

        if self.Fila  < 0:
            print("Boome se ha salido del mapa")
            self.Vivo = False
            self.Fila = self.Fila + 1

        else:

            self.detectar_bomba()

            if  self.Mapa[self.Fila][self.Columna]== self.obstaculo:
                self.Vivo = False
                print("Boome se ha estrellado")

    def movAbajo(self):
        self.Fila = self.Fila + 1

        if self.Fila  >= len(self.Mapa):
            print("Boome se ha salido del mapa")
            self.Vivo = False
            self.Fila = self.Fila - 1

        else:

            self.detectar_bomba()

            if  self.Mapa[self.Fila][self.Columna]== self.obstaculo:
                self.Vivo = False
                print("Boome se ha estrellado")


    def leer_sensor(self,direccion):


        # Retorna: 0 = No hay nada, 1 = Hay obstáculo o bomba"""

        # Obtener la posición ACTUAL del robot
        fila,col = self.Fila, self.Columna

        # izquierda
        if direccion == "ab":
            col -= 1

        # derecha
        elif direccion == "je":
            col += 1

        # abajo
        elif direccion == "dw":
            fila += 1

        # arriba
        elif direccion == "up":
            fila -= 1

        # VERIFICAR que la nueva posición está DENTRO del mapa

        if (fila >= 0 and fila < len(self.Mapa)) and (col >= 0 and col < len(self.Mapa[0])):

            valor = self.Mapa[fila][col]

            if valor == "0":
                print(f"Sensor {direccion}: Vacío (0)")
                return 0
            elif valor == self.obstaculo:
                print(f"Sensor {direccion}: Hay algo aqui")
                return 1
            elif valor == self.bomba:
                print(f"Sensor {direccion}: Hay algo aqui")
                return 1

        else:
            print("¡FUERA DEL MAPA!")
            return 1

        return 0


    def obtener_valor(self,operando):

        if operando in self.R:
            return self.R[operando]

        elif operando.startswith("0x"):
            return int(operando,16)

        else:
            return int(operando)

    #  LOGICA DE LA BOMBA
    def detectar_bomba(self):

        if self.Mapa[self.Fila][self.Columna] == self.bomba:

            print(f"¡Has pisado una BOMBA en la posición [{self.Fila},{self.Columna}] ")
            print("¿Quieres desactivar la bomba?")

            while True:
                respuesta = input(" 1 = Desactivar bomba, 2 = No desactivar (Pero no le di importancia) ").strip()

                if respuesta == "1":
                    print("🔧 Bomba desactivada")
                    self.Mapa[self.Fila][self.Columna] = "0"
                    break

                elif respuesta == "2":
                    print(" ¡BOOOOM! La bomba explotó...")
                    print(" Boome ha muerto :( ")
                    self.Vivo = False
                    break

                else:
                    print(" Opción no válida. Ingresa 1 o 2")



    def fetchDecodeExecute(self, instruccion_parseada):

        """
        Ejecutar la instrucción y devolver:
        - True : si debe continuar con la siguiente línea
        - N: si debe saltar a la línea N
        """

        self.ultimaInstruccion = self.InstruccionActual
        self.InstruccionActual = str(instruccion_parseada)

        tipo = instruccion_parseada["tipo"]

        # CASO 1 MOVIMIENTO
        if tipo == "movimiento":
            accion = instruccion_parseada["valor"]

            if accion == "movi":
                self.movIzquierda()
            elif accion == "movd":
                self.movDerecha()
            elif accion == "mova":
                self.movArriba()
            elif accion == "movb":
                self.movAbajo()

            return True

        # CASO 2 SENSOR
        elif tipo == "sensor":
            direccion = instruccion_parseada["direccion"]
            self.leer_sensor(direccion)
            return True

        # CASO 3 ASIGNACION SIMPLE
        elif tipo == "asignacion_simple":
            destino = instruccion_parseada["destino"]
            fuente = instruccion_parseada["fuente"]

            if fuente in self.R:
                self.R[destino] = self.R[fuente]
            else:
                self.R[destino] = self.obtener_valor(fuente)
            
            return True

        # CASO 4 ASIGNACION SENSOR
        elif tipo == "asignacion_sensor":
            destino = instruccion_parseada["destino"]
            direccion = instruccion_parseada["direccion"]
            self.R[destino] = self.leer_sensor(direccion)
            print( "Este es el valor del registro", destino , "despues de asignacion sensor", self.R[destino])

            return  True
        # CASO 5 OPERACION ARITMETICA
        elif tipo == "operacion":
            destino = instruccion_parseada["destino"]

            op1 = self.obtener_valor(instruccion_parseada["operando1"])
            op2 = self.obtener_valor(instruccion_parseada["operando2"])
            operador = instruccion_parseada["operador"]

            if operador == "+":
                self.R[destino] = op1 + op2
            else:  # "-"
                self.R[destino] = op1 - op2


            return True

        # CASO 6 SALTO
        elif tipo == "salto":
            condicion = instruccion_parseada["condicion"]
            op1 = self.obtener_valor(instruccion_parseada["operando1"])
            op2 = self.obtener_valor(instruccion_parseada["operando2"])
            destino = self.obtener_valor(instruccion_parseada["destino"])

            # Depuración de salto
            print(f"Evaluando salto: {condicion} {op1} {op2} -> línea {destino}")

            # Evaluar condición
            if condicion == "salta_igual" and op1 == op2:
                print(f"¡CONDICIÓN VERDADERA! Saltando a línea {destino}")
                print(f"¡CONDICIÓN VERDADERA! Saltando a línea (1 based) {destino + 1}")
                return destino

            elif condicion == "salta_dif" and op1 != op2:
                print(f"¡CONDICIÓN VERDADERA! Saltando a línea {destino}")
                print(f"¡CONDICIÓN VERDADERA! Saltando a línea (1 based) {destino + 1}")
                return destino

            else:
                print("Condición FALSA, siguiente línea")
                return  True
