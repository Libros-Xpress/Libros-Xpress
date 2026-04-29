"""
Módulo: main.py
Propósito: Punto de entrada de la aplicación Libros-Xpress. Inicializa el entorno MVC y ejecuta el catálogo.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0 (Sprint 1 - Catálogo)
"""

import sys
from PySide6.QtWidgets import QApplication
from src.models.producto_model import ProductoModel
from src.views.catalogo_view import CatalogoView
from src.controllers.catalogo_controller import CatalogoController

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Libros-Xpress")

    # Inicialización MVC para el catálogo
    modelo = ProductoModel("data/productos.json")
    vista = CatalogoView()
    controlador = CatalogoController(vista, modelo)

    vista.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()