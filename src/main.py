"""
Módulo: main.py
Propósito: Punto de entrada de Libros/Xpress con Splash Screen.
Versión: 2.0.0 - Fase 1 (Splash Screen)
Autor: David Solís
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.views.splash_view import SplashView
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
from src.models.cupon_model import CuponModel
from src.views.historial_view import HistorialView
from src.controllers.historial_controller import HistorialController
from src.models.factura_model import FacturaModel
from src.views.venta_fisica_view import VentaFisicaView
from src.controllers.venta_fisica_controller import VentaFisicaController

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Libros/Xpress")

    # --- Splash Screen ---
    splash = SplashView()
    splash.esperar_cierre()      # Espera 3 segundos y se cierra solo

    # Autenticación
    modelo_usuarios = UsuarioModel("data/database.json")
    vista_login = LoginView()
    auth_ctrl = AuthController(vista_login, modelo_usuarios)
    vista_login.show()
    app.exec()

    if not vista_login.isVisible():
        usuario_actual = getattr(auth_ctrl, 'usuario_actual', 'admin')
        rol = "Admin" if usuario_actual == "admin" else "Cliente"

        cupon_model = CuponModel("data/cupones.json")
        carrito = Carrito()
        pedido_model = PedidoModel("data/pedidos.json")
        modelo_productos = ProductoModel("data/productos.json")
        factura_model = FacturaModel("facturas")

        vista_carrito = CarritoView()
        carrito_ctrl = CarritoController(
            vista_carrito, carrito, pedido_model, usuario_actual, cupon_model,
            modelo_productos=modelo_productos, factura_model=factura_model
        )

        admin_ctrl = None
        if rol == "Admin":
            vista_admin = AdminProductosView()
            admin_ctrl = AdminProductosController(vista_admin, modelo_productos)

        vista_historial = HistorialView()
        historial_ctrl = HistorialController(vista_historial, pedido_model, factura_model)

        venta_fisica_ctrl = None
        if rol == "Admin":
            vista_venta_fisica = VentaFisicaView()
            venta_fisica_ctrl = VentaFisicaController(
                vista_venta_fisica, modelo_productos, pedido_model, usuario_actual
            )

        vista_catalogo = CatalogoView()
        catalogo_ctrl = CatalogoController(
            vista_catalogo, modelo_productos, carrito_ctrl,
            admin_ctrl=admin_ctrl, es_admin=(rol == "Admin"),
            usuario_actual=usuario_actual, historial_ctrl=historial_ctrl,
            venta_fisica_ctrl=venta_fisica_ctrl
        )

        if admin_ctrl:
            admin_ctrl.refresh_callback = catalogo_ctrl.mostrar_todos
        if venta_fisica_ctrl:
            venta_fisica_ctrl.refresh_callback = catalogo_ctrl.mostrar_todos

        vista_catalogo.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()