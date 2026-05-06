from collections import deque

TAMANO = 6
NOMBRES = ["B1", "B2", "N1", "N2"]
MOVS = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]


def a_indice(fila, col):
    return fila * TAMANO + col


def a_coord(indice):
    return divmod(indice, TAMANO)


def movimientos(pos):
    fila, col = a_coord(pos)
    res = []
    for df, dc in MOVS:
        nf, nc = fila + df, col + dc
        if 0 <= nf < TAMANO and 0 <= nc < TAMANO:
            res.append(a_indice(nf, nc))
    return res


def bfs(estado_inicial, estado_meta):
    cola = deque([estado_inicial])
    padre = {estado_inicial: None}
    mov = {estado_inicial: None}

    while cola:
        actual = cola.popleft()
        if actual == estado_meta:
            return reconstruir(padre, mov, estado_inicial, estado_meta)

        ocupadas = set(actual)
        for i in range(4):
            origen = actual[i]
            for destino in movimientos(origen):
                if destino in ocupadas:
                    continue
                nuevo = list(actual)
                nuevo[i] = destino
                nuevo = tuple(nuevo)
                if nuevo not in padre:
                    padre[nuevo] = actual
                    mov[nuevo] = (i, origen, destino)
                    cola.append(nuevo)

    return None


def reconstruir(padre, mov, ini, fin):
    pasos = []
    actual = fin
    while actual != ini:
        pasos.append(mov[actual])
        actual = padre[actual]
    pasos.reverse()
    return pasos


def imprimir_tablero(estado, paso=None):
    if paso is not None:
        print("Paso", paso)

    encabezado = "   " + " ".join(str(i) for i in range(TAMANO))
    print(encabezado)
    for f in range(TAMANO):
        linea = ["%2d" % f]
        for c in range(TAMANO):
            idx = a_indice(f, c)
            if idx in estado:
                quien = estado.index(idx)
                linea.append(NOMBRES[quien])
            else:
                linea.append("--")
        print(" ".join(linea))
    print()


def main():
    estado_inicial = (
        a_indice(0, 0),
        a_indice(0, 5),
        a_indice(5, 0),
        a_indice(5, 5),
    )

    estado_meta = (
        a_indice(5, 0),
        a_indice(5, 5),
        a_indice(0, 0),
        a_indice(0, 5),
    )

    print("Intercambio de 4 caballos (6x6)")
    print("Objetivo: B1/B2 <-> N1/N2")
    print("inicio:")
    imprimir_tablero(list(estado_inicial))

    solucion = bfs(estado_inicial, estado_meta)

    if not solucion:
        print("No hay solucion.")
        return

    print("total movs:", len(solucion))
    estado = list(estado_inicial)
    for i, (caballo, origen, destino) in enumerate(solucion, 1):
        estado[caballo] = destino
        print("%d) %s: %s -> %s" % (i, NOMBRES[caballo], a_coord(origen), a_coord(destino)))
        imprimir_tablero(estado, i)


if __name__ == "__main__":
    main()