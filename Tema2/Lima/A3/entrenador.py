import json

def leer_mensajes(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            mensajes = [line.strip() for line in archivo.readlines() if line.strip()]
        return mensajes
    except FileNotFoundError:
        print(" Error: No se encontró el archivo mensajes.txt")
        return []


def etiquetar_mensajes(mensajes):
    datos = []

    print("\n--- Comencemos a etiquetar tus mensajes ---")
    print("Instrucciones, selecciona:")
    print("S = Spam")
    print("N = No Spam\n")

    for i, mensaje in enumerate(mensajes):
        while True:
            print(f"\nMensaje {i+1}:")
            print(mensaje)

            etiqueta = input("¿Es Spam? (S/N): ").strip().lower()

            if etiqueta in ["s", "n"]:
                datos.append({
                    "mensaje": mensaje,
                    "tipo": "spam" if etiqueta == "s" else "noSpam"
                })
                break
            else:
                print(" Entrada inválida. Usa solo S o N.")

    return datos


def guardar_json(datos, ruta_salida):
    try:
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print(f"\n Archivo generado correctamente: {ruta_salida}")
    except Exception as e:
        print(f" Error al guardar el archivo: {e}")


def main():
    ruta_entrada = "mensajes.txt"
    ruta_salida = "mensajesEtiquetados.json"

    mensajes = leer_mensajes(ruta_entrada)

    if not mensajes:
        return

    if len(mensajes) != 10:
        print(" Debes tener exactamente 10 mensajes en mensajes.txt")
        return

    datos_etiquetados = etiquetar_mensajes(mensajes)
    guardar_json(datos_etiquetados, ruta_salida)


if __name__ == "__main__":
    main()