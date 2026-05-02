"""
Módulo: carrito_controller.py
Propósito: Controlador del carrito de compras y pago para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from PySide6.QtWidgets import QMessageBox
from src.models.carrito_model import Carrito, PedidoModel
from src.views.carrito_view import CarritoView

class CarritoController:
    """
    Controlador que maneja la lógica del carrito y el checkout.
    """

    def __init__(self, vista: CarritoView, carrito: Carrito, pedido_model: PedidoModel, usuario_actual: str):
        """
        Args:
            vista: CarritoView
            carrito: Modelo de carrito en memoria
            pedido_model: Modelo de pedidos (persistencia)
            usuario_actual: Nombre del usuario logueado
        """
        self.vista = vista
        self.carrito = carrito
        self.pedido_model = pedido_model
        self.usuario_actual = usuario_actual
        self._configurar_senales()
        self.actualizar_vista()

    def _configurar_senales(self):
        self.vista.btn_actualizar.clicked.connect(self.actualizar_cantidades)
        self.vista.btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        self.vista.btn_seguir.clicked.connect(self.vista.cerrar)
        self.vista.btn_checkout.clicked.connect(self.mostrar_checkout)
        self.vista.btn_confirmar_pago.clicked.connect(self.procesar_pago)

    def actualizar_vista(self):
        """Carga los items del carrito en la tabla y actualiza totales."""
        self.vista.cargar_items(self.carrito.items)
        self.vista.actualizar_totales(self.carrito.total(),
                                    self.carrito.impuesto(),
                                    self.carrito.total_con_impuesto())

    def actualizar_cantidades(self):
        """Aplica las cantidades ingresadas en los spinboxes al carrito."""
        cantidades = self.vista.obtener_cantidades_actualizadas()
        for titulo, cantidad in cantidades.items():
            self.carrito.actualizar_cantidad(titulo, cantidad)
        self.actualizar_vista()
        self.vista.mostrar_mensaje("Actualizado", "Cantidades actualizadas.")

    def eliminar_seleccionado(self):
        """Elimina el producto seleccionado del carrito."""
        titulo = self.vista.obtener_producto_seleccionado()
        if titulo:
            self.carrito.eliminar_item(titulo)
            self.actualizar_vista()
            self.vista.mostrar_mensaje("Eliminado", f"'{titulo}' retirado del carrito.")
        else:
            self.vista.mostrar_error("Seleccione un producto", "Debe seleccionar un producto para eliminar.")

    def mostrar_checkout(self):
        """Muestra la sección de pago si el carrito no está vacío."""
        if self.carrito.esta_vacio():
            self.vista.mostrar_error("Carrito vacío", "No hay productos para comprar.")
            return
        self.vista.mostrar_seccion_pago(True)

    def procesar_pago(self):
        """Valida los datos de pago y simula la transacción."""
        titular, numero = self.vista.obtener_datos_pago()
        if not titular or not numero:
            self.vista.mostrar_error("Datos incompletos", "Debe ingresar titular y número de tarjeta.")
            return
        # Simulación: se acepta cualquier número con al menos 4 dígitos
        if len(numero) < 4:
            self.vista.mostrar_error("Tarjeta inválida", "Número de tarjeta no válido.")
            return

        try:
            pedido = self.pedido_model.crear_pedido(self.usuario_actual, self.carrito)
            self.vista.mostrar_mensaje("Compra exitosa",
                                    f"Pedido #{pedido['id']} confirmado.\nTotal: ${pedido['total']:.2f}")
            self.carrito.vaciar()
            self.actualizar_vista()
            self.vista.mostrar_seccion_pago(False)
            self.vista.limpiar_pago()
        except (ValueError, IOError) as e:
            self.vista.mostrar_error("Error al procesar", str(e))

    def agregar_al_carrito(self, titulo: str, precio: float):
        """Método para ser llamado desde el catálogo."""
        self.carrito.agregar_item(titulo, precio)
        self.vista.mostrar_mensaje("Agregado", f"'{titulo}' añadido al carrito.")
        self.actualizar_vista()

# --- Prueba del controlador (simulación) ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    import tempfile, json, os

    # Arrange
    # Crear pedidos.json temporal
    datos_pedidos = {"pedidos": []}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_pedidos, tmp)
        ruta_pedidos = tmp.name

    app = QApplication(sys.argv)
    carrito = Carrito()
    pedido_model = PedidoModel(ruta_pedidos)
    vista = CarritoView()
    usuario = "test_user"
    controlador = CarritoController(vista, carrito, pedido_model, usuario)

    # Act - agregar productos
    controlador.agregar_al_carrito("Libro X", 25.0)
    controlador.agregar_al_carrito("Libro Y", 15.0)

    # Verificar que la tabla se llenó
    assert vista.tabla.rowCount() == 2, "Debería haber 2 filas en la tabla"
    # Verificar totales
    assert carrito.total() == 40.0
    assert carrito.total_con_impuesto() == 45.2

    # Simular checkout (mostrar sección de pago)
    vista.btn_checkout.click()
    assert vista.grupo_pago.isVisible(), "La sección de pago debe estar visible"

    # Simular datos de pago y confirmar
    vista.txt_titular.setText("Juan Pérez")
    vista.txt_numero.setText("1234567890123456")
    vista.btn_confirmar_pago.click()

    # Assert: el carrito está vacío después del pago exitoso
    assert carrito.esta_vacio(), "El carrito debe quedar vacío tras el pago"
    assert len(pedido_model.pedidos) == 1, "Debe haberse creado un pedido"

    # Limpiar archivo temporal
    os.unlink(ruta_pedidos)
    print("✅ Prueba del controlador de carrito pasó correctamente.")
    app.quit()