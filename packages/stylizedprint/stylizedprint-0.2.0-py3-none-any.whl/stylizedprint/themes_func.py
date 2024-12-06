
from .themes import get_theme
from .colors import apply_color

def apply_theme(text, theme_name):
    """
    Aplica un tema predefinido al texto y retorna el texto estilizado.

    :param text: Texto a estilizar.
    :param theme_name: Nombre del tema predefinido.
    :return: Texto estilizado con los colores del tema.
    :raises ValueError: Si el tema no existe.
    """
    try:
        theme = get_theme(theme_name)
        return apply_color(text, text_color=theme.get("text_color"), bg_color=theme.get("bg_color"))
    except ValueError as e:
        print(f"Error al aplicar tema: {e}")
        return text