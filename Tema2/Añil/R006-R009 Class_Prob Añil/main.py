import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from entrenador   import entrenador, detokenizador
from clasificador import clasificador
from evaluador    import evaluador

# ============================== MAIN ==============================#

def main():
    print("=" * 60)
    print("  SISTEMA DE CLASIFICACIÓN PROBABILÍSTICO  (Class_Prob)")
    print("  Detección de Spam — Probabilidad Condicional")
    print("=" * 60)

    entrenador()        # R006 — genera entrenamiento.json
    detokenizador()     # R007 — genera probabilidades.json
    resultados = clasificador()   # R008 — genera resultados.json
    evaluador(resultados)         # R009 — genera evaluacion.json

    print("=" * 60)
    print("  PROCESO COMPLETO FINALIZADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
