# ui/widgets/animated_tool_button.py

from PyQt5.QtWidgets import QToolButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, Qt
from PyQt5.QtGui import QPainter

class AnimatedToolButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale = 1.0

        # ✅ Style du texte forcé
        self.setToolButtonStyle(Qt.ToolButtonTextOnly)

        # ✅ Animation hover
        self.anim = QPropertyAnimation(self, b"scale", self)
        self.anim.setDuration(260)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation = self.anim

        # ✅ Style CSS explicite
        self.setStyleSheet("""
            QToolButton {
                background-color: #f2f4fc;
                border-radius: 12px;
                font-size: 16px;
                color: #2c2f4c;
                padding: 8px;
            }
            QToolButton:hover {
                background-color: #ecf0fa;
            }
            QToolButton:pressed {
                background-color: #dbeaff;
            }
        """)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setEndValue(1.12)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setEndValue(1.0)
        self.anim.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.save()
        w, h = self.width(), self.height()
        scale = self._scale
        painter.translate(w / 2, h / 2)
        painter.scale(scale, scale)
        painter.translate(-w / 2, -h / 2)
        super().paintEvent(event)
        painter.restore()

    def getScale(self):
        return self._scale

    def setScale(self, val):
        self._scale = val
        self.update()

    scale = pyqtProperty(float, getScale, setScale)
