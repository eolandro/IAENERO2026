import random

class BoomeVM:
    def __init__(self):
        # R003: Registros
        self.registros = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
        
        # Generación del Mapa (Representación abstracta)
        self.mapa = [['0' for _ in range(10)] for _ in range(7)]
        for _ in range(15):
            f, c = random.randint(0, 6), random.randint(0, 9)
            if (f, c) != (2, 0): # No bloquear inicio
                self.mapa[f][c] = random.choice(['1', '2'])
        
        self.fila = 2
        self.columna = 0
        self.estado = "Activo"
        self.S = 0 
        self.PC = 0

    def ejecutar(self, instruccion):
        if self.estado != "Activo": return
        
        # R005: Uso de Pattern Matching (Enfoque funcional/lógico)
        match instruccion:
            case ["avanza", direccion]:
                if direccion == "Der": self.columna += 1
                elif direccion == "Izq": self.columna -= 1
                elif direccion == "Arr": self.fila -= 1
                elif direccion == "Abj": self.fila += 1
                self.verificar_colision()

            case ["sensor", direccion]:
                f, c = self.fila, self.columna
                if direccion == "Der": c += 1
                elif direccion == "Izq": c -= 1
                elif direccion == "Arr": f -= 1
                elif direccion == "Abj": f += 1
                
                if 0 <= f < 7 and 0 <= c < 10:
                    self.S = 1 if self.mapa[f][c] in ['1', '2'] else 0
                else: 
                    self.S = 1 # Límite del mapa

            case ["Scero", etiqueta]:
                if self.S == 0:
                    self.PC = int(etiqueta[1:], 16) - 1

            case ["Sncero", etiqueta]:
                if self.S != 0:
                    self.PC = int(etiqueta[1:], 16) - 1

            case [r, "=", val]:
                self.registros[r] = int(val[1:], 16) if val.startswith('H') else self.registros.get(val, 0)

    def verificar_colision(self):
        # R004: Sobrevivir a la ejecución (Manejo de estados)
        if not (0 <= self.fila < 7 and 0 <= self.columna < 10):
            self.estado = "Morido"
            print("!!! FUERA DE RANGO !!!")
            return

        celda = self.mapa[self.fila][self.columna]
        
        if celda == '1': # BOMBA (Extra: Desactivación)
            print(f"-- BOMBA DESACTIVADA en [{self.fila},{self.columna}] --")
            self.mapa[self.fila][self.columna] = '0'
            self.registros["R3"] += 1 # R3 llevará la cuenta de bombas desactivadas
            
        elif celda == '2': # MURO (Obstáculo infranqueable)
            self.mapa[self.fila][self.columna] = 'X'
            self.estado = "Morido"
            print("!!! CHOQUE CON MURO !!!")

        if self.columna >= 9:
            self.estado = "Ganador"

    def __str__(self):
        # R003: Representación adecuada en consola
        res = f"\n{'='*30}\n"
        res += f" PC: {self.PC:02} | S: {self.S} | Estado: {self.estado}\n"
        res += f" REGISTROS: {self.registros}\n"
        res += f"{'-'*30}\n"
        
        copia = [f[:] for f in self.mapa]
        if self.estado == "Activo": copia[self.fila][self.columna] = 'R'
        
        for f in copia:
            res += "  " + " ".join(f) + "\n"
        res += f"{'='*30}"
        return res