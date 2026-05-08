"""
Módulo: venta_fisica_controller.py
Propósito: Controlador para registrar ventas físicas y sincronizar stock.
Autor: [Robert Cerón, David Solís, Juan Castro]
Versión: 1.0.0 - Sprint 4
"""

import sys
import os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication
from src.models.producto_model import ProductoModel
from src.models.carrito_model import PedidoModel
from src.views.venta_fisica_view import VentaFisicaView

class VentaFisicaController:
    """Controlador para gestionar ventas físicas."""

    def __init__(self, vista: VentaFisicaView, modelo_productos: ProductoModel,
                pedido_model: PedidoModel, usuario_actual: str, refresh_callback=None):
        self.vista = vista
        self.modelo_productos = modelo_productos
        self.pedido_model = pedido_model
        self.usuario_actual = usuario_actual
        self.refresh_callback = refresh_callback
        self._configurar_senales()
        self.cargar_productos()

    def _configurar_senales(self):
        self.vista.btn_registrar.clicked.connect(self.registrar_venta)

    def cargar_productos(self):
        self.vista.cargar_productos(self.modelo_productos.productos)

    def registrar_venta(self):
        id_producto = self.vista.obtener_producto_seleccionado_id()
        cantidad = self.vista.obtener_cantidad()

        if id_producto is None:
            self.vista.mostrar_error("Error", "Seleccione un producto válido.")
            return

        # Verificar stock
        producto = next((p for p in self.modelo_productos.productos if p.id == id_producto), None)
        if not producto:
            self.vista.mostrar_error("Error", "Producto no encontrado.")
            return
        if producto.stock < cantidad:
            self.vista.mostrar_error("Stock insuficiente",
                                    f"Solo hay {producto.stock} unidades disponibles.")
            return

        # Reducir stock
        ok = self.modelo_productos.reducir_stock(id_producto, cantidad)
        if not ok:
            self.vista.mostrar_error("Error", "No se pudo reducir el stock.")
            return

        # Registrar pedido como venta física
        from src.models.carrito_model import Carrito
        carrito_temp = Carrito()
        carrito_temp.agregar_item(producto.titulo, producto.precio, cantidad)
        pedido = self.pedido_model.crear_pedido(self.usuario_actual, carrito_temp)
        # Marcar como venta física (sobrescribimos estado)
        pedido['estado'] = "Venta Física"
        self.pedido_model.guardar_pedidos()

        self.vista.mostrar_mensaje("Venta registrada",
                                f"Venta de {cantidad} x '{producto.titulo}' registrada.\nPedido #{pedido['id']}")
        self.cargar_productos()
        if self.refresh_callback:
            self.refresh_callback()


# --- Prueba simulada ---
if __name__ == "__main__":
    import tempfile, json

    app = QApplication(sys.argv)

    # Arrange
    datos_productos = {"productos": [{"id": 1, "titulo": "Libro A", "autor": "A", "categoria": "C", "precio": 10.0, "portada": "", "stock": 5}]}
    datos_pedidos = {"pedidos": []}

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_productos, tmp)
        ruta_prod = tmp.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_pedidos, tmp)
        ruta_pedidos = tmp.name

    modelo_prod = ProductoModel(ruta_prod)
    pedido_model = PedidoModel(ruta_pedidos)
    vista = VentaFisicaView()
    vista.show()
    vista.mostrar_mensaje = lambda t, m: print(f"ℹ️ {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"❌ {t}: {m}")

    controlador = VentaFisicaController(vista, modelo_prod, pedido_model, "admin")
    app.processEvents()

    # Act - simular selección y venta
    vista.cmb_producto.setCurrentIndex(0)
    vista.spin_cantidad.setValue(2)
    vista.btn_registrar.clicked.emit()
    app.processEvents()

    # Assert
    assert modelo_prod.productos[0].stock == 3, "El stock debió reducirse a 3"
    assert len(pedido_model.pedidos) == 1
    assert pedido_model.pedidos[0]['estado'] == "Venta Física"
    print("✅ Prueba del controlador de venta física pasó correctamente.")

    os.unlink(ruta_prod)
    os.unlink(ruta_pedidos)
    vista.close()
    app.quit()
    sys.exit()