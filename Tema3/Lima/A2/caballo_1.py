from collections import deque

class Caballos3x3:
    def __init__(self):
        self.tamano = 3

        # Estado inicial: posiciones de los 4 caballos
        # (blanco1, blanco2, negro1, negro2)
        self.estadoInicial = (0, 2, 6, 8)

        # Objetivo: los blancos deben terminar en 6 y 8, negros en 0 y 2
        self.objetivoBlancos = {6, 8}
        self.objetivoNegros = {0, 2}

        # Nombres de los caballos (para imprimir)
        self.nombresCaballos = ["B1", "B2", "N1", "N2"]

        # Movimientos posibles del caballo
        movimientosRelativos = [
            (2,1),(2,-1),(-2,1),(-2,-1),
            (1,2),(1,-2),(-1,2),(-1,-2)
        ]

        # Lista donde cada celda guarda a dónde puede moverse
        self.movimientosPorCelda = [[] for _ in range(9)]

        # Precalcular movimientos válidos dentro del tablero
        for celda in range(9):
            fila, col = divmod(celda, 3)

            for df, dc in movimientosRelativos:
                nuevaFila = fila + df
                nuevaCol = col + dc

                # Validar que el movimiento no salga del tablero
                if 0 <= nuevaFila < 3 and 0 <= nuevaCol < 3:
                    destino = nuevaFila * 3 + nuevaCol
                    self.movimientosPorCelda[celda].append(destino)

        # Total de estados posibles: 9^4 (4 caballos, 9 posiciones cada uno)
        self.maxEstados = 9**4

        # Para reconstruir el camino (BFS)
        self.padre = [-1] * self.maxEstados
        self.movimientoHijo = [None] * self.maxEstados

    # Convierte un estado (tupla) a un índice (número)
    def estadoAIndice(self, estado):
        pos1, pos2, pos3, pos4 = estado

        # Conversión en base 9
        return pos1 + pos2*9 + pos3*(9**2) + pos4*(9**3)

    # Convierte un índice de regreso a un estado (tupla)
    def indiceAEstado(self, indice):
        pos4 = indice // (9**3)
        resto = indice % (9**3)

        pos3 = resto // (9**2)
        resto = resto % (9**2)

        pos2 = resto // 9
        pos1 = resto % 9

        return (pos1, pos2, pos3, pos4)

    # Verifica si el estado actual es el objetivo
    def esObjetivo(self, estado):
        blancos = {estado[0], estado[1]}
        negros = {estado[2], estado[3]}

        return blancos == self.objetivoBlancos and negros == self.objetivoNegros

    # Búsqueda en anchura (BFS)
    def buscar(self):
        indiceInicial = self.estadoAIndice(self.estadoInicial)

        cola = deque([indiceInicial])

        # Se marca como visitado apuntando a sí mismo
        self.padre[indiceInicial] = indiceInicial

        while cola:
            indiceActual = cola.popleft()
            estadoActual = self.indiceAEstado(indiceActual)

            # Si llegamos al objetivo, reconstruimos el camino
            if self.esObjetivo(estadoActual):
                return self.reconstruirCamino(indiceInicial, indiceActual)

            posicionesOcupadas = set(estadoActual)

            # Intentar mover cada caballo
            for caballo in range(4):
                origen = estadoActual[caballo]

                for destino in self.movimientosPorCelda[origen]:

                    # No permitir que dos caballos ocupen la misma celda
                    if destino in posicionesOcupadas:
                        continue

                    nuevoEstado = list(estadoActual)
                    nuevoEstado[caballo] = destino

                    nuevoIndice = self.estadoAIndice(tuple(nuevoEstado))

                    if self.padre[nuevoIndice] == -1:
                        self.padre[nuevoIndice] = indiceActual
                        self.movimientoHijo[nuevoIndice] = (caballo, destino)
                        cola.append(nuevoIndice)

        return None

    # Reconstruye el camino desde el objetivo al inicio
    def reconstruirCamino(self, indiceInicial, indiceFinal):
        camino = []
        indiceActual = indiceFinal

        while indiceActual != indiceInicial:
            caballo, destino = self.movimientoHijo[indiceActual]
            indicePadre = self.padre[indiceActual]

            estadoPadre = self.indiceAEstado(indicePadre)
            origen = estadoPadre[caballo]

            camino.append((caballo, origen, destino))

            indiceActual = indicePadre

        camino.reverse()
        return camino


    def imprimirTablero(self, estado, paso=None):
        if paso:
            print(f"--- Paso {paso} ---\n")

        print("     0  1  2")
        print("    " + "--"*6)

        for fila in range(3):
            linea = f"{fila}  |"

            for col in range(3):
                celda = fila*3 + col
                encontrado = False

                for i, pos in enumerate(estado):
                    if pos == celda:
                        linea += f" {self.nombresCaballos[i]}"
                        encontrado = True
                        break

                if not encontrado:
                    linea += "  #"

            print(linea)
        print()

    # Convierte celda a coordenadas (fila, columna)
    def obtenerCoordenada(self, celda):
        return (celda//3, celda%3)


    def ejecutar(self):
        print("")
        print("="*60)
        print("Problema de los 4 caballos")
        print("="*60)

        print("\nEstado inicial:")
        self.imprimirTablero(self.estadoInicial)

        print("Buscando solución ...")

        solucion = self.buscar()

        if not solucion:
            print("\nNo se encontró solución.")
            return

        print(f"\nSolución encontrada en {len(solucion)} movimientos\n")
        print("-"*60)

        estadoActual = list(self.estadoInicial)

        for paso, (caballo, origen, destino) in enumerate(solucion, 1):
            print(f"Movimiento {paso}: {self.nombresCaballos[caballo]} "
                  f"{self.obtenerCoordenada(origen)} → {self.obtenerCoordenada(destino)}\n")

            estadoActual[caballo] = destino
            self.imprimirTablero(tuple(estadoActual), paso)


def main():
    juego = Caballos3x3()
    juego.ejecutar()


if __name__ == "__main__":
    main()