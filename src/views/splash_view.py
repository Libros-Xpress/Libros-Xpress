"""
Módulo: splash_view.py
Propósito: Pantalla de bienvenida (Splash Screen) para Libros/Xpress.
Autor: David Solís
Versión: 2.0.0
"""

from PySide6.QtWidgets import QSplashScreen
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QLinearGradient

class SplashView(QSplashScreen):
    """Ventana de presentación inicial del software."""

    def __init__(self):
        # Crear un pixmap con el fondo y los textos
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor("#FFF8F0"))  # Fondo crema

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Degradado superior
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor("#D4A574"))
        gradient.setColorAt(0.3, QColor("#FFF8F0"))
        painter.fillRect(0, 0, 600, 400, gradient)

        # Marcos decorativos
        pen = QPen(QColor("#8B5E3C"), 2)
        painter.setPen(pen)
        painter.drawRoundedRect(20, 20, 560, 360, 20, 20)
        painter.drawRoundedRect(28, 28, 544, 344, 15, 15)

        # ---- Distribución manual de textos (evita amontonamiento) ----

        # 1. Nombre de la empresa (parte superior)
        painter.setFont(QFont("Segoe UI", 22, QFont.Bold))
        painter.setPen(QColor("#8B5E3C"))
        painter.drawText(QRect(0, 60, 600, 40), Qt.AlignHCenter, "DIGITAL-SHIFT")

        # 2. Nombre del software (centro, grande)
        painter.setFont(QFont("Segoe UI", 38, QFont.Bold))
        painter.setPen(QColor("#6B3A2A"))
        painter.drawText(QRect(0, 140, 600, 60), Qt.AlignHCenter, "LIBROS/XPRESS")

        # 3. Eslogan (justo debajo del nombre)
        painter.setFont(QFont("Segoe UI", 13, QFont.Light))
        painter.setPen(QColor("#8B5E3C"))
        painter.drawText(QRect(0, 210, 600, 30), Qt.AlignHCenter, "From physical to digital")

        # 4. Línea separadora sutil
        painter.setPen(QPen(QColor("#D4A574"), 1))
        painter.drawLine(150, 260, 450, 260)

        # 5. Versión y autores (parte inferior, bien espaciados)
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor("#5D4037"))
        painter.drawText(QRect(0, 280, 600, 25), Qt.AlignHCenter, "v2.0.0 - Digital Shift 2026")
        painter.drawText(QRect(0, 310, 600, 25), Qt.AlignHCenter, "Robert Cerón - David Solís - Juan Castro")

        painter.end()
        super().__init__(pixmap)

    def mostrar(self, duracion_ms=3000):
        """Muestra el splash y lo cierra automáticamente después de la duración indicada."""
        self.show()
        QTimer.singleShot(duracion_ms, self.close)


# --- Prueba visual de la vista ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    splash = SplashView()
    splash.mostrar(5000)
    app.exec()