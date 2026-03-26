# Agente busca bombas en zigzag usando inferencia bayesiana
# EQUIPO AMARILLO

import yaml
from pathlib import Path
from bayes import calcular_posterior, simular_sensor

RUTA_TABLERO = Path(__file__).parent / "datos" / "tablero.yaml"
UMBRAL = 0.5 # Probabilidad minima para intentar desactivar


def cargar_tablero() -> dict:
    # R010: Carga tablero desde YAML
    with open(RUTA_TABLERO, "r") as f: return yaml.safe_load(f)


def analizar_casilla(real: int, previa: float) -> float:
    # R011: Activa sensor y actualiza probabilidad (Bayes)
    p = previa
    if simular_sensor(real) == 1:
        p = calcular_posterior(p)
        print(f"      Sensor: [+] -> P(bomba) = {p:.4f}")
    else:
        print(f"      Sensor: [-]")
    return p


def buscar(tablero: dict) -> None:
    filas = list(tablero.keys())
    bombas_ok = 0
    total_bombas = sum(sum(tablero[f]) for f in filas)

    print(f"  Buscando {total_bombas} bombas...")
    for i, f in enumerate(filas):
        # Zigzag
        cols = range(len(tablero[f])) if i % 2 == 0 else range(len(tablero[f])-1, -1, -1)
        for c in cols:
            real = tablero[f][c]
            p_final = analizar_casilla(real, 0.1) 

            if p_final >= UMBRAL:
                if real == 1:
                    bombas_ok += 1
                    print(f"  [✓] BOMBA en {f} col {c} desactivada.")
                else:
                    print(f"  [✗] Falsa alarma en {f} col {c}.")

    print(f"\n  Final: {bombas_ok}/{total_bombas} bombas desactivadas.")


def main() -> None:
    print("=" * 60 + "\n  BOOM_BAY - Bayes Agent\n" + "=" * 60)
    buscar(cargar_tablero())


if __name__ == "__main__":
    main()
