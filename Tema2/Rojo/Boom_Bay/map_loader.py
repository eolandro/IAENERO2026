def _parsear_linea(linea):
    if " " in linea:
        tokens = [tok for tok in linea.split() if tok]
    else:
        tokens = list(linea)
    return tokens


def cargar_mapa_desde_archivo(ruta, filas_esperadas=5, columnas_esperadas=10):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = [ln.strip() for ln in f.readlines() if ln.strip()]
    except OSError as ex:
        raise ValueError(f"no se pudo abrir '{ruta}': {ex}") from ex

    if len(lineas) != filas_esperadas:
        raise ValueError(
            f"dimensiones invalidas: se esperaban {filas_esperadas} filas y llegaron {len(lineas)}"
        )

    mapa = []
    for i, linea in enumerate(lineas):
        fila = _parsear_linea(linea)
        if len(fila) != columnas_esperadas:
            raise ValueError(
                f"fila {i} invalida: se esperaban {columnas_esperadas} columnas y llegaron {len(fila)}"
            )

        for j, celda in enumerate(fila):
            if celda not in ["0", "*"]:
                raise ValueError(
                    f"valor invalido en ({i},{j}): '{celda}'. Solo se permite '0' o '*'"
                )

        mapa.append(fila)

    return mapa