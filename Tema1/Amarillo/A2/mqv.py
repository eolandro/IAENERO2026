class BoomerVM:

    def __init__(self):
        # Registros de propósito general
        self.R = {"0": 0, "1": 0, "2": 0, "3": 0}

        # Posición actual de Boome en el mapa (fila, columna)
        self.Columnas = 0
        self.Filas = 0

        # Mapa 5 filas x 10 columnas  ('X' = bomba/obstáculo)
        self.Map = [
            ["0", "0", "0", "X", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "X", "0", "0", "0", "0"],
            ["0", "X", "0", "0", "0", "0", "0", "X", "0", "0"],
            ["0", "0", "0", "0", "X", "0", "0", "0", "0", "0"],
            ["0", "0", "X", "0", "0", "0", "0", "0", "0", "0"],
        ]

        self.ultimaInstruccion  = ""
        self.InstruccionActual  = ""
        self.Vivo               = True

    def __str__(self):
        # Registros
        ret  = "Registros\n"
        ret += f"  R0: {self.R['0']}\n"
        ret += f"  R1: {self.R['1']}\n"
        ret += f"  R2: {self.R['2']}\n"
        ret += f"  R3: {self.R['3']}\n"

        # Mapa con Boome marcado como 'B'
        ret += "Mapa:\n"
        mapa_visual = [fila[:] for fila in self.Map]
        mapa_visual[self.Filas][self.Columnas] = "B"
        for i, fila in enumerate(mapa_visual):
            ret += f"  {fila}\n"

        # Estado general
        ret += f"Ultima Instruccion : {self.ultimaInstruccion}\n"
        ret += f"Instruccion Actual : {self.InstruccionActual}\n"
        ret += f"Vivo               : {self.Vivo}\n"
        ret += "-" * 50
        return ret

    def _valor(self, token):
        """Convierte un token (registro o literal hex) a entero."""
        if token in ("r0", "r1", "r2", "r3"):
            return self.R[token[1]]
        # literal hexadecimal tipo 0xFF o 0xFFFF
        return int(token, 16)

    def _celda(self, fila, col):
        """Devuelve el contenido de una celda o None si está fuera del mapa."""
        if 0 <= fila < len(self.Map) and 0 <= col < len(self.Map[fila]):
            return self.Map[fila][col]
        return None

    def _matar(self, motivo=""):
        """Marca a Boome como muerto."""
        self.Vivo = False
        if motivo:
            print(f"  [!] Boome murió: {motivo}")

    def movIzquierda(self):
        nueva_col = self.Columnas - 1
        if nueva_col < 0:
            self._matar("salió del mapa por la izquierda")
            return
        if self._celda(self.Filas, nueva_col) == "X":
            self._matar("chocó con un obstáculo (izquierda)")
            return
        self.Columnas = nueva_col

    def movDerecha(self):
        nueva_col = self.Columnas + 1
        if nueva_col >= len(self.Map[self.Filas]):
            self._matar("salió del mapa por la derecha")
            return
        if self._celda(self.Filas, nueva_col) == "X":
            self._matar("chocó con un obstáculo (derecha)")
            return
        self.Columnas = nueva_col

    def movArriba(self):
        nueva_fila = self.Filas - 1
        if nueva_fila < 0:
            self._matar("salió del mapa por arriba")
            return
        if self._celda(nueva_fila, self.Columnas) == "X":
            self._matar("chocó con un obstáculo (arriba)")
            return
        self.Filas = nueva_fila

    def movAbajo(self):
        nueva_fila = self.Filas + 1
        if nueva_fila >= len(self.Map):
            self._matar("salió del mapa por abajo")
            return
        if self._celda(nueva_fila, self.Columnas) == "X":
            self._matar("chocó con un obstáculo (abajo)")
            return
        self.Filas = nueva_fila

    def sensor(self, direccion):
        match direccion:
            case "ab" | "dw":
                celda = self._celda(self.Filas + 1, self.Columnas)
            case "je" | "up":
                celda = self._celda(self.Filas - 1, self.Columnas)
            case "iz":
                celda = self._celda(self.Filas, self.Columnas - 1)
            case "de":
                celda = self._celda(self.Filas, self.Columnas + 1)
            case _:
                celda = None
        return 1 if celda == "X" else 0

    def fetchDecodeExecute(self, instruccion):
        if not self.Vivo:
            return None

        self.InstruccionActual  = instruccion
        self.ultimaInstruccion  = instruccion

        # Normalizar para tokenizar igual que anlex
        linea = instruccion.strip()
        linea = linea.replace("=", " = ").replace("+", " + ").replace("-", " - ")
        tokens = linea.split()

        match tokens:

            case ["movi"]:
                self.movIzquierda()

            case ["movd"]:
                self.movDerecha()

            case ["mova"]:
                self.movArriba()

            case ["movb"]:
                self.movAbajo()

            case ["negro_desactiva"] | ["deactivate"] | ["desactivar"]:
                self.Vivo = False
                print("  [i] Boome se desactivó voluntariamente.")

            case [reg, "=", val] if reg.startswith("r"):
                self.R[reg[1]] = self._valor(val)

            case [reg, "=", "abelardo", direccion] if reg.startswith("r"):
                self.R[reg[1]] = self.sensor(direccion)

            case [reg, "=", a, op, b] if reg.startswith("r"):
                va = self._valor(a)
                vb = self._valor(b)
                match op:
                    case "+":
                        self.R[reg[1]] = va + vb
                    case "-":
                        self.R[reg[1]] = va - vb


            case [salto, a, b, dest] if salto in ("salta_igual", "salta_dif"):
                va  = self._valor(a)
                vb  = self._valor(b)
                pc  = self._valor(dest)       # destino como número de línea
                condicion = (va == vb) if salto == "salta_igual" else (va != vb)
                if condicion:
                    return pc                 # salto tomado → nueva PC

        return None                           # avance normal


'''
duraznito@drzn:~/IA$ python3
Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
Ctrl click to launch VS Code Native REPL

>>> from mqv import BoomerVM
>>> ovm = BoomerVM()
>>> print(ovm)
R1: 0
R2: 0
R3: 0
['B', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
Ultima Instruccion: 
Instruccion Actual: 
Vivo: True
--------------------------------------------------
>>> ovm.felchDecode("movi")
>>> print(ovm)
R1: 0
R2: 0
R3: 0
['B', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
Ultima Instruccion: movi
Instruccion Actual: movi
Vivo: False
--------------------------------------------------
>>> 
'''