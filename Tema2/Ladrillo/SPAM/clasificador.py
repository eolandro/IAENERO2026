import yaml

def clasificador():

    with open("probabilidades.yml", encoding="utf-8") as f:
        tabla = yaml.safe_load(f)

    resultados = []

    while True:

        msg = input("Nuevo mensaje (escribe 'salir' para terminar): ").strip()

        # Condición de salida
        if msg.lower() == "salir":
            print("Finalizando captura de mensajes...")
            break

        if not msg:
            print("Mensaje vacío, intenta de nuevo.")
            continue

        tokens = msg.lower().split()

        votos_spam = 0
        votos_ham = 0

        for t in tokens:

            if t in tabla:

                if tabla[t]["spam"] > tabla[t]["ham"]:
                    votos_spam += 1
                else:
                    votos_ham += 1

        # Decisión
        if votos_spam > votos_ham:
            pred = "spam"
        else:
            pred = "ham"

        print("Clasificación:", pred)

        resultados.append({
            "mensaje": msg,
            "prediccion": pred
        })

    # Guardar resultados solo si hay datos
    if resultados:
        with open("resultados.yml", "w", encoding="utf-8") as f:
            yaml.dump(resultados, f, allow_unicode=True)

        print("Resultados guardados en resultados.yml")
    else:
        print("No se generaron resultados.")