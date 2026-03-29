"""
R005 - Minimización de If
Módulo de utilidades que evita árboles de control con múltiples if-else.
Se usan diccionarios de despacho, map/filter y operadores lógicos en su lugar.
"""

# ──────────────────────────────────────────────────────────────
# Dispatcher: reemplaza cadenas de if-else con un dict de funciones
# ──────────────────────────────────────────────────────────────


def dispatch(key: str, tabla: dict, *args, **kwargs):
    """
    Ejecuta la función asociada a 'key' en 'tabla'.
    Si la clave no existe, ejecuta 'default' (si está definida).
    Elimina la necesidad de if-elif-else para selección de acciones.
    """
    accion = tabla.get(key, tabla.get("default", lambda *a, **k: None))
    return accion(*args, **kwargs)


# ──────────────────────────────────────────────────────────────
# Validadores sin if explícito
# ──────────────────────────────────────────────────────────────


def es_valido(valor, condicion) -> bool:
    """Evalúa una condición sobre un valor sin if."""
    return condicion(valor)


def primer_verdadero(condiciones: list, valor):
    """
    Retorna la primera condición (etiqueta, fn) cuya fn(valor) sea True.
    Reemplaza una cadena de if-elif.
    """
    return next((etiqueta for etiqueta, fn in condiciones if fn(valor)), None)


# ──────────────────────────────────────────────────────────────
# Clasificación sin if: umbral → etiqueta
# ──────────────────────────────────────────────────────────────

REGLAS_CLASIFICACION = [
    ("spam", lambda p: p >= 0.5),
    ("no_spam", lambda p: p < 0.5),
]


def clasificar_por_probabilidad(probabilidad: float) -> str:
    """
    Determina la etiqueta según la probabilidad.
    Sin un solo if explícito: usa primer_verdadero + REGLAS_CLASIFICACION.
    """
    return primer_verdadero(REGLAS_CLASIFICACION, probabilidad) or "no_spam"


# ──────────────────────────────────────────────────────────────
# Métodos de consenso (sin if para seleccionar el método)
# ──────────────────────────────────────────────────────────────


def _consenso_media(probabilidades: list[float]) -> float:
    return sum(probabilidades) / len(probabilidades) if probabilidades else 0.0


def _consenso_mediana(probabilidades: list[float]) -> float:
    ordenadas = sorted(probabilidades)
    n = len(ordenadas)
    mitad = n // 2
    # Expresión ternaria: reemplaza if-else
    return (
        (ordenadas[mitad - 1] + ordenadas[mitad]) / 2
        if n % 2 == 0
        else ordenadas[mitad]
    )


def _consenso_moda(probabilidades: list[float]) -> float:
    """Moda: el valor más frecuente; si hay empate, usa la media."""
    from collections import Counter

    conteo = Counter(round(p, 2) for p in probabilidades)
    max_frec = max(conteo.values())
    modas = [v for v, c in conteo.items() if c == max_frec]
    return sum(modas) / len(modas)


def _consenso_democracia(probabilidades: list[float]) -> float:
    """Votación: fracción de probabilidades >= 0.5 (votos spam)."""
    votos = sum(1 for p in probabilidades if p >= 0.5)
    return votos / len(probabilidades) if probabilidades else 0.0


METODOS_CONSENSO: dict = {
    "media": _consenso_media,
    "mediana": _consenso_mediana,
    "moda": _consenso_moda,
    "democracia": _consenso_democracia,
    "default": _consenso_media,
}


def aplicar_consenso(probabilidades: list[float], metodo: str = "media") -> float:
    """
    Aplica el método de consenso seleccionado sin if-elif.
    Usa dispatch sobre METODOS_CONSENSO.
    """
    return dispatch(metodo, METODOS_CONSENSO, probabilidades)


# ──────────────────────────────────────────────────────────────
# Stop-words en español (artículos, preposiciones, conectores)
# ──────────────────────────────────────────────────────────────

STOP_WORDS: frozenset = frozenset(
    {
        # Artículos
        "el",
        "la",
        "los",
        "las",
        "un",
        "una",
        "unos",
        "unas",
        # Preposiciones
        "a",
        "ante",
        "bajo",
        "con",
        "contra",
        "de",
        "desde",
        "en",
        "entre",
        "hacia",
        "hasta",
        "para",
        "por",
        "según",
        "sin",
        "sobre",
        "tras",
        "durante",
        "mediante",
        # Conectores / conjunciones
        "y",
        "e",
        "ni",
        "o",
        "u",
        "pero",
        "sino",
        "porque",
        "aunque",
        "si",
        "que",
        "como",
        "cuando",
        "donde",
        "mientras",
        "pues",
        "entonces",
        "además",
        "también",
        "ya",
        "más",
        "menos",
        # Pronombres comunes
        "me",
        "te",
        "se",
        "nos",
        "lo",
        "le",
        "les",
        "tu",
        "su",
        "mi",
        "mis",
        "tus",
        "sus",
        "este",
        "esta",
        "estos",
        "estas",
        "ese",
        "esa",
        "esos",
        "esas",
        "aquel",
        # Verbos auxiliares muy frecuentes
        "es",
        "son",
        "era",
        "fue",
        "ser",
        "estar",
        "ha",
        "han",
        "he",
        "has",
        "hemos",
        "hay",
        "no",
        "del",
    }
)


def tokenizar(texto: str) -> list[str]:
    """
    Convierte texto en tokens limpios, filtrando stop-words.
    Usa map + filter: sin if explícito en el cuerpo.
    """
    import re

    normalizado = texto.lower()
    tokens_raw = re.findall(r"\b[a-záéíóúüñ]+\b", normalizado)
    return list(filter(lambda t: t not in STOP_WORDS and len(t) > 2, tokens_raw))
