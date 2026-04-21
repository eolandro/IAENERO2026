from pathlib import Path;
from ruamel.yaml import YAML;
import argparse;
import random;

def leerGrafo():
    parser = argparse.ArgumentParser();
    parser.add_argument('Archivo', help='Archivo YAML que contiene el grafo', type=Path);
    args = parser.parse_args();
    if args.Archivo.exists():
        print(f'Archivo {args.Archivo} encontrado. Cargando grafo...');
        yaml = YAML(typ='safe');
        with args.Archivo.open('r') as arch_yaml:
            grafo1 = yaml.load(arch_yaml);
            print("sb_M(grafo1, 'A', 'J', 10)");
            print("sb_m(grafo1, 'A', 'J', 10)");
            return grafo1; 
    else:
        print(f'Archivo {args.Archivo} no encontrado;');
        return None;

#Inicio de busqueda
def ejecutar_busqueda(G, inicio, fin, max_pasos, tipo):
    actual = inicio;
    total_costo = 0;
    pasos_dados = 0;
    stack = [];
    camino_recorrido = [inicio];
    while actual != fin and pasos_dados < max_pasos:
        #Obtener vecinos
        opciones = [linea for linea in G['grafo']['lineas'] if linea['origen'] == actual];
        #Verificar los nodos
        opciones_validas = [opt for opt in opciones if opt['destino'] not in stack];
        if not opciones_validas:
            print(f"Ya no se puede avanzar, fin !!!");
            break;
        #Checar pesos
        pesos = [opt['peso'] for opt in opciones_validas];
        mejor_peso = max(pesos) if tipo == "MAX" else min(pesos);
        #Pesos iguales
        candidatos = [opt for opt in opciones_validas if opt['peso'] == mejor_peso];
        seleccion = random.choice(candidatos);
        total_costo += seleccion['peso'];
        pasos_dados += 1;
        #Actualizar stack
        stack.append(actual);
        if len(stack) > 3:
            stack.pop(0);
        actual = seleccion['destino'];
        camino_recorrido.append(actual);
        
        print(f"Paso {pasos_dados}:\n De {seleccion['origen']} a {actual}\n Peso: {seleccion['peso']}\n Stack: {stack}\n Costo Total: {total_costo}");
        print("-" * 50);
    if actual == fin:
        return f"Ruta: {' -> '.join(camino_recorrido)}. Costo Total: {total_costo};";
    else:
        return f"Numero de nodos agotados en {actual}. Costo Total: {total_costo};";

# sb_M: Largo
def sb_M(G, inicio, fin, max_p):
    return ejecutar_busqueda(G, inicio, fin, max_p, "MAX");

# sb_m: Corto
def sb_m(G, inicio, fin, max_p):
    return ejecutar_busqueda(G, inicio, fin, max_p, "min");

def main():
    grafo1 = leerGrafo();
    if grafo1 is None: return;
    while True:
        Read = input("> ");
        if Read.strip() == "exit":
            print("Sayonara baby!");
            break;
        try:
            EVAL = eval(Read);
            print(f"Resultado: {EVAL}");
        except Exception as e:
            print(f"Error al evaluar: {e}; \n Escriba bien baboso!");

if __name__ == "__main__":
    main();