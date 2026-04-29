"""
Módulo: main.py
Propósito: Punto de entrada de la aplicación Libros-Xpress. Ajusta el path para importaciones absolutas.
"""
import sys
import os
# Agrega la raíz del proyecto al PYTHONPATH para permitir imports desde src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.models.producto_model import ProductoModel
from src.views.catalogo_view import CatalogoView
from src.controllers.catalogo_controller import CatalogoController

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Libros-Xpress")

    modelo = ProductoModel("data/productos.json")
    vista = CatalogoView()
    controlador = CatalogoController(vista, modelo)

    vista.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()