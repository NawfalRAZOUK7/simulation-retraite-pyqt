# utils/mpl_theme.py

import matplotlib as mpl
from ui.theme import MPL_COLORS, FONT_FAMILY, FONT_SIZE

def set_mpl_theme(dark_mode=False):
    """
    Applique un thème matplotlib cohérent avec le thème Qt (clair ou sombre),
    incluant palette de couleurs, fonds, polices, tailles, styles de légende, etc.
    Appelle cette fonction à chaque changement de mode pour homogénéiser tous tes plots.
    """
    base_colors = MPL_COLORS
    # Couleurs adaptées dark/clair
    if dark_mode:
        bg = base_colors.get("dark_background", "#181C20")
        fg = "#EEE"
        grid = "#444"
        legend_face = "#232B34"
        legend_edge = "#444"
        tooltip_bg = "#232B34"
        tooltip_fg = "#F8FBFF"
    else:
        bg = base_colors["background"]
        fg = "#222"
        grid = "#DDE3EA"
        legend_face = "#F8FBFF"
        legend_edge = "#AAA"
        tooltip_bg = "#F8FBFF"
        tooltip_fg = "#282C34"

    # Palette matplotlib mise à jour
    mpl.rcParams.update({
        # --- Couleurs et fonds globaux ---
        "figure.facecolor": bg,
        "axes.facecolor": bg,
        "axes.edgecolor": fg,
        "axes.labelcolor": fg,
        "axes.titlesize": FONT_SIZE + 2,
        "axes.labelsize": FONT_SIZE + 1,
        "xtick.color": fg,
        "ytick.color": fg,
        "font.size": FONT_SIZE,
        "font.family": FONT_FAMILY.split(",")[0],
        # --- Légende ---
        "legend.facecolor": legend_face,
        "legend.edgecolor": legend_edge,
        "legend.fontsize": FONT_SIZE - 1,
        # --- Palette des courbes ---
        "axes.prop_cycle": mpl.cycler(color=[
            base_colors["reserve"],
            base_colors["confidence"],
            base_colors["highlight"],
            base_colors["danger"],
            base_colors["success"]
        ]),
        # --- Grille ---
        "grid.color": grid,
        "grid.linestyle": "--",
        "grid.alpha": 0.5,
        # --- Export ---
        "savefig.facecolor": bg,
        "savefig.edgecolor": bg,
        "savefig.dpi": 150,
        # --- Styles ---
        "errorbar.capsize": 4,
        "lines.linewidth": 2.2,
        "lines.markersize": 7,
        # --- Interactions/bonus ---
        # (Optionnel) Tooltips/annotations (pour plot_helpers, hover)
        # On ne peut pas définir le style tooltip global, mais tu peux le centraliser ici :
        # "text.color": fg,  # Utilisé pour texte dynamique si besoin
    })

    # BONUS : si tu utilises plot_helpers pour tooltips, tu peux centraliser les couleurs ici :
    mpl._MPL_TOOLTIP_BG = tooltip_bg
    mpl._MPL_TOOLTIP_FG = tooltip_fg

# --- UTILISATION ---
"""
from utils.mpl_theme import set_mpl_theme

# Appeler à chaque changement de mode :
set_mpl_theme(dark_mode=True)   # Pour le mode sombre
set_mpl_theme(dark_mode=False)  # Pour le mode clair
"""
