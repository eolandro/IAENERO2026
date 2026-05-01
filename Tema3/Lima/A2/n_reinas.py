class NReinas: 
 
    def __init__(self, n):
        self.n = n
        self.solucionesEncontradas = []
        self.letras = ['a','b','c','d','e','f']
    
    def esValido(self, tablero, fila, columna):
        
        # Se usa abs() para quitar los signos negativos y comparar solo la distancia 
        # entre posiciones. Esto permite detectar diagonales sin importar 
        # la dirección.
        
        for i in range(fila):
            if tablero[i] == columna or abs(tablero[i] - columna) == abs(i - fila):
                return False
        return True
    
    def encontrarPosiciones(self, tablero, fila):
        if fila == self.n:
            self.solucionesEncontradas.append(tablero[:])
            return
        
        for columna in range(self.n):
            if self.esValido(tablero, fila, columna):
                tablero[fila] = columna
                self.encontrarPosiciones(tablero, fila + 1)
                
    def buscarSoluciones(self): 
        tableroInicial = [-1] * self.n
        self.encontrarPosiciones(tableroInicial, 0)
    
    def obtenerPosicionesLetras(self, solucion):
        posiciones = []
        for fila in range(self.n):
            columna = solucion[fila]
            letraColumna = self.letras[columna]
            numeroFila = fila + 1
            posiciones.append(f"{letraColumna}{numeroFila}")
        return posiciones
    
    def mostrarTablero(self, solucion):

        print("    ", end="")
        for c in range(self.n):
            print(f" {self.letras[c]}  ", end="")
        print()
        
        print("    " + "----" * self.n)
        
        for fila in range(self.n):

            print(f"{fila+1:2} ", end="")

            for col in range(self.n):
                if solucion[fila] == col:
                    print("| R ", end="")
                else:
                    print("| # ", end="")
            print("|")

            if fila < self.n - 1:
                print("    " + "----" * self.n)
        
        print("    " + "----" * self.n)
    
    def imprimirSoluciones(self):

        print(f"\n La cantidad de soluciones encontradas fueron: {len(self.solucionesEncontradas)}")
        
        numeroSolucion = 1
        for solucion in self.solucionesEncontradas:
            posiciones = self.obtenerPosicionesLetras(solucion)
            listaPosiciones = ", ".join(posiciones)
            print(f"\n Solución {numeroSolucion}:  Reinas[ {listaPosiciones} ]")
            print("\n Tablero: \n " )
            self.mostrarTablero(solucion)
            print() 
            numeroSolucion += 1


def main():

    print("\n   Bienvenido   ")
    while True:
        try:
            n = int(input("\n Ingrese el número de reinas (entre 4 y 6): "))
            if 4 <= n <= 6:
                break
            else:
                print("\n Error: el número debe estar entre 4 y 6.")
        except ValueError:
            print("\n Error: debe ingresar un número entero.")
    
    problema = NReinas(n)
    problema.buscarSoluciones()
    problema.imprimirSoluciones()


if __name__ == "__main__":
    main()