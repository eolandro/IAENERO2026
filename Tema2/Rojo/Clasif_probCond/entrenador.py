import json

archivo_yaml = "mensajes.yaml"
archivo_salida = "conocimiento_entrenamiento.json"

registros = []


def leer_lista_yaml(ruta, clave):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"No existe {ruta}.")
        raise SystemExit(1)

    lista = []
    en_seccion = False

    for linea in lineas:
        txt = linea.strip()

        if not txt or txt.startswith("#"):
            continue

        if txt == f"{clave}:":
            en_seccion = True
            continue

        if en_seccion and txt.endswith(":") and not txt.startswith("-"):
            break

        if en_seccion and txt.startswith("-"):
            item = txt[1:].strip()
            if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            if item:
                lista.append(item)

    return lista


print("ENTRENADOR")
print("Clasifica 10 mensajes (s/n).")

mensajes = leer_lista_yaml(archivo_yaml, "mensajes_entrenamiento")
if len(mensajes) != 10:
    print(f"Se esperaban 10 mensajes_entrenamiento en {archivo_yaml} y hay {len(mensajes)}.")
    raise SystemExit(1)

for i, mensaje in enumerate(mensajes, start=1):
    print(f"\nMensaje {i}: {mensaje}")

    while True:
        etiqueta = input("Etiqueta (s/n): ").strip().lower()
        if etiqueta in ("s", "n"):
            break
        print("Etiqueta inválida. Usa solo s o n.")

    registros.append({"mensaje": mensaje, "etiqueta": etiqueta})

with open(archivo_salida, "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=2)

print(f"Archivo generado: {archivo_salida}")
