"""
Módulo: main.py
Propósito: Punto de entrada de Libros-Xpress. Integra autenticación, catálogo y carrito.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.2.0 - Sprint 2 (Carrito de compras)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.models.usuario_model import UsuarioModel
from src.views.login_view import LoginView
from src.controllers.auth_controller import AuthController
from src.models.producto_model import ProductoModel
from src.views.catalogo_view import CatalogoView
from src.controllers.catalogo_controller import CatalogoController
from src.models.carrito_model import Carrito, PedidoModel
from src.views.carrito_view import CarritoView
from src.controllers.carrito_controller import CarritoController

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Libros-Xpress")

    # Autenticación
    modelo_usuarios = UsuarioModel("data/database.json")
    vista_login = LoginView()
    auth_ctrl = AuthController(vista_login, modelo_usuarios)
    vista_login.show()
    app.exec()

    if not vista_login.isVisible():
        usuario_actual = getattr(auth_ctrl, 'usuario_actual', 'admin')

        # Carrito y pedidos
        carrito = Carrito()
        pedido_model = PedidoModel("data/pedidos.json")
        vista_carrito = CarritoView()
        carrito_ctrl = CarritoController(vista_carrito, carrito, pedido_model, usuario_actual)

        # Catálogo (con integración del carrito)
        modelo_productos = ProductoModel("data/productos.json")
        vista_catalogo = CatalogoView()
        catalogo_ctrl = CatalogoController(vista_catalogo, modelo_productos, carrito_ctrl)

        vista_catalogo.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()