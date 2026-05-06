"""
Módulo: main.py
Propósito: Punto de entrada de Libros-Xpress. Orquesta autenticación, catálogo, carrito y panel admin.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.3.0 - Sprint 2 completo (Carrito + Panel Admin)
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
from src.views.admin_productos_view import AdminProductosView
from src.controllers.admin_productos_controller import AdminProductosController

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
        # Determinamos el rol de forma simplificada (podría consultarse del modelo)
        rol = "Admin" if usuario_actual == "admin" else "Cliente"

        # Carrito y pedidos
        carrito = Carrito()
        pedido_model = PedidoModel("data/pedidos.json")
        vista_carrito = CarritoView()
        carrito_ctrl = CarritoController(vista_carrito, carrito, pedido_model, usuario_actual)

        # Modelo de productos compartido
        modelo_productos = ProductoModel("data/productos.json")

        # Panel de administración (solo para admin)
        admin_ctrl = None
        if rol == "Admin":
            vista_admin = AdminProductosView()
            admin_ctrl = AdminProductosController(vista_admin, modelo_productos)
            # El refresh_callback se asigna después, cuando tengamos catalogo_ctrl

        # Catálogo (con integración del carrito y panel admin)
        vista_catalogo = CatalogoView()
        catalogo_ctrl = CatalogoController(
            vista_catalogo,
            modelo_productos,
            carrito_ctrl,
            admin_ctrl=admin_ctrl,
            es_admin=(rol == "Admin")
        )

        # Completar el callback de refresco para que el panel admin actualice el catálogo
        if admin_ctrl:
            admin_ctrl.refresh_callback = catalogo_ctrl.mostrar_todos

        vista_catalogo.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()