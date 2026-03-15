import os
import sys
import json
import yaml
import math

# ============================================================
#                       INICIALIZADOR
# ============================================================

def cargar_config(archivo="config.yaml"):
    ruta = os.path.join(os.path.dirname(__file__), archivo)
    f = open(ruta, "r", encoding="utf-8")
    datos = yaml.safe_load(f)
    f.close()
    return datos

def calcular_puntaje(animal_vals, config):
    total = 0
    for carac, info in config["caracteristicas"].items():
        total += animal_vals.get(carac, 0) * info["peso"]
    return total

def construir_animales(config):
    lista = []
    for nombre, vals in config["animales"].items():
        pts = calcular_puntaje(vals, config)
        lista.append({
            "nombre": nombre,
            "caracteristicas": vals,
            "puntaje": pts
        })
    return lista

def imprimir_tabla(config, animales):
    cols = list(config["caracteristicas"].keys())
    linea = f"{'Animal':<12}" + "".join(f"{c[:4]:>6}" for c in cols) + f"{'Pts':>6}"
    print(linea)
    print("-" * len(linea))
    for a in animales:
        fila = f"{a['nombre']:<12}"
        fila += "".join(f"{a['caracteristicas'].get(c, 0):>6}" for c in cols)
        fila += f"{a['puntaje']:>6}"
        print(fila)

def guardar_animales_json(config, animales):
    pesos = {c: info["peso"] for c, info in config["caracteristicas"].items()}
    preguntas = {c: info["pregunta"] for c, info in config["caracteristicas"].items()}
    salida = {
        "caracteristicas": list(config["caracteristicas"].keys()),
        "pesos": pesos,
        "preguntas": preguntas,
        "animales": animales
    }
    ruta = os.path.join(os.path.dirname(__file__), "animales.json")
    f = open(ruta, "w", encoding="utf-8")
    json.dump(salida, f, ensure_ascii=False, indent=2)
    f.close()

def detectar_perfiles_identicos(animales):
    """Busca animales que tengan exactamente el mismo perfil de caracteristicas."""
    grupos = {}
    for a in animales:
        # convierto el dict a tupla para usarlo como clave
        clave = tuple(sorted(a["caracteristicas"].items()))
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(a["nombre"])
    
    # regresa solo los grupos con mas de un animal
    conflictos = [nombres for nombres in grupos.values() if len(nombres) > 1]
    return conflictos

def inicializador():
    print("=" * 50)
    print("  ETAPA 1: INICIALIZADOR")
    print("=" * 50)
    config = cargar_config()
    animales = construir_animales(config)
    imprimir_tabla(config, animales)

    # revisar si hay animales con perfil identico
    conflictos = detectar_perfiles_identicos(animales)
    if conflictos:
        print("\n[ADVERTENCIA] Estos animales tienen el mismo perfil y no se podran distinguir:")
        for grupo in conflictos:
            print(f"  -> {grupo}")
        print("  Considera agregar una caracteristica que los diferencie en config.yaml\n")
    else:
        print("\n[OK] Todos los animales tienen un perfil unico\n")

    guardar_animales_json(config, animales)
    print(f"Total animales: {len(animales)}")
    return config

# ============================================================
#                       ENTRENADOR
# ============================================================

def cargar_animales_json():
    ruta = os.path.join(os.path.dirname(__file__), "animales.json")
    f = open(ruta, "r", encoding="utf-8")
    datos = json.load(f)
    f.close()
    return datos

def entropia(p):
    # H(p) = -p*log2(p) - (1-p)*log2(1-p)
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def analizar(datos):
    animales = datos["animales"]
    caracteristicas = datos["caracteristicas"]
    preguntas = datos["preguntas"]
    total = len(animales)
    resultados = []
    for carac in caracteristicas:
        si = sum(1 for a in animales if a["caracteristicas"][carac] == 1)
        no = total - si
        p = si / total
        h = entropia(p)
        resultados.append({
            "caracteristica": carac,
            "pregunta": preguntas[carac],
            "si": si,
            "no": no,
            "p": round(p, 4),
            "entropia": round(h, 6)
        })
    return resultados

def ordenar_burbuja(resultados):
    n = len(resultados)
    for i in range(n):
        for j in range(0, n - i - 1):
            if resultados[j]["entropia"] < resultados[j+1]["entropia"]:
                temp = resultados[j]
                resultados[j] = resultados[j+1]
                resultados[j+1] = temp
    return resultados

def guardar_preguntas_json(ordenados, pesos):
    ruta = os.path.join(os.path.dirname(__file__), "preguntas_ordenadas.json")
    salida = {
        "orden_preguntas": [r["caracteristica"] for r in ordenados],
        "detalle": ordenados,
        "pesos": pesos
    }
    f = open(ruta, "w", encoding="utf-8")
    json.dump(salida, f, ensure_ascii=False, indent=2)
    f.close()

def entrenador():
    print("\n" + "=" * 50)
    print("  ETAPA 2: ENTRENADOR")
    print("=" * 50)
    datos = cargar_animales_json()
    print(f"Animales cargados: {len(datos['animales'])}")
    resultados = analizar(datos)
    ordenados = ordenar_burbuja(resultados)

    print(f"\n{'#':<4} {'Caracteristica':<12} {'Pregunta':<35} {'Si':>4} {'No':>4} {'Entropia':>10}")
    print("-" * 75)
    for i, r in enumerate(ordenados, 1):
        print(f"{i:<4} {r['caracteristica']:<12} {r['pregunta']:<35} {r['si']:>4} {r['no']:>4} {r['entropia']:>10.6f}")

    guardar_preguntas_json(ordenados, datos["pesos"])
    print("\n[OK] Orden optimo calculado")

# ============================================================
#                       ADIVINAR
# ============================================================

def cargar_todo():
    carpeta = os.path.dirname(__file__)
    f1 = open(os.path.join(carpeta, "animales.json"), "r", encoding="utf-8")
    animales = json.load(f1)
    f1.close()
    f2 = open(os.path.join(carpeta, "preguntas_ordenadas.json"), "r", encoding="utf-8")
    preguntas = json.load(f2)
    f2.close()
    return animales, preguntas

def hacer_pregunta(texto):
    while True:
        resp = input(f"  {texto} (s/n): ").strip().lower()
        if resp in ("s", "si", "sí"):
            return 1
        elif resp in ("n", "no"):
            return 0
        else:
            print("  Responde s o n")

def filtrar(candidatos, carac, respuesta):
    return [a for a in candidatos if a["caracteristicas"][carac] == respuesta]

def calcular_confianza(candidatos):
    """
    Calcula la confianza actual.
    Si hay 1 candidato = 100%, si hay 2 = 50%, etc.
    Regresa el porcentaje del candidato mas probable (todos tienen igual peso por ahora).
    """
    if len(candidatos) == 0:
        return 0, None
    confianza = 1 / len(candidatos)
    return confianza, candidatos[0]

def mejor_pregunta(candidatos, disponibles, detalle):
    """Elige la pregunta con mayor entropia sobre los candidatos actuales."""
    mejor_carac = None
    mejor_h = -1
    total = len(candidatos)
    for carac in disponibles:
        si = sum(1 for a in candidatos if a["caracteristicas"][carac] == 1)
        no = total - si
        if si == 0 or no == 0:
            continue  # pregunta que no divide, la saltamos
        p = si / total
        h = -p * math.log2(p) - (1-p) * math.log2(1-p)
        if h > mejor_h:
            mejor_h = h
            mejor_carac = carac
    return mejor_carac

def jugar(datos_animales, datos_preguntas):
    candidatos = list(datos_animales["animales"])
    detalle = {r["caracteristica"]: r["pregunta"] for r in datos_preguntas["detalle"]}
    disponibles = list(datos_preguntas["orden_preguntas"])
    max_preguntas = len(disponibles)
    num_preguntas = 0
    UMBRAL = 0.90

    print("\nPiensa en un animal... responde mis preguntas\n")

    while len(disponibles) > 0:
        if len(candidatos) == 0:
            print("Algo salio mal, no quedan candidatos")
            return

        confianza, mejor = calcular_confianza(candidatos)
        print(f"  [Confianza actual: {confianza*100:.1f}% | Candidatos: {len(candidatos)}]")

        if confianza >= UMBRAL:
            break

        # elegir la mejor pregunta para los candidatos que quedan ahora
        carac = mejor_pregunta(candidatos, disponibles, detalle)

        if carac is None:
            break  # ninguna pregunta divide mas al grupo

        disponibles.remove(carac)

        print(f"Pregunta {num_preguntas + 1}:")
        resp = hacer_pregunta(detalle[carac])
        num_preguntas += 1

        candidatos = filtrar(candidatos, carac, resp)

        if len(candidatos) == 0:
            print("  Respuesta inconsistente, no quedan candidatos")
            return

        nombres = [a["nombre"] for a in candidatos]
        print(f"  -> Candidatos: {nombres}\n")

    # confianza final
    confianza, mejor = calcular_confianza(candidatos)

    print("=" * 40)
    if confianza >= UMBRAL:
        print(f"  El animal es: {mejor['nombre'].upper()}")
        print(f"  Confianza: {confianza*100:.1f}%")
        print(f"  Preguntas usadas: {num_preguntas} de {max_preguntas} posibles")
        ahorro = max_preguntas - num_preguntas
        if ahorro > 0:
            print(f"  Preguntas ahorradas: {ahorro}")
    else:
        nombres = [a["nombre"] for a in candidatos]
        print(f"  No alcance el 90% de confianza.")
        print(f"  Confianza final: {confianza*100:.1f}%")
        print(f"  Posibles animales: {nombres}")
    print("=" * 40)

def adivinar():
    print("\n" + "=" * 50)
    print("  ETAPA 3: ADIVINAR")
    print("=" * 50)
    datos_animales, datos_preguntas = cargar_todo()
    nombres = [a["nombre"] for a in datos_animales["animales"]]
    print("Animales registrados:", nombres)

    while True:
        jugar(datos_animales, datos_preguntas)
        otra = input("\nJugar de nuevo? (s/n): ").strip().lower()
        if otra not in ("s", "si"):
            print("Fin del programa")
            break

# ============================================================
#                           MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  RSTeoriaInfo - Sistema Experto")
    print("  Red Semantica + Teoria de la Informacion")
    print("=" * 50)

    inicializador()
    entrenador()
    adivinar()
