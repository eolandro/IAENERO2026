#Forma de llamar a la maquina virtual:
"""
python3
from vm import BoomeVM
ovm = BoomeVM()
print (ovm)
ovm.fetchDecodeExecute("movi")
print (ovm)

"""
import random


class BoomeVM:
    #Tipos de constructores: por defecto(no tiene argumentos), el completo(tiene argumentos), constructor copia.
    def __init__(self):
        #Tenemos 4 registros
        #Auto destrciptivo el diccionario
        self.R={"0":0,"1":0,"2":0,"3":0}
        #self.R[0]==>r0
        #Se maneja como columna-fila separadas
        self.Columna=0;
        self.Fila=0;
        
        #self.Mapa = [
        #    ["0"]*10,
        #    ["0"]*10,
        #    ["0"]*10,
        #    ["0"]*10,
        #    ["0"]*10,
        #]
        self.Mapa = [['0' for _ in range(10)] for _ in range(5)];
        num_bombas = random.randint(1, 5);
        num_obstaculos = random.randint(1, 5);
        
        self.colocar_elementos('1', num_bombas);
        self.colocar_elementos('|', num_obstaculos);
        self.ultimaInstruccion = ""
        self.Vivo = True
        self.InstruccionActual = ""

    def colocar_elementos(self,simbolo, cantidad):
            colocados = 0
            while colocados < cantidad:
                f_rand = random.randint(0, len(self.Mapa) - 1);#Fila
                c_rand = random.randint(0, len(self.Mapa[0]) - 1);#Columna
                
                # Condición: Que no sea el origen (0,0) Y que la celda esté vacía ('0')
                if (f_rand, c_rand) != (0, 0) and self.Mapa[f_rand][c_rand] == '0':
                    self.Mapa[f_rand][c_rand] = simbolo
                    colocados += 1

        #poner el objeto como cadena
    def __str__(self):
        Ret=f"Registros \nR0 {self.R['0']}\n";
        Ret+=f"R1 {self.R['1']}\n";
        Ret+=f"R2 {self.R['2']}\n";
        Ret+=f"R3 {self.R['3']}\n";
        #Se debe copiar todo cada posicion de manera manual por ello se ocupa compresión de listas.
        Mapa=[fila[:] for fila in self.Mapa];
        Mapa[self.Fila][self.Columna]="B";
        for fila in Mapa:
            Ret+=f'{fila}\n';
        Ret+=f'Ultima Instrucción : {self.ultimaInstruccion}\n';
        Ret+=f'Instrucción Actual : {self.InstruccionActual}\n';
        Ret+= f'Vivo: {self.Vivo}\n';
        Ret+= f'-------------------------------------------------------------\n';
        return Ret;
#EL hecho de tomar una instrucción, es decir que la linea se ejecute. Se hace en la memoria baja de la RAM -> Fetch
#Decodificar -> decode
#FInalmente se ejecuta la linea -> execute

#******************Exepciones*************************+
    def muro(self):
        if self.Mapa[self.Fila][self.Columna] == '|':
            self.Vivo=False;
            print("Te estrellaste contra un muro, perdiste");
            return True;

    def bomba(self):
        if self.Mapa[self.Fila][self.Columna] == '1':
            self.Vivo = False;
            print("¡KA-BOOM!");
            return True;
        return False;
    
    def desactivar_bomba(self):
        if self.Mapa[self.Fila][self.Columna] == '1':
            self.Mapa[self.Fila][self.Columna] = '0';
            print("¡Bomba desactivada correctamente!");
        else:
            print("No le sabe raza, no hay bomba en esta celda.");

#******************MOVIMIENTOS*************************
    def movIzquierda(self):
        #Bomba
        if self.bomba():
            return
        #Verificar si se puede mover
        #Primero lo vamos a estrellar
        self.Columna-=1;
        if self.Columna <0:
            print("Saliste del mapa, perdiste");
            self.Vivo=False;
            self.Columna+=1;
            return
        if self.muro():
            self.Columna+=1;

    def movDerecha(self):
        if self.bomba():
            return
        self.Columna+=1;
        #if self.Columna >=self.Mapa[self.Fila]:
        if self.Columna >= len(self.Mapa[self.Fila]):
            print("Saliste del mapa, perdiste");
            self.Vivo=False;
            self.Columna-=1;
            return
        if self.muro():
            self.Columna-=1;
    
    def movArriba(self):
        if self.bomba():
            return
        self.Fila-=1;
        if self.Fila <0:
            print("Saliste del mapa, perdiste");
            self.Vivo=False;
            self.Fila+=1;
            return
        if self.muro():
            self.Fila+=1;

    def movIAbajo(self):
        if self.bomba():
            return
        self.Fila+=1;
        if self.Fila >=len(self.Mapa):
            print("Saliste del mapa, perdiste");
            self.Vivo=False;
            self.Fila-=1;
            return
        if self.muro():
            self.Fila-=1;

#Lo que se hace es convertir un operando a un numero entero, ya sea porque es un numero hexadecimal o porque es un registro, en este caso se busca el valor del registro.
    def _obtener_valor(self, operando):
        if operando.startswith("0x"):
            return int(operando, 16) # Convierte hex a decimal
        elif operando in ['r0', 'r1', 'r2', 'r3']:
            # Extrae el número del registro ("r0" -> "0") y busca su valor
            num_reg = operando.replace("r", "")
            return self.R[num_reg]
        return 0

    def fetchDecodeExecute(self, Instruccion):
        #Va confiar en que todo esta bien, sino es culpa del anlex.
        if not self.Vivo:
            return
        self.ultimaInstruccion = self.InstruccionActual
        self.InstruccionActual = Instruccion
        #Separar la instrucción
        LStr = Instruccion.strip().split(" ")
        LStr = [s for s in LStr if s]  # Eliminar elementos vacíos con una compresión de listas
        if not LStr:
            return
        match LStr:
            #Movimiento 
            case [mov] if mov in ['movi', 'movd', 'mova', 'movb']:
                print(f"Movimiento: {mov}")
                if mov == 'movi': self.movIzquierda()
                elif mov == 'movd': self.movDerecha()
                elif mov == 'mova': self.movArriba()
                elif mov == 'movb': self.movIAbajo()
            #Bomba
            case ["deactivate"]:
                self.desactivar_bomba()
            #Asignación simple (Ej: r0 = 0x1 o r1 = r0)
            case [dest, "=", src]:
                print(f"Asignación simple: {dest} = {src}")
                valor = self._obtener_valor(src)
                num_reg = dest.replace("r", "")
                self.R[num_reg] = valor
            #El abelardo
            case [dest, "=", "abelardo", direccion]:
                print(f"Abelardo: {dest} = abelardo {direccion}")
                #Leer el valor de la celda actual
                valor_celda = int(self.Mapa[self.Fila][self.Columna])
                num_reg = dest.replace("r", "")
                self.R[num_reg] = valor_celda
            #Operadores (Ej: r0 = r1 + 0x02) 
            case [dest, "=", op1, signo, op2]:
                val1 = self._obtener_valor(op1)
                val2 = self._obtener_valor(op2)
                if signo == "+":
                    res = val1 + val2
                elif signo == "-":
                    res = val1 - val2
                else:
                    res = 0
                print(f"Operación: {dest} = {op1} {signo} {op2} -> {res}")
                num_reg = dest.replace("r", "")
                self.R[num_reg] = res
            # Gramática: salta_igual op1 op2 destino
            # Ejemplo: salta_igual r0 0x5 0x0 (Si r0 vale 5, vete a la línea 0)
            case [tipo_salto, op1, op2, dest] if tipo_salto in ["salta_igual", "salta_dif"]:
                val1 = self._obtener_valor(op1)
                val2 = self._obtener_valor(op2)
                linea_destino = self._obtener_valor(dest)
                
                hacer_salto = False
                
                if tipo_salto == "salta_igual" and val1 == val2:
                    hacer_salto = True
                elif tipo_salto == "salta_dif" and val1 != val2:
                    hacer_salto = True
                
                if hacer_salto:
                    print(f"¡SALTO! {tipo_salto}: {val1} vs {val2} -> Ir a linea {linea_destino}")
                    return linea_destino # <--- Retornamos el destino
                else:
                    print(f"No salto: {tipo_salto}: {val1} vs {val2}")
                    return None # <--- No hubo salto, seguimos normal

#Toma la instruccón y de una vez checar que se debe de hacer.
#Primera versión:
"""
    def fetchDecodeExecute(self,Instruccion):
        #Va confiar en que todo esta bien, sino es culpa del anlex.
        if not self.Vivo:
            return
        #Movimiento
        if Instruccion in ['movi','movd','mova','movb']:
            self.ultimaInstruccion=self.InstruccionActual;
            self.InstruccionActual=Instruccion;
            match [Instruccion]:
                case ['movi']:
                    self.movIzquierda();
                    return
                case ['movd']:
                    self.movDerecha();
                    return
                case ['mova']:
                    self.movArriba();
                    return
                case ['movb']:
                    self.movIAbajo();
                    return
"""


#Corrida de ejemplo
"""
r0 = 0x01 -> El r0 es la dirección de memoria, es decir, el valor que se le asigna a r0 es 1 en hexadecimal, lo cual es 1 en decimal.
r1 = 0x02 -> El r1 es la dirección de memoria, es decir, el valor que se le asigna a r1 es 2 en hexadecimal, lo cual es 2 en decimal.
r2 = r0 + r1 -> El r2 es la dirección de memoria, es decir, el valor que se le asigna a r2 es la suma de r0 y r1, lo cual es 3 en decimal.
movd -> El robot se mueve a la derecha, ahora está en la columna 1.
movd -> El robot se mueve a la derecha, ahora está en la columna 2.
r3 = abelardo je -> El r3 es la dirección de memoria, es decir, el valor que se le asigna a r3 es lo que "Abelardo" lee en la celda actual. Dado que el robot está en la fila 0 y columna 2, y el mapa tiene "0" en esa posición, r3 se asigna el valor 0.
movd -> El robot se mueve a la derecha, ahora está en la columna 3.
r0 = 0xFF -> El r0 es la dirección de memoria, es decir, el valor que se le asigna a r0 es 255 en hexadecimal, lo cual es 255 en decimal.
"""
#Bucle infinito de salto:
#r0 = 0x0001
#movd
#movi
#salta_igual r0 0x01 0x00
