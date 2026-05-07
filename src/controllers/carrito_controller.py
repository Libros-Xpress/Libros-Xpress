"""
Módulo: carrito_controller.py
Propósito: Controlador del carrito de compras, pago y aplicación de cupones para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.3.0 - Sprint 3 (Cupones de descuento)
"""

import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication
from src.models.carrito_model import Carrito, PedidoModel
from src.models.cupon_model import CuponModel
from src.views.carrito_view import CarritoView

class CarritoController:
    """
    Controlador que maneja la lógica del carrito, el checkout y los cupones de descuento.
    """

    def __init__(self, vista: CarritoView, carrito: Carrito, pedido_model: PedidoModel,
                usuario_actual: str, cupon_model: CuponModel = None):
        self.vista = vista
        self.carrito = carrito
        self.pedido_model = pedido_model
        self.usuario_actual = usuario_actual
        self.cupon_model = cupon_model if cupon_model else CuponModel()
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
            pedido = self.pedido_model.crear_pedido(self.usuario_actual, self.carrito, descuento=self.descuento_aplicado)
            total_final = pedido['total']  # Ya incluye el descuento, si el modelo lo aplica
            self.vista.mostrar_mensaje("Compra exitosa",
                                    f"Pedido #{pedido['id']} confirmado.\nTotal: ${total_final:.2f}")
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


# --- Prueba del controlador (simulación con cupón) ---
if __name__ == "__main__":
    import tempfile, json

    # Arrange
    datos_pedidos = {"pedidos": []}
    datos_cupones = {"cupones": [{"codigo": "DESC10", "tipo": "porcentaje", "valor": 10, "activo": True}]}

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_pedidos, tmp)
        ruta_pedidos = tmp.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_cupones, tmp)
        ruta_cupones = tmp.name

    app = QApplication(sys.argv)
    carrito = Carrito()
    pedido_model = PedidoModel(ruta_pedidos)
    cupon_model = CuponModel(ruta_cupones)
    vista = CarritoView()
    vista.show()

    vista.mostrar_mensaje = lambda t, m: print(f"ℹ️ {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"❌ {t}: {m}")

    usuario = "test_user"
    controlador = CarritoController(vista, carrito, pedido_model, usuario, cupon_model)

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

    vista.txt_titular.setText("Juan Pérez")
    vista.txt_numero.setText("1234567890123456")
    vista.btn_confirmar_pago.clicked.emit()
    app.processEvents()

    # Assert
    assert carrito.esta_vacio(), "El carrito debe quedar vacío tras el pago"
    assert len(pedido_model.pedidos) == 1, "Debe haberse creado un pedido"
    # Verificar que el pedido guardó descuento (si se implementó en el modelo)
    if 'descuento' in pedido_model.pedidos[0]:
        print(f"Descuento guardado en pedido: {pedido_model.pedidos[0]['descuento']}")

    os.unlink(ruta_pedidos)
    os.unlink(ruta_cupones)
    print("✅ Prueba del controlador de carrito con cupón pasó correctamente.")
    vista.close()
    app.quit()
    sys.exit()