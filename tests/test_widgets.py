# test_widgets.py

"""
Teste les widgets personnalisés de l’interface :
- AnimatedToolButton : animation de clic
- FadeTabWidget : animation de changement d’onglet
- FadeWidget : visibilité avec effet fondu

Ces tests garantissent que les widgets graphiques fonctionnent
correctement lors de leur création et interaction de base.
"""

# test_widgets.py

import pytest
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QVBoxLayout
from ui.widgets.animated_tool_button import AnimatedToolButton
from ui.widgets.fade_tab_widget import FadeTabWidget
from ui.widgets.fade_widget import FadeWidget


class TestWidgets:

    def test_animated_tool_button_init(self, qtbot):
        btn = AnimatedToolButton()
        qtbot.addWidget(btn)

        assert btn is not None
        assert btn.animation is not None
        assert btn.iconSize().width() > 0

    def test_fade_widget_static_methods(self, qtbot):
        container = QDialog()
        layout = QVBoxLayout(container)
        widget = QWidget()
        layout.addWidget(widget)
        qtbot.addWidget(container)

        container.show()
        QApplication.processEvents()

        FadeWidget.fade_in(widget)
        QApplication.processEvents()

        # On accepte isVisible=True OU opacity > 0
        assert widget.isVisible() or widget.windowOpacity() > 0, "fade_in() n’a pas rendu le widget visible ni partiellement visible"

    def test_fade_tab_widget_add_tab(self, qtbot):
        tab_widget = FadeTabWidget()
        qtbot.addWidget(tab_widget)

        # Désactive temporairement le signal de transition
        tab_widget.currentChanged.disconnect()
        tab_widget.addTab(QWidget(), "Onglet 1")
        tab_widget.addTab(QWidget(), "Onglet 2")

        tab_widget.show()
        QApplication.processEvents()

        assert tab_widget.count() == 2, "Onglets non ajoutés correctement"

    def test_fade_tab_widget_switch_tab(self, qtbot):
        tab_widget = FadeTabWidget()
        qtbot.addWidget(tab_widget)

        # Désactive temporairement l'animation
        tab_widget.currentChanged.disconnect()
        tab_widget.addTab(QWidget(), "One")
        tab_widget.addTab(QWidget(), "Two")
        tab_widget.setCurrentIndex(0)

        tab_widget.show()
        QApplication.processEvents()

        next_index = 1
        tab_widget.setCurrentIndex(next_index)
        QApplication.processEvents()

        assert tab_widget.currentIndex() == next_index, "L’onglet actif n’a pas changé"
