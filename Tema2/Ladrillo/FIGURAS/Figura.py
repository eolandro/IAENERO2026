import yaml

try:
    with open("figuras.yaml", "r", encoding="utf-8") as f:
        datos = yaml.safe_load(f)
except: exit()

print("🎮 ¡ADIVINA LA FIGURA!")

preguntas = datos["preguntas"]
grafo = datos["grafo"]
nodo = "P0"

while nodo in preguntas:
    print(f"\n {preguntas[nodo]}")
    print("Opciones:", ', '.join(grafo[nodo]))
    
    resp = input("➤ ").strip().upper()
    
    try:
        nodo = grafo[nodo][resp]
    except:
        print("❌ Opción inválida")
        continue
        
    if nodo not in preguntas:
        print(f"\n🎉 ¡ES UN/A {nodo.upper()}!")
        break

print("¡Gracias por jugar!")