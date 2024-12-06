# stylizedprint/themes.py

# Definición de temas predefinidos
PREDEFINED_THEMES = {
    "alerta": {
        "text_color": "red",
        "bg_color": "yellow"
    },
    "éxito": {
        "text_color": "white",
        "bg_color": "green"
    },
    "información": {
        "text_color": "blue",
        "bg_color": "cyan"
    },
    "advertencia": {
        "text_color": "yellow",
        "bg_color": "black"
    },
    "error": {
        "text_color": "white",
        "bg_color": "red"
    }
}

def get_theme(theme_name):
    """
    Retorna la configuración del tema especificado.

    :param theme_name: Nombre del tema predefinido.
    :return: Diccionario con las configuraciones de colores.
    :raises ValueError: Si el tema no existe.
    """
    theme = PREDEFINED_THEMES.get(theme_name.lower())
    if not theme:
        raise ValueError(f"El tema '{theme_name}' no está definido. Temas disponibles: {', '.join(PREDEFINED_THEMES.keys())}")
    return theme
