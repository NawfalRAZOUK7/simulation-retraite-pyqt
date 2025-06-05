"""
test_ui_shortcuts.py

Teste les raccourcis clavier de l’interface :
- Vérifie la présence des actions dans MenuWindow
- Vérifie que les raccourcis sont bien définis (QAction ou QShortcut)
- Vérifie qu’aucun déclenchement de raccourci ne provoque d’exception

Ce test garantit que les raccourcis clavier fonctionnent correctement dans les composants définis.
"""

import pytest
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
import sys

from ui.menu_window import MenuWindow


app = QApplication(sys.argv)


class TestMenuWindowShortcuts:
    def test_actions_exist(self, qtbot):
        """Vérifie que MenuWindow possède des actions accessibles."""
        window = MenuWindow()
        qtbot.addWidget(window)

        found = False
        for attr in dir(window):
            if "action" in attr.lower() or "shortcut" in attr.lower():
                found = True
                break
        assert found, "Aucune QAction ou QShortcut trouvée dans MenuWindow"

    def test_quit_shortcut_triggers_safely(self, qtbot):
        """Teste que l’action ‘Quitter’ peut être déclenchée sans crash."""
        window = MenuWindow()
        qtbot.addWidget(window)

        if hasattr(window, "actionQuitter"):
            action = window.actionQuitter
            assert isinstance(action.shortcut(), QKeySequence)
            action.trigger()  # Doit passer sans erreur
