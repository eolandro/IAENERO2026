import json
import pandas as pd
import math

def cargar_dataset():
    with open('adivinar_dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data['animales'])
    atributos = data['atributos']
    print(f" {len(df)} animales | {len(atributos)} atributos")
    return df, atributos

def ganancia_info(df, atributo):
    if len(df) <= 1:
        return 0
    total = len(df)
    counts = df['animal'].value_counts()
    entropia_total = -sum((c/total * math.log2(c/total) for c in counts.values))
    
    valores = df[atributo].value_counts()
    ent_cond = 0
    for k, count in valores.items():
        if count == 0:
            continue
        sub_df = df[df[atributo] == k]
        sub_counts = sub_df['animal'].value_counts()
        ent_sub = 0
        for c in sub_counts.values:
            if c > 0:
                ent_sub -= (c/count) * math.log2(c/count)
        ent_cond += (count/total) * ent_sub
    return entropia_total - ent_cond

def mejor_atributo(df, atributos):
    ganancias = {}
    for a in atributos:
        if len(df[a].value_counts()) > 1:
            ganancias[a] = ganancia_info(df, a)
    return max(ganancias, key=ganancias.get) if ganancias else None

def jugar():
    df, atributos = cargar_dataset()
    actuales = df.copy()
    preguntas = 0
    
    print(" Piensa un animal")
    print("1=Sí 0=No")
    
    while len(actuales) > 1:
        attr = mejor_atributo(actuales, atributos)
        if attr is None:
            print("Posibles:", actuales['animal'].tolist())
            return
        
        resp = int(input(f"\n ¿{attr}? "))
        preguntas += 1
        actuales = actuales[actuales[attr] == resp]
        print(f" {len(actuales)} restantes")
    
    if len(actuales) > 0:
        print(f"\n ¡{actuales['animal'].iloc[0]}! ({preguntas} preguntas)")
    else:
        print(" No encontrado")

if __name__ == "__main__":
    jugar()
