
from .themes import get_theme
from .colors import apply_color

from .colors import apply_color
from .styles import apply_style
from .borders import add_border
from .animations import gradual_print, blinking_text

# Diccionario de temas predefinidos
THEMES = {
    "alerta": {"text_color": "red", "bg_color": "yellow", "bold": True},
    "éxito": {"text_color": "white", "bg_color": "green", "bold": True},
    "error": {"text_color": "white", "bg_color": "red", "bold": True},
    "información": {"text_color": "blue", "bg_color": "cyan"},
    "advertencia": {"text_color": "yellow", "bg_color": "black"},
}

def apply_theme(text, theme_name):
    """
    Aplica un tema predefinido al texto.

    Args:
        text (str): El texto al que se le aplicará el tema.
        theme_name (str): El nombre del tema a aplicar.

    Returns:
        str: El texto estilizado según el tema.
    
    Raises:
        ValueError: Si el tema no está definido.
    """
    if theme_name not in THEMES:
        raise ValueError(f"Theme '{theme_name}' is not defined.")
    
    theme = THEMES[theme_name]
    styled_text = apply_color(text, 
                              text_color=theme.get("text_color"), 
                              bg_color=theme.get("bg_color"))
    styled_text = apply_style(styled_text, 
                              bold=theme.get("bold", False), 
                              italic=theme.get("italic", False),
                              underline=theme.get("underline", False),
                              strikethrough=theme.get("strikethrough", False))
    return styled_text

def reset_theme():
    """
    Restablece los estilos a los valores predeterminados.

    Returns:
        str: Texto sin estilos aplicados.
    """
    return ""