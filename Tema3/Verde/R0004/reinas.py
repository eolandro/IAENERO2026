import yaml

def resolver_n_reinas(N):
    soluciones = []

    columnas = set()
    diag1 = set()  # fila - columna
    diag2 = set()  # fila + columna

    tablero = [-1] * N  # índice = fila, valor = columna

    def backtrack(fila):
        if fila == N:
            soluciones.append(tablero[:])
            return

        for col in range(N):
            if col in columnas or (fila - col) in diag1 or (fila + col) in diag2:
                continue

            # colocar reina
            tablero[fila] = col
            columnas.add(col)
            diag1.add(fila - col)
            diag2.add(fila + col)

            backtrack(fila + 1)

            # quitar reina (backtracking)
            columnas.remove(col)
            diag1.remove(fila - col)
            diag2.remove(fila + col)

    backtrack(0)
    return soluciones


def convertir_a_matriz(solucion, N):
    matriz = []
    for fila in range(N):
        renglon = [0] * N
        renglon[solucion[fila]] = 1
        matriz.append(renglon)
    return matriz


def generar_yaml(soluciones, N):
    yaml_data = []

    for i, sol in enumerate(soluciones, start=1):
        matriz = convertir_a_matriz(sol, N)

        tablero_texto = [" ".join(map(str, fila)) for fila in matriz]

        yaml_data.append({
            "solucion": i,
            "tablero": tablero_texto
        })

    return yaml_data


def main():
    N = 4
    soluciones = resolver_n_reinas(N)

    yaml_data = generar_yaml(soluciones, N)

    with open("soluciones_4_reinas.yaml", "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False, allow_unicode=True)

    print(f"Se encontraron {len(soluciones)} soluciones.")


if __name__ == "__main__":
    main()