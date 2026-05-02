"""
Módulo: main.py
Propósito: Punto de entrada de la aplicación Libros-Xpress. Gestiona autenticación y catálogo.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.1.0 - Sprint 1 completo (Catálogo + Autenticación)
"""

import sys
import os
# Ajuste de path para importaciones absolutas
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.models.usuario_model import UsuarioModel
from src.views.login_view import LoginView
from src.controllers.auth_controller import AuthController
from src.models.producto_model import ProductoModel
from src.views.catalogo_view import CatalogoView
from src.controllers.catalogo_controller import CatalogoController

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Libros-Xpress")

    # --- Flujo de autenticación ---
    modelo_usuarios = UsuarioModel("data/database.json")
    vista_login = LoginView()
    controlador_auth = AuthController(vista_login, modelo_usuarios)

    # Mostrar ventana de login (modal: detiene la ejecución hasta que se cierre)
    vista_login.show()
    app.exec()  # Necesario para que la ventana se procese y se cierre tras login exitoso

    # Si la ventana de login se cerró (porque el login fue exitoso), continuamos
    # Nota: el cierre se realiza en auth_controller.iniciar_sesion() con vista.cerrar_ventana()
    # Si no se cerró, el usuario cerró manualmente -> salimos
    if not vista_login.isVisible():
        # Inicializar catálogo
        modelo_productos = ProductoModel("data/productos.json")
        vista_catalogo = CatalogoView()
        controlador_catalogo = CatalogoController(vista_catalogo, modelo_productos)
        vista_catalogo.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()