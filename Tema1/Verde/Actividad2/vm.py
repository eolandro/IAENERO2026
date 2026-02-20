class BoomeVM:
    def __init__(self):
        self.R={"0":0,"1":0,"2":0,"3":0}
        self.Columna=0
        self.Fila=0

        self.Mapa=[
            ["0"]*10,
            ["0"]*10,
            ["0"]*10,
            ["0"]*10,
            ["0"]*10
        ]

        # bombas ejemplo
        self.Mapa[0][1] = "X"
        self.Mapa[4][9] = "X"

        print(self.Mapa)

        self.ultimaInstruccion=""
        self.InstruccionActual=""
        self.Vivo=True


    def __str__(self):
        Ret=f"\nRegistros:\n"
        Ret+=f"R0 {self.R['0']}\n"
        Ret+=f"R1 {self.R['1']}\n"
        Ret+=f"R2 {self.R['2']}\n"
        Ret+=f"R3 {self.R['3']}\n"

        M=[fila[:] for fila in self.Mapa]
        M[self.Fila][self.Columna]="B"

        for fila in M:
            Ret+=f"{fila}\n"

        Ret+=f"Ultima instrucción: {self.ultimaInstruccion}\n"
        Ret+=f"Instrucción actual: {self.InstruccionActual}\n"
        Ret+=f"Vivo: {self.Vivo}\n"
        Ret+="--------------------------------------"
        return Ret


    
    # BOMBA
    
    def checarBomba(self):
        if self.Mapa[self.Fila][self.Columna]=="X":
            self.Vivo=False
            print(" Boomee explotó!")


    
    # MOVIMIENTOS
    
    def movIzquierda(self):
        self.Columna-=1
        if self.Columna<0:
            self.Columna=0
            self.Vivo=False

    def movDerecha(self):
        self.Columna+=1
        if self.Columna>=len(self.Mapa[0]):
            self.Columna-=1
            self.Vivo=False

    def movArriba(self):
        self.Fila-=1
        if self.Fila<0:
            self.Fila=0
            self.Vivo=False

    def movAbajo(self):
        self.Fila+=1
        if self.Fila>=len(self.Mapa):
            self.Fila-=1
            self.Vivo=False


    
    # SENSORES
    
    def sensIzquierda(self):
        c=self.Columna-1
        if c<0 or self.Mapa[self.Fila][c]!="0":
            self.R["0"]=1
        else:
            self.R["0"]=0

    def sensDerecha(self):
        c=self.Columna+1
        if c>=len(self.Mapa[0]) or self.Mapa[self.Fila][c]!="0":
            self.R["0"]=1
        else:
            self.R["0"]=0

    def sensArriba(self):
        f=self.Fila-1
        if f<0 or self.Mapa[f][self.Columna]!="0":
            self.R["0"]=1
        else:
            self.R["0"]=0

    def sensAbajo(self):
        f=self.Fila+1
        if f>=len(self.Mapa) or self.Mapa[f][self.Columna]!="0":
            self.R["0"]=1
        else:
            self.R["0"]=0

    def salta_igual(self,r,val,dir):
        if self.R[r]==int(val,16):
            return int(dir,16)
        return None

    def salta_dif(self,r,val,dir):
        if self.R[r]!=int(val,16):
            return int(dir,16)
        return None


    
    # EJECUCIÓN
    
    def fetchDecodeExecute(self,Ins):
        if not self.Vivo:
            return

        self.ultimaInstruccion=self.InstruccionActual
        self.InstruccionActual=Ins


        # ---- MOVS ----
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
            return


        # ---- SENSORES ----
        if Ins in ["je","dw","up","ab"]:
            match Ins:
                case "je":
                    self.sensIzquierda()
                case "dw":
                    self.sensDerecha()
                case "up":
                    self.sensArriba()
                case "ab":
                    self.sensAbajo()
            return


        # ---- SALTOS ----
        parts = Ins.split()

        if len(parts)==4:
            if parts[0]=="salta_igual":
                return self.salta_igual(parts[1][1],parts[2],parts[3])

            if parts[0]=="salta_dif":
                return self.salta_dif(parts[1][1],parts[2],parts[3])


