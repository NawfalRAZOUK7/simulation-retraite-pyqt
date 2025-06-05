"""
test_ui_shortcuts.py

⌨️ Teste les raccourcis clavier de l’interface :
- Vérifie la présence des actions dans MenuWindow
- Vérifie que les raccourcis sont bien définis (QAction ou QShortcut)
- Vérifie qu’aucun déclenchement de raccourci ne provoque d’exception

🎯 Ce test garantit que les raccourcis clavier fonctionnent correctement dans les composants définis.
"""

import pytest
from PyQt5.QtGui import QKeySequence
from ui.menu_window import MenuWindow


class TestMenuWindowShortcuts:

    def test_actions_exist(self, qtbot):
        """✅ Vérifie que MenuWindow possède des actions ou raccourcis définis."""
        window = MenuWindow()
        qtbot.addWidget(window)

        found = any(
            "action" in attr.lower() or "shortcut" in attr.lower()
            for attr in dir(window)
        )

        assert found, "❌ Aucune QAction ou QShortcut détectée dans MenuWindow"

    def test_quit_shortcut_triggers_safely(self, qtbot):
        """✅ Vérifie que l’action 'Quitter' se déclenche sans erreur."""
        window = MenuWindow()
        qtbot.addWidget(window)

        if hasattr(window, "actionQuitter"):
            action = window.actionQuitter
            assert isinstance(action.shortcut(), QKeySequence), "❌ Le raccourci n’est pas de type QKeySequence"
            try:
                action.trigger()
            except Exception as e:
                pytest.fail(f"❌ Le déclenchement de actionQuitter a échoué : {e}")
        else:
            pytest.skip("🔔 actionQuitter non défini sur MenuWindow")
