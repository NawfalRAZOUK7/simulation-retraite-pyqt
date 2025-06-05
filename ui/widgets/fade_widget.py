# ui/widgets/fade_widget.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, QObject, Qt

class FadeWidget(QObject):
    """
    Animation avancée de fade-in ou fade-out sur n'importe quel QWidget.

    - fade_in=True : lève l'opacité de 0 à 1 (affichage progressif)
    - fade_in=False : baisse de 1 à 0 (disparition)
    - duration : ms (défaut 350)
    - easing : courbe d'accélération (par défaut QEasingCurve.InOutQuad)
    - finished_callback : slot appelé à la fin

    UX avancée :
    - Protège d'une double animation sur le même widget
    - Peut interrompre une animation en cours proprement
    - Supporte une superposition d'effets (fade + autre)
    - Remet le widget visible/invisible selon l'effet
    """
    _active_animations = {}

    def __init__(self, widget: QWidget, fade_in=True, duration=350, parent=None, easing=QEasingCurve.InOutQuad, finished_callback=None):
        super().__init__(parent)
        self.widget = widget
        self.fade_in = fade_in
        self.duration = duration
        self.easing = easing
        self.finished_callback = finished_callback
        self._setup()

    def _setup(self):
        # Nettoie toute animation précédente sur ce widget
        old_anim = FadeWidget._active_animations.get(self.widget)
        if old_anim:
            old_anim.anim.stop()
            del FadeWidget._active_animations[self.widget]

        # Crée l'animation d'opacité
        self.anim = QPropertyAnimation(self.widget, b"windowOpacity", self)
        self.anim.setDuration(self.duration)
        self.anim.setEasingCurve(self.easing)
        self.anim.setStartValue(0.0 if self.fade_in else 1.0)
        self.anim.setEndValue(1.0 if self.fade_in else 0.0)
        self.anim.finished.connect(self._on_finished)
        FadeWidget._active_animations[self.widget] = self

    def start(self):
        # S'assure que le widget est visible (pour fade-in)
        if self.fade_in:
            self.widget.setWindowOpacity(0.0)
            self.widget.setVisible(True)
        else:
            self.widget.setWindowOpacity(1.0)
            self.widget.setVisible(True)
        self.anim.start()

    def _on_finished(self):
        if not self.fade_in:
            self.widget.setVisible(False)
            self.widget.setWindowOpacity(1.0)  # Remet à 1 pour la prochaine fois
        # Libère la référence
        FadeWidget._active_animations.pop(self.widget, None)
        if self.finished_callback:
            self.finished_callback()

    @staticmethod
    def fade_in(widget, duration=350, easing=QEasingCurve.InOutQuad, finished_callback=None):
        FadeWidget(widget, fade_in=True, duration=duration, easing=easing, finished_callback=finished_callback).start()

    @staticmethod
    def fade_out(widget, duration=350, easing=QEasingCurve.InOutQuad, finished_callback=None):
        FadeWidget(widget, fade_in=False, duration=duration, easing=easing, finished_callback=finished_callback).start()
