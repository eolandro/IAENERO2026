from pathlib import Path;
from ruamel.yaml import YAML;
import argparse;

def leerGrafo():
    parser = argparse.ArgumentParser();
    parser.add_argument('Archivo', help='Archivo YAML que contiene el grafo', type=Path);
    args = parser.parse_args();
    if args.Archivo.exists():
        print(f'Archivo {args.Archivo} encontrado. Cargando grafo...');
        yaml = YAML(typ='safe');
        with args.Archivo.open('r') as arch_yaml:
            grafo1 = yaml.load(arch_yaml);
            print("pP_ID(grafo1, 'A', 'ACBA')");
            print("pP_DI(grafo1, 'A', 'ACBA')");
            print("pA(grafo1, 'A', 'ACBA')");
            return grafo1;
    else:
        print(f'Archivo {args.Archivo} no encontrado;');
        return None;

# pP_ID (Primero en Profundidad - Izquierda-Derecha)
def pP_ID(G, R, B):
    #Si R no es una llave en el diccionario se busca dentro de los hijios
    if R not in G:
        #print(f"Raiz: {R} no encontrada como clave, buscando en subgrafos...");
        if isinstance(G, dict):
            #print(f"Subgrafos disponibles: {list(G.keys())}");
            for clave in G:
                #print(f"Buscando en subgrafo: {clave}");
                if pP_ID(G[clave], R, B):
                    #print(f"Raiz: {R} encontrada en subgrafo {clave}");
                    return True;
        return False;
    if R == B:
        #print(f"Destino {B} encontrado!");
        return True;
    #Obtener hijos
    if isinstance(G, dict) and R in G:
        #print(f"Raiz: {R} encontrada, obteniendo hijos...");
        hijos = G[R];
        #print(f"Hijos de {R}: {hijos}");
    else:
        #print(f"Raiz: {R} no tiene hijos o no es un diccionario.");
        return False;
    #Recorrer hijos
    if isinstance(hijos, list):
        #print(f"Recorriendo hijos de {R} (lista)...");
        for hijo in hijos:
            #print(f"Visitando hijo: {hijo} de {R}");
            if hijo == B: return True;
            #print(f"Stack actual (antes de visitar {hijo}): {[h for h in hijos if h != hijo]}");
    elif isinstance(hijos, dict):
        #print(f"Recorriendo hijos de {R} (diccionario)...");
        for hijo in hijos:
            #print(f"Visitando hijo: {hijo} de {R}");
            if pP_ID(hijos, hijo, B):
                #print(f"Destino {B} encontrado a través de {hijo}!");
                return True;
    return False;

# pP_DI (Primero en Profundidad - Derecha-Izquierda)
def pP_DI(G, R, B):
    if R not in G:
        #print(f"Raiz: {R} no encontrada como clave, buscando en subgrafos...");
        if isinstance(G, dict):
            #print(f"Subgrafos disponibles: {list(G.keys())}");
            claves_invertidas = list(G.keys());
            #Invertir
            claves_invertidas.reverse();
            for clave in claves_invertidas:
                #print(f"Buscando en subgrafo: {clave}");
                if pP_DI(G[clave], R, B): 
                    #print(f"Raiz: {R} encontrada en subgrafo {clave}");
                    return True;
        #print(f"Raiz: {R} no encontrada en ningún subgrafo.");
        return False;
    if R == B:
        #print(f"Destino {B} encontrado!");
        return True;
    if isinstance(G, dict) and R in G:
        #print(f"Raiz: {R} encontrada, obteniendo hijos...");
        hijos = G[R];
        #print(f"Hijos de {R}: {hijos}");
    else: 
        #print(f"Raiz: {R} no tiene hijos o no es un diccionario.");
        return False;
    #print(f"Visitando: {R} (Modo Invertido). Hijos: {hijos};");
    if isinstance(hijos, list):
        #Invertir hijos
        for hijo in hijos[::-1]:
            #print(f"Checando hijo: {hijo};");
            if hijo == B: 
                return True;
    elif isinstance(hijos, dict):
        #print(f"Recorriendo hijos de {R} (diccionario) en orden invertido...");
        claves = list(hijos.keys());
        #print(f"Claves antes de invertir: {claves}");
        claves.reverse();
        #print(f"Claves después de invertir: {claves}");
        for hijo in claves:
            #print(f"Visitando hijo: {hijo} de {R} (Modo Invertido)");
            if pP_DI(hijos, hijo, B): return True;
    return False;

# pA (Búsqueda en Anchura - Iterativo con Cola)
def pA(G, R, B):
    #Validación inicial de raíz
    if R not in G and not isinstance(G, dict):
        return False; 
    cola = [(R, G)];
    print(f"Cola inicial: {cola}");
    while cola:
        #Obtener el primero (Frente de la cola)
        nodo, subgrafo = cola[0];
        #Eliminar el primero
        cola = cola[1:];
        print(f"Visitando: {nodo}");
        if nodo == B:
            print(f"Destino {B} encontrado!");
            return True;
        if isinstance(subgrafo, dict) and nodo in subgrafo:
            hijos = subgrafo[nodo];
            if isinstance(hijos, list):
                for hijo in hijos:
                    cola.append((hijo, hijos));
            elif isinstance(hijos, dict):
                for hijo in hijos:
                    cola.append((hijo, hijos));
    return False;

#
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
