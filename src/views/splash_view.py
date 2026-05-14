"""
Módulo: splash_view.py
Propósito: Pantalla de bienvenida (Splash Screen) para Libros/Xpress con logo corporativo.
Autor: Robert Cerón
Versión: 2.0.1
"""

import sys, os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QSplashScreen, QApplication
from PySide6.QtCore import Qt, QTimer, QRect, QEventLoop
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QLinearGradient

class SplashView(QSplashScreen):
    """Ventana de presentación inicial del software."""

    def __init__(self):
        pixmap = QPixmap(600, 420)
        pixmap.fill(QColor("#FFF8F0"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Degradado superior
        gradient = QLinearGradient(0, 0, 0, 420)
        gradient.setColorAt(0.0, QColor("#D4A574"))
        gradient.setColorAt(0.3, QColor("#FFF8F0"))
        painter.fillRect(0, 0, 600, 420, gradient)

        # Marcos decorativos
        pen = QPen(QColor("#8B5E3C"), 2)
        painter.setPen(pen)
        painter.drawRoundedRect(20, 20, 560, 380, 20, 20)
        painter.drawRoundedRect(28, 28, 544, 364, 15, 15)

        # --- LOGO ---
        logo_path = os.path.join("assets", "img", "LOGO-LIBROSXPRESS.png")
        if os.path.exists(logo_path):
            logo = QPixmap(logo_path)
            logo = logo.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(480, 300, logo)

        # 1. Nombre de la empresa
        painter.setFont(QFont("Segoe UI", 22, QFont.Bold))
        painter.setPen(QColor("#8B5E3C"))
        painter.drawText(QRect(0, 100, 600, 40), Qt.AlignHCenter, "DIGITAL-SHIFT")

        # 2. Nombre del software
        painter.setFont(QFont("Segoe UI", 38, QFont.Bold))
        painter.setPen(QColor("#6B3A2A"))
        painter.drawText(QRect(0, 160, 600, 60), Qt.AlignHCenter, "LIBROS/XPRESS")

        # 3. Eslogan
        painter.setFont(QFont("Segoe UI", 13, QFont.Light))
        painter.setPen(QColor("#8B5E3C"))
        painter.drawText(QRect(0, 230, 600, 30), Qt.AlignHCenter, "From physical to digital")

        # 4. Línea separadora
        painter.setPen(QPen(QColor("#D4A574"), 1))
        painter.drawLine(150, 270, 450, 270)

        # 5. Versión y autores
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor("#5D4037"))
        painter.drawText(QRect(0, 290, 600, 25), Qt.AlignHCenter, "v2.0.1 - Digital Shift 2026")
        painter.drawText(QRect(0, 320, 600, 25), Qt.AlignHCenter, "Robert Cerón - David Solís - Juan Castro")

        painter.end()
        super().__init__(pixmap)

    def mostrar(self, duracion_ms=3000):
        self.show()
        QTimer.singleShot(duracion_ms, self.close)

    def esperar_cierre(self):
        loop = QEventLoop()
        self.destroyed.connect(loop.quit)
        QTimer.singleShot(5000, loop.quit)
        self.show()
        QTimer.singleShot(4000, self.close)
        loop.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashView()
    splash.mostrar(3000)
    app.exec()