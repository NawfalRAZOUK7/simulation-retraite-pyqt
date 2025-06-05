# ui/theme.py

from PyQt5.QtGui import QPalette, QColor

# === Couleurs centralisées (modifie ici pour toute l'app) ===
PRIMARY_COLOR     = "#2077B4"      # Bleu principal (boutons, plots)
SECONDARY_COLOR   = "#70AD47"      # Vert (succès)
SUCCESS_COLOR     = "#2ECC71"      # Vert succès (bonus)
DANGER_COLOR      = "#C44D58"      # Rouge alerte
BACKGROUND_COLOR  = "#F5F7FB"      # Fond clair
TEXT_COLOR        = "#282C34"      # Texte foncé
HIGHLIGHT_COLOR   = "#3A99D8"      # Hover, sélection
ALT_ROW_COLOR     = "#E6E9F0"      # Lignes alternées

DISABLED_COLOR    = "#C0C4CC"      # Texte désactivé

DARK_BG           = "#282C34"
DARK_TEXT         = "#DFE1E6"
DARK_ALT_ROW      = "#323846"
DARK_HIGHLIGHT    = "#3A99D8"
DARK_DISABLED     = "#4A4E58"

# === Palette matplotlib harmonisée ===
MPL_COLORS = {
    "reserve": PRIMARY_COLOR,
    "confidence": SECONDARY_COLOR,
    "danger": DANGER_COLOR,
    "success": SUCCESS_COLOR,
    "highlight": HIGHLIGHT_COLOR,
    "background": BACKGROUND_COLOR,
    "dark_background": DARK_BG,
}

# === Fonts (matplotlib + Qt) ===
FONT_FAMILY = "Segoe UI, Arial, sans-serif"
FONT_SIZE   = 10

def get_custom_palette():
    """Palette Qt claire personnalisée."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.WindowText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(ALT_ROW_COLOR))
    palette.setColor(QPalette.ToolTipBase, QColor(250, 250, 210))
    palette.setColor(QPalette.ToolTipText, QColor(30, 30, 30))
    palette.setColor(QPalette.Text, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Button, QColor(229, 241, 251))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.BrightText, QColor(220, 0, 0))
    palette.setColor(QPalette.Link, QColor(HIGHLIGHT_COLOR))
    palette.setColor(QPalette.Highlight, QColor(HIGHLIGHT_COLOR))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(DISABLED_COLOR))
    return palette

def get_dark_palette():
    """Palette Qt sombre personnalisée."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(DARK_BG))
    palette.setColor(QPalette.WindowText, QColor(DARK_TEXT))
    palette.setColor(QPalette.Base, QColor("#22242b"))
    palette.setColor(QPalette.AlternateBase, QColor(DARK_ALT_ROW))
    palette.setColor(QPalette.ToolTipBase, QColor("#383b42"))
    palette.setColor(QPalette.ToolTipText, QColor("#fafafa"))
    palette.setColor(QPalette.Text, QColor(DARK_TEXT))
    palette.setColor(QPalette.Button, QColor("#232734"))
    palette.setColor(QPalette.ButtonText, QColor(DARK_TEXT))
    palette.setColor(QPalette.BrightText, QColor(255, 60, 60))
    palette.setColor(QPalette.Link, QColor(DARK_HIGHLIGHT))
    palette.setColor(QPalette.Highlight, QColor(DARK_HIGHLIGHT))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(DARK_DISABLED))
    return palette

def style_button(widget, color=PRIMARY_COLOR, dark_mode=False):
    """
    Applique un style bouton moderne (couleur principale, coins arrondis).
    """
    col = DARK_HIGHLIGHT if dark_mode else color
    hover = PRIMARY_COLOR if dark_mode else HIGHLIGHT_COLOR
    pressed = SECONDARY_COLOR if not dark_mode else DANGER_COLOR
    widget.setStyleSheet(
        f"""
        QPushButton {{
            background-color: {col};
            color: white;
            border: none;
            border-radius: 7px;
            padding: 7px 18px;
            font-weight: bold;
            font-size: 13px;
            min-width: 100px;
            transition: background 0.2s;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        QPushButton:pressed {{
            background-color: {pressed};
        }}
        """
    )

def get_tab_stylesheet(dark_mode=False):
    """
    Retourne la feuille de style QTabWidget selon le mode.
    """
    if dark_mode:
        return DARK_TAB_STYLESHEET
    else:
        return TAB_STYLESHEET

TAB_STYLESHEET = f"""
QTabBar::tab {{
    background: {BACKGROUND_COLOR};
    border: 1px solid #b4c3d6;
    border-radius: 8px 8px 0 0;
    padding: 8px 22px;
    color: {TEXT_COLOR};
    font-weight: bold;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background: {PRIMARY_COLOR};
    color: white;
}}
QTabBar::tab:hover {{
    background: {HIGHLIGHT_COLOR};
    color: white;
}}
QTabWidget::pane {{
    border: 1px solid #c7d2e0;
    border-radius: 9px;
    top: -2px;
}}
"""

DARK_TAB_STYLESHEET = f"""
QTabBar::tab {{
    background: {DARK_BG};
    border: 1px solid #44485c;
    border-radius: 8px 8px 0 0;
    padding: 8px 22px;
    color: {DARK_TEXT};
    font-weight: bold;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background: {DARK_HIGHLIGHT};
    color: white;
}}
QTabBar::tab:hover {{
    background: {PRIMARY_COLOR};
    color: white;
}}
QTabWidget::pane {{
    border: 1px solid #22242b;
    border-radius: 9px;
    top: -2px;
}}
"""

def apply_theme(app, dark_mode):
    """
    Applique la palette Qt et la feuille de style des onglets en fonction du mode (clair/sombre).
    """
    if dark_mode:
        app.setPalette(get_dark_palette())
        app.setStyleSheet(DARK_TAB_STYLESHEET)
    else:
        app.setPalette(get_custom_palette())
        app.setStyleSheet(TAB_STYLESHEET)

def get_highlight_color(dark_mode=False):
    """
    Renvoie la couleur de survol globale (utile pour d'autres widgets).
    """
    return DARK_HIGHLIGHT if dark_mode else HIGHLIGHT_COLOR

# === USAGE EXEMPLE (dans main.py) ===
"""
from PyQt5.QtWidgets import QApplication
from ui.theme import apply_theme

app = QApplication([])
app.setStyle('Fusion')
apply_theme(app, dark_mode=False)   # ou dark_mode=True
"""
