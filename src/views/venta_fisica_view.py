"""
Módulo: venta_fisica_view.py
Propósito: Interfaz gráfica para registrar ventas físicas con diseño Digital‑Shift.
Autor: David Solís
Versión: 2.0.0 – Fase 5 (Venta Física)
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class VentaFisicaView(QMainWindow):
    """Ventana para registrar una venta en tienda física."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Venta Física – Libros/Xpress")
        self.setFixedSize(420, 280)
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
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        # Título
        titulo = QLabel("Venta en Tienda Física")
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Producto:"))
        self.cmb_producto = QComboBox()
        layout.addWidget(self.cmb_producto)

        cant_layout = QHBoxLayout()
        cant_layout.addWidget(QLabel("Cantidad:"))
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        self.spin_cantidad.setMaximum(999)
        cant_layout.addWidget(self.spin_cantidad)
        layout.addLayout(cant_layout)

        self.lbl_stock = QLabel("Stock disponible: --")
        layout.addWidget(self.lbl_stock)

        self.btn_registrar = QPushButton("Registrar Venta")
        layout.addWidget(self.btn_registrar)

        # Estilos
        self.setStyleSheet("""
            QMainWindow { background-color: #FFF8F0; }
            QLabel { font-size: 13px; color: #5D4037; }
            QPushButton {
                background-color: #8B5E3C; color: white;
                border: none; padding: 10px; border-radius: 6px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #6B3A2A; }
            QComboBox, QSpinBox {
                padding: 8px; border: 1px solid #D4A574; border-radius: 6px;
                background-color: #FFFAF5; color: #3E2723; font-size: 13px;
            }
        """)

    def cargar_productos(self, productos: list, on_select_callback=None):
        self.cmb_producto.clear()
        self.productos_dict = {}
        for p in productos:
            if p.stock == 0:
                texto = f"{p.titulo} (AGOTADO)"
            else:
                texto = f"{p.titulo} (Stock: {p.stock})"
            self.cmb_producto.addItem(texto)
            self.productos_dict[texto] = p.id
        if on_select_callback:
            self.cmb_producto.currentTextChanged.connect(on_select_callback)
        # Actualizar label de stock automáticamente al cambiar selección
        self.cmb_producto.currentTextChanged.connect(self._actualizar_stock_label)

    def _actualizar_stock_label(self, texto):
        # Extraer número de stock del texto
        if "AGOTADO" in texto:
            self.lbl_stock.setText("Stock disponible: 0 (AGOTADO)")
            self.lbl_stock.setStyleSheet("color: #C0392B; font-weight: bold;")
            self.btn_registrar.setEnabled(False)
        else:
            # Buscar el stock en el texto
            import re
            match = re.search(r'\d+', texto)
            if match:
                stock = int(match.group())
                self.lbl_stock.setText(f"Stock disponible: {stock}")
                self.lbl_stock.setStyleSheet("color: #2E7D32;")
                self.btn_registrar.setEnabled(True)
            else:
                self.lbl_stock.setText("Stock disponible: --")
                self.lbl_stock.setStyleSheet("color: #5D4037;")
                self.btn_registrar.setEnabled(True)

    def obtener_producto_seleccionado_id(self) -> int:
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
            self.id, self.titulo, self.stock = id, titulo, stock

    productos = [
        ProdFalso(1, "Cien años de soledad", 5),
        ProdFalso(2, "El principito", 0)
    ]
    ventana.cargar_productos(productos)
    ventana.show()
    sys.exit(app.exec())