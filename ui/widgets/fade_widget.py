# ui/widgets/fade_widget.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QBrush, QColor

class FadeWidget(QWidget):
    _active_animations = {}

    def __init__(self, widget: QWidget, fade_in=True, duration=350, parent=None,
                 easing=QEasingCurve.InOutQuad, finished_callback=None):
        super().__init__(parent)
        self._opacity = 0.0 if fade_in else 1.0
        self._inner = widget
        self._fade_in = fade_in
        self.duration = duration
        self.easing = easing or QEasingCurve.Linear
        self.finished_callback = finished_callback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)

        self.anim = QPropertyAnimation(self, b"opacity")
        self.anim.setDuration(duration)
        self.anim.setEasingCurve(self.easing)
        self.anim.setStartValue(0.0 if fade_in else 1.0)
        self.anim.setEndValue(1.0 if fade_in else 0.0)
        self.anim.finished.connect(self._on_finished)

        FadeWidget._active_animations[self] = self
        self.setVisible(True)

    def start(self):
        self.anim.start()

    def _on_finished(self):
        if not self._fade_in:
            self.setVisible(False)
        FadeWidget._active_animations.pop(self, None)
        if self.finished_callback:
            self.finished_callback()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        painter.fillRect(self.rect(), QBrush(QColor(255, 255, 255)))  # fond blanc (optionnel)
        super().paintEvent(event)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.update()

    opacity = pyqtProperty(float, fget=get_opacity, fset=set_opacity)

    def fade_in(self, duration=350, easing=QEasingCurve.InOutQuad, finished_callback=None):
        self.anim.stop()
        self.anim.setDuration(duration)
        self.anim.setEasingCurve(easing)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        if finished_callback:
            self.anim.finished.connect(finished_callback)
        self.setVisible(True)
        self.anim.start()
