"""
test_widgets.py

Teste les widgets personnalisés de l’interface :
- AnimatedToolButton : animation de clic
- FadeTabWidget : animation de changement d’onglet
- FadeWidget : visibilité avec effet fondu

Ces tests garantissent que les widgets graphiques personnalisés fonctionnent
sans erreur lors de leur création et de leur interaction basique.
"""

import pytest
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QTimer
import sys

from ui.widgets.animated_tool_button import AnimatedToolButton
from ui.widgets.fade_tab_widget import FadeTabWidget
from ui.widgets.fade_widget import FadeWidget


app = QApplication(sys.argv)


class TestWidgets:
    def test_animated_tool_button_init(self):
        """Teste la création d’un bouton animé."""
        btn = AnimatedToolButton()
        assert btn is not None
        assert btn.animation is not None
        assert btn.iconSize().width() > 0  # taille icône définie

    def test_fade_widget_toggle(self, qtbot):
        """Teste les effets de fade in/out sur le widget."""
        widget = FadeWidget(QWidget())
        qtbot.addWidget(widget)

        # Affiche le widget
        widget.fade_in()
        assert widget.isVisible()

        # Masque avec fondu
        widget.fade_out()
        assert not widget.isVisible()

    def test_fade_tab_widget_add_tab(self, qtbot):
        """Teste qu’on peut ajouter des onglets à FadeTabWidget."""
        tab_widget = FadeTabWidget()
        qtbot.addWidget(tab_widget)

        w1 = QWidget()
        w2 = QWidget()
        tab_widget.addTab(w1, "Onglet 1")
        tab_widget.addTab(w2, "Onglet 2")

        assert tab_widget.count() == 2

    def test_fade_tab_widget_switch_tab(self, qtbot):
        """Teste le changement d’onglet avec effet de transition."""
        tab_widget = FadeTabWidget()
        qtbot.addWidget(tab_widget)

        tab_widget.addTab(QWidget(), "One")
        tab_widget.addTab(QWidget(), "Two")

        current_index = tab_widget.currentIndex()
        next_index = 1 if current_index == 0 else 0
        tab_widget.setCurrentIndex(next_index)

        assert tab_widget.currentIndex() == next_index
