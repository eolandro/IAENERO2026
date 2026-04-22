from ruamel.yaml import YAML
from pathlib import Path

def adivinador():
    yaml = YAML()
    archivo_tabla = Path('tabla.yaml')
    
    if not archivo_tabla.exists():
        print("Error: No existe 'tabla.yaml'. Ejecuta el Entrenador primero.")
        return

    with open(archivo_tabla, 'r', encoding='utf-8') as file:
        datos = yaml.load(file)
    
    caracteristicas = datos['caracteristicas']
    tabla_animales = datos['tabla_animales']
    candidatos = list(tabla_animales.keys())
    
    print("=== ETAPA 3: SISTEMA EXPERTO (RSTeoriaInfo) ===")
    print(f"Piensa en uno de estos {len(candidatos)} animales...")

    while len(candidatos) > 1:
        # OPTIMIZACIÓN: Buscar pregunta que divida a los candidatos al 50/50
        mejor_pregunta_idx = -1
        mejor_division = len(candidatos)
        
        for idx in range(len(caracteristicas)):
            con_si = sum(1 for a in candidatos if tabla_animales[a]['respuestas'][idx] == 1)
            con_no = len(candidatos) - con_si
            
            # Buscamos la diferencia mínima entre SI y NO para maximizar Ganancia de Información
            division = abs(con_si - con_no)
            
            if con_si > 0 and con_no > 0: # Solo preguntas que filtren algo
                if division < mejor_division:
                    mejor_division = division
                    mejor_pregunta_idx = idx

        if mejor_pregunta_idx == -1:
            print("\nNo puedo diferenciar más a estos animales:", candidatos)
            break

        # Interacción con el usuario
        pregunta = caracteristicas[mejor_pregunta_idx]
        while True:
            resp = input(f"\n{pregunta} (si/no): ").strip().lower()
            if resp in ['si', 'sí', 's', '1']:
                valor = 1; break
            elif resp in ['no', 'n', '0']:
                valor = 0; break
            print("Por favor responde si/no.")

        # Filtrado de la Red Semántica
        candidatos = [a for a in candidatos if tabla_animales[a]['respuestas'][mejor_pregunta_idx] == valor]
        print(f"Animales posibles: {len(candidatos)}")

    if len(candidatos) == 1:
        print(f"\n¡Adiviné! Tu animal es el: {candidatos[0].upper()}")
    else:
        print("\nEl conocimiento actual es insuficiente para distinguir el animal.")

if __name__ == "__main__":
    adivinador()
