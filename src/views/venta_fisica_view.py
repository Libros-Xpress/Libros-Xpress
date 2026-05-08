"""
Módulo: venta_fisica_view.py
Propósito: Interfaz gráfica para registrar ventas físicas y sincronizar el stock.
Autor: [Robert Cerón, David Solís, Juan Castro]
Versión: 1.0.0 - Sprint 4
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

class VentaFisicaView(QMainWindow):
    """Ventana para registrar una venta en tienda física."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Venta Física - Libros-Xpress")
        self.setFixedSize(400, 250)
        self._configurar_ui()
        self._centrar_en_pantalla()

    def _centrar_en_pantalla(self):
        centro = self.screen().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centro)
        self.move(frame.topLeft())

    def _configurar_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)

        # Selección de producto
        layout.addWidget(QLabel("Seleccionar producto:"))
        self.cmb_producto = QComboBox()
        layout.addWidget(self.cmb_producto)

        # Cantidad
        cant_layout = QHBoxLayout()
        cant_layout.addWidget(QLabel("Cantidad:"))
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        self.spin_cantidad.setMaximum(999)
        cant_layout.addWidget(self.spin_cantidad)
        layout.addLayout(cant_layout)

        # Stock actual
        self.lbl_stock = QLabel("Stock disponible: --")
        layout.addWidget(self.lbl_stock)

        # Botón registrar
        self.btn_registrar = QPushButton("Registrar Venta")
        self.btn_registrar.setStyleSheet("background-color: #28a745; color: white; padding: 10px;")
        layout.addWidget(self.btn_registrar)

        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QLabel { font-size: 13px; }
            QPushButton { border-radius: 4px; }
            QComboBox, QSpinBox { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
        """)

    def cargar_productos(self, productos: list, on_select_callback=None):
        """Llena el combo con los productos y sus IDs."""
        self.cmb_producto.clear()
        self.productos_dict = {}
        for p in productos:
            texto = f"{p.titulo} (Stock: {p.stock})"
            self.cmb_producto.addItem(texto)
            self.productos_dict[texto] = p.id
        if on_select_callback:
            self.cmb_producto.currentTextChanged.connect(on_select_callback)

    def obtener_producto_seleccionado_id(self) -> int:
        """Retorna el ID del producto seleccionado."""
        texto = self.cmb_producto.currentText()
        return self.productos_dict.get(texto)

    def obtener_cantidad(self) -> int:
        return self.spin_cantidad.value()

    def actualizar_stock_label(self, texto: str):
        self.lbl_stock.setText(f"Stock disponible: {texto}")

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        QMessageBox.critical(self, titulo, mensaje)

    def cerrar(self):
        self.close()


# --- Prueba visual ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = VentaFisicaView()

    class ProdFalso:
        def __init__(self, id, titulo, stock):
            self.id = id
            self.titulo = titulo
            self.stock = stock

    productos_prueba = [
        ProdFalso(1, "Cien años de soledad", 5),
        ProdFalso(2, "El principito", 0)
    ]
    ventana.cargar_productos(productos_prueba)
    ventana.show()
    sys.exit(app.exec())