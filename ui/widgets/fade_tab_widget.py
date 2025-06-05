# ui/widgets/fade_tab_widget.py

from PyQt5.QtWidgets import QTabWidget, QWidget
from PyQt5.QtCore import pyqtSlot, QEasingCurve
from ui.widgets.fade_widget import FadeWidget

class FadeTabWidget(QTabWidget):
    def __init__(self, parent=None, duration=350, easing=None):
        super().__init__(parent)
        self._duration = duration
        self._easing = easing or QEasingCurve.Linear
        self.currentChanged.connect(self._animate_fade)

    def addTab(self, widget: QWidget, title: str):
        """Ajoute un onglet et assure que le widget est visible à l’ajout."""
        widget.setVisible(True)  # ← utile pour éviter les erreurs d’état
        super().addTab(widget, title)

    @pyqtSlot(int)
    def _animate_fade(self, index):
        if index < 0:
            return  # Aucun onglet actif
        widget = self.widget(index)
        if widget is not None:
            # Ne pas réanimer si déjà FadeWidget
            if not isinstance(widget, FadeWidget):
                FadeWidget.fade_in(widget, duration=self._duration, easing=self._easing)
