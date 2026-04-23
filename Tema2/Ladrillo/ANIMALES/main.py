from ruamel.yaml import YAML
from pathlib import Path
import os

def adivinador():
    yaml = YAML()
    archivo_tabla = Path('tabla.yaml')
    
    if not archivo_tabla.exists():
        print("\nERROR: No se encuentra 'tabla.yaml'. Captura los 12 animales en el Entrenador.")
        return

    with open(archivo_tabla, 'r', encoding='utf-8') as file:
        datos = yaml.load(file)
    
    caracteristicas = datos['caracteristicas']
    tabla = datos['tabla_animales']
    
    # Esta lista depende de lo que hayas guardado en el Entrenador
    lista_maestra = list(tabla.keys()) 
    candidatos = list(lista_maestra)
    
    os.system('cls' if os.name == 'nt' else 'clear')

    print("============================================================")
    print("      RSTeoriaInfo: INSPECCION DE RED SEMANTICA             ")
    print("============================================================")
    # Aqui veras si realmente entrenaste a los 12 o solo a 6
    print(f"ANIMALES EN BASE DE DATOS: {len(lista_maestra)}")
    print(f"LISTA: {', '.join(lista_maestra)}")
    print("-" * 60)

    paso = 1
    while len(candidatos) > 1:
        mejor_idx = -1
        mejor_dif = len(candidatos)
        
        for i in range(len(caracteristicas)):
            si = sum(1 for a in candidatos if tabla[a]['respuestas'][i] == 1)
            no = len(candidatos) - si
            if si > 0 and no > 0:
                dif = abs(si - no)
                if dif < mejor_dif:
                    mejor_dif, mejor_idx = dif, i

        if mejor_idx == -1:
            print("\nAVISO: No hay mas caracteristicas para diferenciar a los restantes.")
            break

        pregunta = caracteristicas[mejor_idx]
        print(f"\nPASO {paso}")
        print(f"PREGUNTA: ¿El animal tiene o es '{pregunta}'?")
        
        while True:
            resp = input("RESPUESTA (s/n): ").strip().lower()
            if resp in ['s', 'si', '1']:
                valor = 1; break
            elif resp in ['n', 'no', '0']:
                valor = 0; break
            print("Entrada invalida.")

        candidatos = [a for a in candidatos if tabla[a]['respuestas'][mejor_idx] == valor]
        
        print("\n" + "-"*45)
        print(f"{'ESTADO':<15} | {'ANIMAL':<20}")
        print("-"*45)
        for animal in lista_maestra:
            estado = "  ACTIVO" if animal in candidatos else "ELIMINADO"
            print(f"{estado:<15} | {animal:<20}")
        
        print("-"*45)
        print(f"Candidatos restantes: {len(candidatos)}")
        paso += 1

    if len(candidatos) == 1:
        print("\n========================================")
        print(f" IDENTIFICACION FINAL: {candidatos[0].upper()} ")
        print("========================================\n")
    else:
        print("\nCONOCIMIENTO INSUFICIENTE PARA DIFERENCIAR.")

if __name__ == "__main__":
    adivinador()
