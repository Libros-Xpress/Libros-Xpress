"""
Módulo: historial_controller.py
Propósito: Controlador para el historial de pedidos del usuario.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

import sys
import os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication
from src.models.carrito_model import PedidoModel
from src.views.historial_view import HistorialView

class HistorialController:
    """Controlador para mostrar el historial de pedidos."""

    def __init__(self, vista: HistorialView, pedido_model: PedidoModel):
        """
        Args:
            vista: HistorialView
            pedido_model: PedidoModel (compartido)
        """
        self.vista = vista
        self.pedido_model = pedido_model

    def cargar_historial(self, usuario: str):
        """Carga los pedidos del usuario en la vista."""
        pedidos = self.pedido_model.obtener_pedidos_cliente(usuario)
        self.vista.cargar_historial(pedidos)
        if not pedidos:
            self.vista.mostrar_mensaje("Sin pedidos", "No tienes pedidos registrados.")


# --- Prueba simulada ---
if __name__ == "__main__":
    import tempfile, json
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Arrange: crear pedidos.json temporal con datos
    datos = {"pedidos": [
        {"id": 1, "fecha": "2026-05-01", "cliente": "test", "total": 45.2, "estado": "Pendiente"},
        {"id": 2, "fecha": "2026-05-02", "cliente": "test", "total": 30.0, "estado": "Enviado"}
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

    controlador = HistorialController(vista, pedido_model)
    controlador.cargar_historial("test")
    app.processEvents()

    # Assert: la tabla debe tener 2 filas
    assert vista.tabla.rowCount() == 2, "Debería haber 2 pedidos"
    print("✅ Prueba del controlador de historial pasó correctamente.")

    os.unlink(ruta_tmp)
    vista.close()
    app.quit()
    sys.exit()