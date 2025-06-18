# main.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.menu_window import MenuWindow
import sys

def excepthook(type, value, traceback):
    print("Exception:", value)

sys.excepthook = excepthook

if __name__ == "__main__":
    # ✅ Active l'adaptation haute résolution (Retina/4K)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # ❌ Thème désactivé : on n’applique aucun QPalette
    # from utils.theme_utils import load_theme_pref
    # from ui.theme import get_custom_palette, get_dark_palette
    # dark = load_theme_pref()
    # palette = get_dark_palette() if dark else get_custom_palette()
    # app.setPalette(palette)

    # ✅ Style global pour forcer la couleur des textes visibles
    app.setStyleSheet("""
        QWidget {
            color: #2c2f4c;
            background-color: #f5f6fb;
        }
        QLabel {
            color: #2c2f4c;
        }
        QPushButton {
            color: #2c2f4c;
            font-size: 16px;
            border-radius: 12px;
            padding: 8px 12px;
        }
    """)

    win = MenuWindow()
    win.show()
    sys.exit(app.exec_())
