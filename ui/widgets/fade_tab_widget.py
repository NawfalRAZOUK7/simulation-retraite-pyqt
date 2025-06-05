# ui/widgets/fade_tab_widget.py

from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSlot
from ui.widgets.fade_widget import FadeWidget

class FadeTabWidget(QTabWidget):
    def __init__(self, parent=None, duration=350, easing=None):
        super().__init__(parent)
        self._duration = duration
        self._easing = easing
        self.currentChanged.connect(self._animate_fade)

    @pyqtSlot(int)
    def _animate_fade(self, index):
        widget = self.widget(index)
        if widget:
            FadeWidget.fade_in(widget, duration=self._duration, easing=self._easing)
