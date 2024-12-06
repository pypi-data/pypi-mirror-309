# stylizedprint/core.py

from .colors import apply_color
from .styles import apply_style
from .borders import add_border
from .animations import gradual_print, blinking_text
from .formatting import justify_text
from .utils import print_with_time
from .separator import LineSeparator
from .themes import get_theme
from rich.console import Console

console = Console()

class StylizedPrinter:
    def __init__(self, text):
        self.text = text
        self.text_color = None  # Color de texto del tema
        self.bg_color = None    # Color de fondo del tema
        self.styles = {}
        # Otros atributos existentes

    def print_colored(self, text_color=None, bg_color=None):
        """
        Imprime el texto con colores especificados.
        Prioriza los colores del tema si se ha aplicado uno.

        :param text_color: Color del texto (opcional).
        :param bg_color: Color de fondo (opcional).
        """
        try:
            # Determinar los colores finales
            final_text_color = self.text_color if self.text_color else text_color
            final_bg_color = self.bg_color if self.bg_color else bg_color

            # Aplicar los colores
            colored_text = apply_color(self.text, text_color=final_text_color, bg_color=final_bg_color)
            print(colored_text)
        except Exception as e:
            print(f"Error in print_colored: {e}")

    def print_styled(self, bold=False, italic=False, underline=False, strikethrough=False):
        try:
            styled_text = apply_style(self.text, bold, italic, underline, strikethrough)
            console.print(styled_text)
        except Exception as e:
            print(f"Error in print_styled: {e}")

    def print_with_border(self, border_char="*"):
        try:
            bordered_text = add_border(self.text, border_char)
            print(bordered_text)
        except Exception as e:
            print(f"Error in print_with_border: {e}")

    def print_gradually(self, delay=0.1):
        try:
            gradual_print(self.text, delay)
        except Exception as e:
            print(f"Error in print_gradually: {e}")

    def print_blinking(self, times=3, delay=0.5):
        try:
            blinking_text(self.text, times, delay)
        except Exception as e:
            print(f"Error in print_blinking: {e}")

    def print_justified(self, alignment="center", width=50):
        try:
            justified_text = justify_text(self.text, alignment, width)
            print(justified_text)
        except Exception as e:
            print(f"Error in print_justified: {e}")

    def print_with_timestamp(self):
        try:
            print_with_time(self.text)
        except Exception as e:
            print(f"Error in print_with_timestamp: {e}")

    def print_with_separator(self, separator_type="plain", *lines, custom_separator=None):
        """
        Imprime múltiples líneas con un tipo de separador elegido.

        Args:
            separator_type (str): Tipo de separador (plain, html, custom).
            *lines: Líneas de texto para unir e imprimir.
            custom_separator (str): Separador personalizado si separator_type es "custom".
        """
        separator = LineSeparator(separator_type)
        if custom_separator:
            separator.set_custom_separator(custom_separator)
        joined_text = separator.join_lines(*lines)
        print(joined_text)

    def apply_theme(self, theme_name):
        """
        Aplica un tema predefinido al texto.

        :param theme_name: Nombre del tema predefinido.
        """
        try:
            theme = get_theme(theme_name)
            self.text_color = theme.get("text_color")
            self.bg_color = theme.get("bg_color")
        except ValueError as e:
            print(f"Error al aplicar tema: {e}")

    def reset_theme(self):
        """
        Resetea los colores del tema, permitiendo usar colores individuales nuevamente.
        """
        self.text_color = None
        self.bg_color = None
