"""
Módulo: historial_controller.py
Propósito: Controlador para el historial de pedidos del usuario y descarga de facturas.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.1.0 - Sprint 4 (Descarga de facturas)
"""

import sys
import os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication
from src.models.carrito_model import PedidoModel
from src.models.factura_model import FacturaModel
from src.views.historial_view import HistorialView

class HistorialController:
    """Controlador para mostrar el historial de pedidos y descargar facturas."""

    def __init__(self, vista: HistorialView, pedido_model: PedidoModel, factura_model: FacturaModel = None):
        """
        Args:
            vista: HistorialView
            pedido_model: PedidoModel (compartido)
            factura_model: FacturaModel (para generar PDFs)
        """
        self.vista = vista
        self.pedido_model = pedido_model
        self.factura_model = factura_model if factura_model else FacturaModel()
        self._configurar_senales()

    def _configurar_senales(self):
        """Conecta el botón de descarga de factura."""
        if hasattr(self.vista, 'btn_descargar_factura'):
            self.vista.btn_descargar_factura.clicked.connect(self.descargar_factura)

    def cargar_historial(self, usuario: str):
        """Carga los pedidos del usuario en la vista."""
        pedidos = self.pedido_model.obtener_pedidos_cliente(usuario)
        self.vista.cargar_historial(pedidos)
        if not pedidos:
            self.vista.mostrar_mensaje("Sin pedidos", "No tienes pedidos registrados.")

    def descargar_factura(self):
        """Genera y guarda la factura en PDF del pedido seleccionado."""
        seleccion = self.vista.obtener_pedido_seleccionado()
        if not seleccion:
            self.vista.mostrar_error("Seleccione un pedido", "Debe seleccionar un pedido para descargar su factura.")
            return

        # Obtener el pedido completo desde el modelo (incluye items, descuento, etc.)
        pedido_completo = None
        for p in self.pedido_model.pedidos:
            if p['id'] == seleccion['id']:
                pedido_completo = p
                break

        if not pedido_completo:
            self.vista.mostrar_error("Error", "No se encontró el pedido completo en los datos.")
            return

        try:
            ruta_pdf = self.factura_model.generar_factura_pdf(pedido_completo)
            self.vista.mostrar_mensaje("Factura generada",
                                       f"La factura se ha guardado correctamente en:\n{ruta_pdf}")
        except Exception as e:
            self.vista.mostrar_error("Error al generar factura", str(e))


# --- Prueba simulada (con descarga de factura) ---
if __name__ == "__main__":
    import tempfile, json
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Arrange: crear pedidos.json temporal con datos
    datos = {"pedidos": [
        {"id": 1, "fecha": "2026-05-01", "cliente": "test", "total": 45.2, "estado": "Pendiente", "items": [{"titulo": "Libro X", "cantidad": 2, "precio_unitario": 20.0}], "descuento": 0.0},
        {"id": 2, "fecha": "2026-05-02", "cliente": "test", "total": 30.0, "estado": "Enviado", "items": [{"titulo": "Libro Y", "cantidad": 1, "precio_unitario": 30.0}], "descuento": 0.0}
    ]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    pedido_model = PedidoModel(ruta_tmp)
    vista = HistorialView()
    vista.show()
    # Mock de mensajes
    vista.mostrar_mensaje = lambda t, m: print(f"ℹ️ {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"❌ {t}: {m}")

    # Mock de FacturaModel para evitar generar PDF real en la prueba
    class MockFacturaModel:
        def generar_factura_pdf(self, pedido):
            return f"facturas/factura_{pedido['id']}.pdf"

    factura_model = MockFacturaModel()

    controlador = HistorialController(vista, pedido_model, factura_model)
    controlador.cargar_historial("test")
    app.processEvents()

    # Assert: la tabla debe tener 2 filas
    assert vista.tabla.rowCount() == 2, "Debería haber 2 pedidos"
    print("✅ Prueba del controlador de historial pasó correctamente.")

    os.unlink(ruta_tmp)
    vista.close()
    app.quit()
    sys.exit()