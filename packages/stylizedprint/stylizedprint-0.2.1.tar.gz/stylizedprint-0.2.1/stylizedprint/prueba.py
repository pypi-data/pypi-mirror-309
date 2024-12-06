from stylizedprint.colors import apply_color
from stylizedprint.themes_func import apply_theme

# Aplica el tema 'éxito' al texto
styled_text = apply_theme("Operación exitosa", "éxito")
print(styled_text)

# Aplicar colores individuales sin tema
styled_text = apply_color("Texto personalizado", text_color="blue", bg_color="yellow")
print(styled_text)
