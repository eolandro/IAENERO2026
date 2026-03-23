#inicializador.py
#Define los animales, características y preguntas del juego

#Lista de animales
ANIMALES = [
    "Perro", "Gato", "Hamster", "Sapo", "Caballo",
    "Gallina", "Quetzal", "Huron", "Castor", "Lobo",
    "Vaca", "Foca"
]

#Características con sus pesos binarios (columnas de la tabla)
#Orden: Colorido, Cuadrupedo, Bigotes, Pequeño, Carrera, Construye, Largo, Gordita(o), Manchas, Aullido, Huevo, Salta
CARACTERISTICAS = [
    "Colorido",
    "Cuadrupedo",
    "Bigotes",
    "Pequeño",
    "Carrera",
    "Construye",
    "Largo",
    "Gordita(o)",
    "Manchas",
    "Aullido",
    "Huevo",
    "Salta"
]

#Preguntas asociadas a cada característica
PREGUNTAS = {
    "Colorido":    "¿Tu animal tiene colores llamativos o vistosos?",
    "Cuadrupedo":  "¿Tu animal camina en cuatro patas?",
    "Bigotes":     "¿Tu animal tiene bigotes?",
    "Pequeño":     "¿Tu animal es pequeño (cabe en tus manos)?",
    "Carrera":     "¿Tu animal puede correr muy rápido?",
    "Construye":   "¿Tu animal construye estructuras (madrigueras, nidos, represas...)?",
    "Largo":       "¿Tu animal tiene el cuerpo alargado?",
    "Gordita(o)":  "¿Tu animal tiene cuerpo redondo o gordito?",
    "Manchas":     "¿Tu animal tiene manchas en su cuerpo?",
    "Aullido":     "¿Tu animal emite aullidos?",
    "Huevo":       "¿Tu animal nace de un huevo?",
    "Salta":       "¿Tu animal salta como forma principal de moverse?"
}

#Pesos para ordenar la importancia de las características (de mayor a menor)
#Refleja los valores de la fila amarilla de la tabla original
PESOS = {
    "Colorido":   2048,
    "Cuadrupedo": 1024,
    "Bigotes":     512,
    "Pequeño":     256,
    "Carrera":     128,
    "Construye":    64,
    "Largo":        32,
    "Gordita(o)":   16,
    "Manchas":       8,
    "Aullido":       4,
    "Huevo":         2,
    "Salta":         1
}
