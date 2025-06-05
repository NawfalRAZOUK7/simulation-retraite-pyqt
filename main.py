# main.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.menu_window import MenuWindow
from utils.theme_utils import load_theme_pref
from ui.theme import get_custom_palette, get_dark_palette
import sys


def excepthook(type, value, traceback):
    print("Exception:", value)


sys.excepthook = excepthook

if __name__ == "__main__":
    # (Bonus) High-DPI scaling for retina/4K
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # (Bonus) Apply saved theme on app start
    try:
        from PyQt5.QtWidgets import QApplication

        dark = load_theme_pref()
        palette = get_dark_palette() if dark else get_custom_palette()
        app.setPalette(palette)
    except Exception:
        pass

    win = MenuWindow()
    win.show()
    sys.exit(app.exec_())
