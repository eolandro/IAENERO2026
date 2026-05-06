class NReinas:
    def __init__(self, n):
        self.n = n
        self.soluciones = []
        self.letras = ["a", "b", "c", "d"]

    def es_valido(self, tablero, fila, col):
        for i in range(fila):
            if tablero[i] == col:
                return False
            if abs(tablero[i] - col) == abs(i - fila):
                return False
        return True

    def buscar(self, tablero, fila):
        if fila == self.n:
            self.soluciones.append(tablero[:])
            return
        for col in range(self.n):
            if self.es_valido(tablero, fila, col):
                tablero[fila] = col
                self.buscar(tablero, fila + 1)

    def resolver(self):
        tablero = [-1] * self.n
        self.buscar(tablero, 0)

    def mostrar_tablero(self, solucion):
        print("   " + " | ".join(self.letras))
        print("  " + "-" * (self.n * 4))
        for fila in range(self.n):
            linea = [str(fila + 1)]
            for col in range(self.n):
                linea.append("Q" if solucion[fila] == col else "-")
            print(" | ".join(linea))

    def imprimir(self):
        print("Total soluciones:", len(self.soluciones))
        for i, sol in enumerate(self.soluciones, 1):
            posiciones = []
            for fila in range(self.n):
                posiciones.append(self.letras[sol[fila]] + str(fila + 1))
            print("\nSolucion #", i, ":", ", ".join(posiciones))
            self.mostrar_tablero(sol)


def main():
    n = 4
    print("Problema de las", n, "reinas")
    r = NReinas(n)
    r.resolver()
    r.imprimir()


if __name__ == "__main__":
    main()