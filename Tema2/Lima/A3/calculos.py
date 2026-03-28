import json

def cargarResultados():
    try:
        with open("resultadosClasificacion.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)  
            
    except FileNotFoundError:
        print("Error: No se encontró resultadosClasificacion.json")
        return None  

def pedirEtiqueta():

    respuesta = input("Clasificación real (S/N): ").strip().lower()  

    if respuesta in ["s", "n"]:
        return "spam" if respuesta == "s" else "noSpam"  
    else:
        print("Entrada inválida, intenta de nuevo.")
        return pedirEtiqueta()  


def clasificacionReal(listaResultados):

    etiquetasReales = []  
    # aquí guardaremos las clasificaciones reales dadas por el usuario

    print("\n--- Comencemos a etiquetar tus mensajes ---")
    print("S = spam | N = no_spam\n")

    for indice, registro in enumerate(listaResultados):
        mensaje = registro["mensaje"]  

        print(f"\nMensaje {indice+1}:")
        print(mensaje)

        etiqueta = pedirEtiqueta()  
        etiquetasReales.append(etiqueta)  

    return etiquetasReales  

def calcularMatriz(predicciones, reales):

    verdaderosPositivos = 0  
    verdaderosNegativos = 0  
    falsosPositivos = 0  
    falsosNegativos = 0  

    for prediccion, realidad in zip(predicciones, reales):  

        if prediccion == "spam" and realidad == "spam":
            verdaderosPositivos += 1  

        if prediccion == "noSpam" and realidad == "noSpam":
            verdaderosNegativos += 1  

        if prediccion == "spam" and realidad == "noSpam":
            falsosPositivos += 1  

        if prediccion == "noSpam" and realidad == "spam":
            falsosNegativos += 1  

    return verdaderosPositivos, verdaderosNegativos, falsosPositivos, falsosNegativos  


def calcularMetricas(VP, VN, FP, FN):

    total = VP + VN + FP + FN  
    # qué tan correcto es el modelo en general
    accuracy = (VP + VN) / total if total > 0 else 0  
    # de los que dijo spam, cuántos realmente lo eran
    precision = VP / (VP + FP) if (VP + FP) > 0 else 0  
    # cuántos spam reales detectó el modelo
    recall = VP / (VP + FN) if (VP + FN) > 0 else 0  

    prevalence = (VP + FN) / total if total > 0 else 0  

    return accuracy, precision, recall, prevalence  


def calcularConsensos(listaPredicciones):

    valores = [1 if valor == "spam" else 0 for valor in listaPredicciones]  
    # convertimos spam=1 y noSpam=0 para poder aplicar cálculos

    mediaValor = sum(valores) / len(valores)  
    # -------- Mediana --------
    valoresOrdenados = sorted(valores)  
    mitad = len(valoresOrdenados) // 2  
    medianaValor = valoresOrdenados[mitad]  

    contador = {}  

    for numero in valores:
        if numero not in contador:
            contador[numero] = 0  
        contador[numero] += 1  

    modaValor = max(contador, key=contador.get)  
    totalSpam = valores.count(1)  
    totalNoSpam = valores.count(0)  

    if totalSpam > totalNoSpam:
        decisionFinal = "spam"
    elif totalNoSpam > totalSpam:
        decisionFinal = "noSpam"
    else:
        decisionFinal = "empate"  

    return mediaValor, medianaValor, modaValor, decisionFinal  


def mostrarResultados(VP, VN, FP, FN, accuracy, precision, recall, prevalence, consensos):

    print("\n /*/*/*/ MATRIZ DE CONFUSIÓN /*/*/*/")
    print(f"VP (Verdaderos Positivos): {VP}")
    print(f"VN (Verdaderos Negativos): {VN}")
    print(f"FP (Falsos Positivos): {FP}")
    print(f"FN (Falsos Negativos): {FN}")

    print("\n/*/*/*/ MÉTRICAS /*/*/*/")
    print(f"Accuracy:   {accuracy:.2f}")
    print(f"Precision:  {precision:.2f}")
    print(f"Recall:     {recall:.2f}")
    print(f"Prevalence: {prevalence:.2f}")

    print("\n/*/*/*/ CONSENSOS /*/*/*/")
    print(f"Media:      {consensos[0]:.2f}")
    print(f"Mediana:    {consensos[1]}")
    print(f"Moda:       {consensos[2]}")


def main():

    resultados = cargarResultados()  
    # cargamos las predicciones del clasificador

    if resultados is None:
        return  
        # si no hay archivo, terminamos

    listaPredicciones = [registro["clasificacion"] for registro in resultados]  
    # extraemos únicamente las clasificaciones del JSON

    listaReales = clasificacionReal(resultados)  

    VP, VN, FP, FN = calcularMatriz(listaPredicciones, listaReales)  
    # calculamos la matriz de confusión

    accuracy, precision, recall, prevalence = calcularMetricas(VP, VN, FP, FN)  
    # calculamos métricas de rendimiento

    consensos = calcularConsensos(listaPredicciones)  
    # calculamos media, mediana, moda y democracia

    mostrarResultados(VP, VN, FP, FN, accuracy, precision, recall, prevalence, consensos)  


if __name__ == "__main__":
    main()