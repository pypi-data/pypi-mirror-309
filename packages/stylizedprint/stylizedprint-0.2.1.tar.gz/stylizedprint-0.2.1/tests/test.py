# tests.py
from stylizedprint.core import StylizedPrinter
from stylizedprint.colors import apply_color
from stylizedprint.themes_func import apply_theme
from stylizedprint.styles import apply_style
from stylizedprint.borders import add_border
from stylizedprint.animations import gradual_print, blinking_text
from stylizedprint.formatting import justify_text
from stylizedprint.utils import print_with_time
from stylizedprint.separator import LineSeparator

def print_section_header(title):
    """
    Prints a section header with a decorative separator line.

    Args:
        title (str): Title of the section.
    """
    separator = LineSeparator("plain")
    print(f"\n{separator.join_lines('=' * 50)}")
    print(f" {title} ".center(50, '='))
    print(separator.join_lines('=' * 50))

def test_apply_color():
    print_section_header("Testing apply_color")
    print(apply_color("Text in red", text_color="red"))
    print(apply_color("Text with blue background", bg_color="blue"))
    print(apply_color("Text in yellow with black background", text_color="yellow", bg_color="black"))

def test_apply_style():
    print_section_header("Testing apply_style")
    print(apply_style("Bold text", bold=True))
    print(apply_style("Italic text", italic=True))
    print(apply_style("Underlined text", underline=True))
    print(apply_style("Strikethrough text", strikethrough=True))

def test_add_border():
    print_section_header("Testing add_border")
    print(add_border("Text with asterisk border", border_char="*"))
    print(add_border("Text with equal sign border", border_char="="))
    print(add_border("Text with hash border", border_char="#"))

def test_gradual_print():
    print_section_header("Testing gradual_print")
    gradual_print("Text printed gradually...", delay=0.05)

def test_blinking_text():
    print_section_header("Testing blinking_text")
    blinking_text("Blinking text", times=3, delay=0.5)

def test_justify_text():
    print_section_header("Testing justify_text")
    print(justify_text("Left-aligned text", alignment="left", width=40))
    print(justify_text("Centered text", alignment="center", width=40))
    print(justify_text("Right-aligned text", alignment="right", width=40))

def test_print_with_time():
    print_section_header("Testing print_with_time")
    print_with_time("Log entry with timestamp")

def test_stylized_printer():
    print_section_header("Testing StylizedPrinter class")
    printer = StylizedPrinter("Stylized text for testing")

    printer.print_colored(text_color="green", bg_color="black")

    printer.print_styled(bold=True)
    printer.print_styled(italic=True)
    printer.print_styled(underline=True)
    printer.print_styled(strikethrough=True)

    printer.print_with_border(border_char="*")

    printer.print_gradually(delay=0.05)

    printer.print_blinking(times=2, delay=0.3)

    printer.print_justified(alignment="left", width=40)
    printer.print_justified(alignment="center", width=40)
    printer.print_justified(alignment="right", width=40)

    printer.print_with_timestamp()

def error_test_apply_color():
    print_section_header("Testing apply_color with invalid color")
    print(apply_color("Invalid color", text_color="invalid_color", bg_color="invalid_bg"))

def error_test_apply_style():
    print_section_header("Testing apply_style with invalid parameters")
    try:
        print(apply_style("Testing", bold="yes", italic="no"))
    except TypeError as e:
        print(f"Expected error: {e}")

def error_test_add_border():
    print_section_header("Testing add_border with invalid border character")
    print(add_border("Border with invalid character", border_char="##"))

def error_test_gradual_print():
    print_section_header("Testing gradual_print with negative delay")
    try:
        gradual_print("Text with negative delay", delay=-0.1)
    except Exception as e:
        print(f"Expected error: {e}")

def error_test_blinking_text():
    print_section_header("Testing blinking_text with negative delay")
    try:
        blinking_text("Blinking text with negative delay", times=3, delay=-0.5)
    except Exception as e:
        print(f"Expected error: {e}")

def error_test_justify_text():
    print_section_header("Testing justify_text with invalid alignment")
    try:
        print(justify_text("Text with invalid alignment", alignment="middle", width=40))
    except Exception as e:
        print(f"Expected error: {e}")

def error_test_stylized_printer():
    print_section_header("Testing StylizedPrinter with invalid parameters")
    printer = StylizedPrinter("Stylized text for error testing")

    printer.print_colored(text_color="unknown_color", bg_color="unknown_bg")

    printer.print_with_border(border_char="**")

    try:
        printer.print_gradually(delay=-0.05)
    except Exception as e:
        print(f"Expected error: {e}")

    try:
        printer.print_blinking(times=3, delay=-0.3)
    except Exception as e:
        print(f"Expected error: {e}")

    try:
        printer.print_justified(alignment="diagonal", width=40)
    except Exception as e:
        print(f"Expected error: {e}")

def test_apply_theme_valid():
    print_section_header("Testing apply_theme with valid theme")
    printer = StylizedPrinter("Mensaje de alerta")
    printer.apply_theme("alerta")
    printer.print_colored()

def test_apply_theme_invalid():
    print_section_header("Testing apply_theme with invalid theme")
    printer = StylizedPrinter("Mensaje con tema inválido")
    printer.apply_theme("invalido")

def test_reset_theme():
    print_section_header("Testing reset_theme")
    printer = StylizedPrinter("Mensaje con tema 'éxito'")
    printer.apply_theme("éxito")
    printer.print_colored()
    printer.reset_theme()
    printer.print_colored(text_color="blue", bg_color="black")

def test_apply_theme_func_valid():
    print_section_header("Testing apply_theme function with valid theme")
    styled_text = apply_theme("Operación exitosa", "éxito")
    print(styled_text)

def test_apply_theme_func_invalid():
    print_section_header("Testing apply_theme function with invalid theme")
    try:
        styled_text = apply_theme("Operación fallida", "invalido")
        print(styled_text)  # Este mensaje no debería imprimirse
    except ValueError as e:
        print(f"Expected error: {e}")

def run_tests():
    print_section_header("Running All Tests")
    test_apply_color()
    test_apply_style()
    test_add_border()
    test_gradual_print()
    test_blinking_text()
    test_justify_text()
    test_print_with_time()
    test_stylized_printer()

    test_apply_theme_valid()
    test_apply_theme_invalid()
    test_reset_theme()
    test_apply_theme_func_valid()
    test_apply_theme_func_invalid()

    print_section_header("Running Error Tests")
    error_test_apply_color()
    error_test_apply_style()
    error_test_add_border()
    error_test_gradual_print()
    error_test_blinking_text()
    error_test_justify_text()
    error_test_stylized_printer()
    print("All tests completed.")

if __name__ == "__main__":
    run_tests()
