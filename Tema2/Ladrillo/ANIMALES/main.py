from ruamel.yaml import YAML
from pathlib import Path

def adivinador():
    yaml = YAML()
    archivo_tabla = Path('tabla.yaml')
    
    if not archivo_tabla.exists():
        print("Error: No se encuentra 'tabla.yaml'.")
        return

    with open(archivo_tabla, 'r') as file:
        datos_tabla = yaml.load(file)
    
    caracteristicas = datos_tabla['caracteristicas']
    tabla_animales = datos_tabla['tabla_animales']
    
    print("=== ADIVINADOR: EDICIÓN PESO PESADO ===")
    print("Piensa en uno de estos animales:")
    for i, animal in enumerate(tabla_animales.keys(), 1):
        print(f"{i}. {animal}")
    
    candidatos = list(tabla_animales.keys())
    
    def encontrar_mejor_pregunta(candidatos, caracteristicas, tabla_animales):
        mejor_pregunta = None
        mejor_division = len(candidatos)
        for idx, caracteristica in enumerate(caracteristicas):
            si = sum(1 for a in candidatos if tabla_animales[a]['respuestas'][idx] == 1)
            no = len(candidatos) - si
            division = abs(si - no)
            if division < mejor_division and (si > 0 and no > 0):
                mejor_division = division
                mejor_pregunta = (idx, caracteristica)
        return mejor_pregunta

    while len(candidatos) > 1:
        mejor_pregunta = encontrar_mejor_pregunta(candidatos, caracteristicas, tabla_animales)
        
        if mejor_pregunta is None:
            print(f"\nEmpate técnico entre: {', '.join(candidatos)}")
            break
            
        idx, pregunta = mejor_pregunta
        while True:
            resp = input(f"\n{pregunta} (si/no): ").strip().lower()
            if resp in ['si', 'sí', 's', '1']:
                valor = 1; break
            elif resp in ['no', 'n', '0']:
                valor = 0; break
            print("Por favor, responde con si o no.")
            
        candidatos = [a for a in candidatos if tabla_animales[a]['respuestas'][idx] == valor]
        
        print(f"Animales restantes ({len(candidatos)}):")
        for animal in candidatos:
            print(f"  - {animal}")

    if len(candidatos) == 1:
        print(f"\n¡Adiviné! Tu animal es: {candidatos[0]}")
    else:
        print("\nNo pude determinar el animal con exactitud.")

if __name__ == "__main__":
    adivinador()