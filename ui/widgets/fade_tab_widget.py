# ui/widgets/fade_tab_widget.py

from PyQt5.QtWidgets import QTabWidget, QWidget
from PyQt5.QtCore import pyqtSlot, QEasingCurve
from ui.widgets.fade_widget import FadeWidget

class FadeTabWidget(QTabWidget):
    def __init__(self, parent=None, duration=350, easing=None):
        super().__init__(parent)
        self._duration = duration
        self._easing = easing or QEasingCurve.Linear
        self._tab_widgets = []  # 🔒 Références internes pour éviter la suppression par GC
        self.currentChanged.connect(self._on_tab_changed)

    def addTab(self, widget: QWidget, title: str):
        """Ajoute un onglet avec un effet de fondu via FadeWidget."""
        fade_widget = FadeWidget(widget)
        fade_widget.setVisible(True)  # ⚠️ Nécessaire pour affichage initial
        self._tab_widgets.append(fade_widget)  # 🔒 Pour garder une référence
        super().addTab(fade_widget, title)

    @pyqtSlot(int)
    def _on_tab_changed(self, index):
        """Lance l’animation de fondu à chaque changement d’onglet."""
        try:
            widget = self.widget(index)
            if isinstance(widget, FadeWidget):
                widget.fade_in(duration=self._duration, easing=self._easing)
        except Exception as e:
            print(f"[FadeTabWidget] Erreur dans _on_tab_changed: {e}")
