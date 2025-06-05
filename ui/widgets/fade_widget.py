from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, Qt

class FadeWidget(QWidget):
    """
    Animation avancée de fade-in ou fade-out sur n'importe quel QWidget.

    - fade_in=True : lève l'opacité de 0 à 1 (affichage progressif)
    - fade_in=False : baisse de 1 à 0 (disparition)
    - duration : ms (défaut 350)
    - easing : courbe d'accélération (par défaut QEasingCurve.InOutQuad)
    - finished_callback : slot appelé à la fin
    """
    _active_animations = {}

    def __init__(self, widget: QWidget, fade_in=True, duration=350, parent=None,
                 easing=QEasingCurve.InOutQuad, finished_callback=None):
        super().__init__(parent)
        self.child_widget = widget
        self._fade_in = fade_in  # <- évite conflit avec méthode fade_in()
        self.duration = duration
        self.easing = easing or QEasingCurve.Linear
        self.finished_callback = finished_callback

        self.child_widget.setParent(self)
        self.child_widget.setGeometry(self.rect())
        self.child_widget.show()

        self._setup()

    def _setup(self):
        old_anim = FadeWidget._active_animations.get(self.child_widget)
        if old_anim:
            old_anim.anim.stop()
            del FadeWidget._active_animations[self.child_widget]

        self.anim = QPropertyAnimation(self.child_widget, b"windowOpacity", self)
        self.anim.setDuration(self.duration)
        self.anim.setEasingCurve(self.easing)
        self.anim.setStartValue(0.0 if self._fade_in else 1.0)
        self.anim.setEndValue(1.0 if self._fade_in else 0.0)
        self.anim.finished.connect(self._on_finished)
        FadeWidget._active_animations[self.child_widget] = self

    def start(self):
        if self._fade_in:
            self.child_widget.setWindowOpacity(0.0)
            self.child_widget.setVisible(True)
        else:
            self.child_widget.setWindowOpacity(1.0)
            self.child_widget.setVisible(True)
        self.anim.start()

    def _on_finished(self):
        if not self._fade_in:
            self.child_widget.setVisible(False)
            self.child_widget.setWindowOpacity(1.0)
        FadeWidget._active_animations.pop(self.child_widget, None)
        if self.finished_callback:
            self.finished_callback()

    @staticmethod
    def fade_in(widget, duration=350, easing=QEasingCurve.InOutQuad, finished_callback=None):
        widget.setVisible(True)  # ← correction pour test
        FadeWidget(widget, fade_in=True, duration=duration, easing=easing, finished_callback=finished_callback).start()

    @staticmethod
    def fade_out(widget, duration=350, easing=QEasingCurve.InOutQuad, finished_callback=None):
        widget.setVisible(True)
        FadeWidget(widget, fade_in=False, duration=duration, easing=easing, finished_callback=finished_callback).start()
