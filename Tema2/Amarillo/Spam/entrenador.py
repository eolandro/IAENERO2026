# entrenador
# El supervisor etiqueta mensajes como spam o no_spam

import yaml
from pathlib import Path

DIR_DATOS = Path(__file__).parent / "datos"
RUTA_ENTRADA = DIR_DATOS / "mensajes_entrada.yaml"
RUTA_SALIDA = DIR_DATOS / "mensajes_etiquetados.yaml"


def cargar_mensajes(ruta: Path) -> list:
    with open(ruta, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["mensajes"]


def etiquetar_mensajes(mensajes: list) -> list:
    etiquetados = []
    print("=" * 60 + "\n  ENTRENADOR - Etiquetado\n" + "=" * 60)

    for msg in mensajes:
        print(f"  --- Mensaje {msg['id']} ---\n  \"{msg['texto']}\"")
        while True:
            resp = input("  ¿Es spam? (s/n): ").strip().lower()
            if resp in ("s", "n"): break
            print("  Responde 's' o 'n'.")

        etiqueta = "spam" if resp == "s" else "no_spam"
        etiquetados.append({
            "id": msg["id"],
            "texto": msg["texto"],
            "etiqueta": etiqueta,
        })
    return etiquetados


def main() -> None:
    if not RUTA_ENTRADA.exists(): return
    etiquetados = etiquetar_mensajes(cargar_mensajes(RUTA_ENTRADA))
    
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        yaml.dump({"mensajes_etiquetados": etiquetados}, f, allow_unicode=True, sort_keys=False)
    print(f"  Archivo generado: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
