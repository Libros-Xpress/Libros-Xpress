"""
Módulo: carrito_controller.py
Propósito: Controlador del carrito de compras, pago, cupones y sincronización de stock.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.4.0 - Sprint 4 (Stock + Facturación)
"""

import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication
from src.models.carrito_model import Carrito, PedidoModel
from src.models.cupon_model import CuponModel
from src.models.producto_model import ProductoModel
from src.models.factura_model import FacturaModel
from src.views.carrito_view import CarritoView

class CarritoController:
    """
    Controlador que maneja la lógica del carrito, el checkout, los cupones y la sincronización de stock.
    """

    def __init__(self, vista: CarritoView, carrito: Carrito, pedido_model: PedidoModel,
                 usuario_actual: str, cupon_model: CuponModel = None,
                 modelo_productos: ProductoModel = None, factura_model: FacturaModel = None):
        self.vista = vista
        self.carrito = carrito
        self.pedido_model = pedido_model
        self.usuario_actual = usuario_actual
        self.cupon_model = cupon_model if cupon_model else CuponModel()
        self.modelo_productos = modelo_productos      # Para reducir stock
        self.factura_model = factura_model if factura_model else FacturaModel()
        self.descuento_aplicado = 0.0
        self.cupon_aplicado = None
        self._configurar_senales()
        self.actualizar_vista()

    def _configurar_senales(self):
        self.vista.btn_actualizar.clicked.connect(self.actualizar_cantidades)
        self.vista.btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        self.vista.btn_seguir.clicked.connect(self.vista.cerrar)
        self.vista.btn_checkout.clicked.connect(self.mostrar_checkout)
        self.vista.btn_confirmar_pago.clicked.connect(self.procesar_pago)
        self.vista.btn_aplicar_cupon.clicked.connect(self.aplicar_cupon)

    def actualizar_vista(self):
        self.vista.cargar_items(self.carrito.items)
        subtotal = self.carrito.total()
        impuesto = self.carrito.impuesto()
        total_con_impuesto = self.carrito.total_con_impuesto()
        total_final = max(0, total_con_impuesto - self.descuento_aplicado)
        self.vista.actualizar_totales(subtotal, impuesto, total_final, self.descuento_aplicado)

    def actualizar_cantidades(self):
        cantidades = self.vista.obtener_cantidades_actualizadas()
        for titulo, cantidad in cantidades.items():
            self.carrito.actualizar_cantidad(titulo, cantidad)
        self.actualizar_vista()
        self.vista.mostrar_mensaje("Actualizado", "Cantidades actualizadas.")

    def eliminar_seleccionado(self):
        titulo = self.vista.obtener_producto_seleccionado()
        if titulo:
            self.carrito.eliminar_item(titulo)
            self.actualizar_vista()
            self.vista.mostrar_mensaje("Eliminado", f"'{titulo}' retirado del carrito.")
        else:
            self.vista.mostrar_error("Seleccione un producto", "Debe seleccionar un producto para eliminar.")

    def mostrar_checkout(self):
        if self.carrito.esta_vacio():
            self.vista.mostrar_error("Carrito vacío", "No hay productos para comprar.")
            return
        self.vista.mostrar_seccion_pago(True)

    def aplicar_cupon(self):
        codigo = self.vista.obtener_codigo_cupon()
        if not codigo:
            self.vista.mostrar_error("Código vacío", "Ingresa un código promocional.")
            return

        cupon = self.cupon_model.validar_cupon(codigo)
        if not cupon:
            self.vista.mostrar_error("Cupón inválido", "El código ingresado no es válido o ha caducado.")
            return

        total_antes = self.carrito.total_con_impuesto()
        total_despues = self.cupon_model.aplicar_descuento(cupon, total_antes)
        self.descuento_aplicado = total_antes - total_despues
        self.cupon_aplicado = cupon

        self.actualizar_vista()
        self.vista.mostrar_mensaje("Cupón aplicado",
                                   f"Descuento de ${self.descuento_aplicado:.2f} aplicado. Total: ${total_despues:.2f}")

    def procesar_pago(self):
        titular, numero = self.vista.obtener_datos_pago()
        if not titular or not numero:
            self.vista.mostrar_error("Datos incompletos", "Debe ingresar titular y número de tarjeta.")
            return
        if len(numero) < 4:
            self.vista.mostrar_error("Tarjeta inválida", "Número de tarjeta no válido.")
            return

        try:
            # Crear pedido
            pedido = self.pedido_model.crear_pedido(self.usuario_actual, self.carrito, descuento=self.descuento_aplicado)
            total_final = pedido['total']

            # Reducir stock (HU7) si está disponible el modelo de productos
            if self.modelo_productos:
                for item in self.carrito.items:
                    producto = next((p for p in self.modelo_productos.productos if p.titulo == item.titulo), None)
                    if producto:
                        self.modelo_productos.reducir_stock(producto.id, item.cantidad)

            # Generar factura (HU8)
            ruta_factura = self.factura_model.generar_factura_pdf(pedido)

            self.vista.mostrar_mensaje("Compra exitosa",
                                       f"Pedido #{pedido['id']} confirmado.\n"
                                       f"Total: ${total_final:.2f}\n"
                                       f"Factura guardada en:\n{ruta_factura}")
            self.carrito.vaciar()
            self.descuento_aplicado = 0.0
            self.cupon_aplicado = None
            self.actualizar_vista()
            self.vista.mostrar_seccion_pago(False)
            self.vista.limpiar_pago()
        except (ValueError, IOError) as e:
            self.vista.mostrar_error("Error al procesar", str(e))

    def agregar_al_carrito(self, titulo: str, precio: float):
        self.carrito.agregar_item(titulo, precio)
        self.vista.mostrar_mensaje("Agregado", f"'{titulo}' añadido al carrito.")
        self.actualizar_vista()


# --- Prueba del controlador (simulación con cupón, stock y factura) ---
if __name__ == "__main__":
    import tempfile, json

    # Arrange
    datos_pedidos = {"pedidos": []}
    datos_cupones = {"cupones": [{"codigo": "DESC10", "tipo": "porcentaje", "valor": 10, "activo": True}]}
    datos_productos = {"productos": [
        {"id": 1, "titulo": "Libro X", "autor": "A", "categoria": "C", "precio": 25.0, "portada": "", "stock": 10},
        {"id": 2, "titulo": "Libro Y", "autor": "B", "categoria": "D", "precio": 15.0, "portada": "", "stock": 5}
    ]}

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_pedidos, tmp)
        ruta_pedidos = tmp.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_cupones, tmp)
        ruta_cupones = tmp.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_productos, tmp)
        ruta_productos = tmp.name

    app = QApplication(sys.argv)
    carrito = Carrito()
    pedido_model = PedidoModel(ruta_pedidos)
    cupon_model = CuponModel(ruta_cupones)
    modelo_productos = ProductoModel(ruta_productos)
    # Mock de factura
    class MockFacturaModel:
        def generar_factura_pdf(self, pedido):
            return f"facturas/factura_{pedido['id']}.pdf"
    factura_model = MockFacturaModel()

    vista = CarritoView()
    vista.show()

    vista.mostrar_mensaje = lambda t, m: print(f"ℹ️ {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"❌ {t}: {m}")

    usuario = "test_user"
    controlador = CarritoController(vista, carrito, pedido_model, usuario, cupon_model,
                                    modelo_productos=modelo_productos, factura_model=factura_model)

    # Act - agregar productos
    controlador.agregar_al_carrito("Libro X", 25.0)
    controlador.agregar_al_carrito("Libro Y", 15.0)

    assert vista.tabla.rowCount() == 2, "Debería haber 2 filas en la tabla"
    assert carrito.total() == 40.0
    assert carrito.total_con_impuesto() == 45.2

    # Aplicar cupón
    vista.txt_cupon.setText("DESC10")
    controlador.aplicar_cupon()
    assert abs(controlador.descuento_aplicado - 4.52) < 0.01, "El descuento debería ser 4.52"

    # Checkout y pago
    vista.btn_checkout.clicked.emit()
    app.processEvents()
    assert vista.grupo_pago.isVisible(), "La sección de pago debe estar visible"

    # Verificar stock antes del pago
    stock_inicial_x = modelo_productos.productos[0].stock
    stock_inicial_y = modelo_productos.productos[1].stock

    vista.txt_titular.setText("Juan Pérez")
    vista.txt_numero.setText("1234567890123456")
    vista.btn_confirmar_pago.clicked.emit()
    app.processEvents()

    # Assert
    assert carrito.esta_vacio(), "El carrito debe quedar vacío tras el pago"
    assert len(pedido_model.pedidos) == 1, "Debe haberse creado un pedido"
    # Verificar que el stock se redujo
    assert modelo_productos.productos[0].stock == stock_inicial_x - 1, "El stock de Libro X debió reducirse en 1"
    assert modelo_productos.productos[1].stock == stock_inicial_y - 1, "El stock de Libro Y debió reducirse en 1"

    os.unlink(ruta_pedidos)
    os.unlink(ruta_cupones)
    os.unlink(ruta_productos)
    print("✅ Prueba del controlador de carrito con stock y factura pasó correctamente.")
    vista.close()
    app.quit()
    sys.exit()