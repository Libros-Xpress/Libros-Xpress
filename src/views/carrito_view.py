"""
Módulo: carrito_view.py
Propósito: Interfaz gráfica del carrito de compras, checkout y cupones con diseño Digital‑Shift.
Autor: David Solís
Versión: 2.0.0 – Fase 4 (Carrito)
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QHeaderView, QMessageBox, QLineEdit, QFormLayout, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class CarritoView(QMainWindow):
    """Ventana del carrito de compras con diseño Digital‑Shift."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carrito de Compras – Libros/Xpress")
        self.setMinimumSize(650, 480)
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
        titulo = QLabel("Tu Carrito")
        titulo.setFont(QFont("Segoe UI", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Tabla de items
        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad", "Subtotal"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tabla.setColumnWidth(2, 80)
        layout.addWidget(self.tabla)

        # Sección de código promocional
        cupon_layout = QHBoxLayout()
        cupon_layout.addWidget(QLabel("Código promocional:"))
        self.txt_cupon = QLineEdit()
        self.txt_cupon.setPlaceholderText("Ingresa tu código")
        cupon_layout.addWidget(self.txt_cupon)
        self.btn_aplicar_cupon = QPushButton("Aplicar")
        cupon_layout.addWidget(self.btn_aplicar_cupon)
        layout.addLayout(cupon_layout)

        # Resumen de totales
        resumen_layout = QHBoxLayout()
        self.lbl_subtotal = QLabel("Subtotal: $0.00")
        self.lbl_descuento = QLabel("Descuento: -$0.00")
        self.lbl_descuento.setVisible(False)
        self.lbl_impuesto = QLabel("Impuesto (13%): $0.00")
        self.lbl_total = QLabel("Total: $0.00")
        self.lbl_total.setFont(QFont("Segoe UI", 13, QFont.Bold))
        resumen_layout.addWidget(self.lbl_subtotal)
        resumen_layout.addWidget(self.lbl_descuento)
        resumen_layout.addWidget(self.lbl_impuesto)
        resumen_layout.addStretch()
        resumen_layout.addWidget(self.lbl_total)
        layout.addLayout(resumen_layout)

        # Botones de acción
        botones_layout = QHBoxLayout()
        self.btn_seguir = QPushButton("Seguir Comprando")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar Seleccionado")
        self.btn_checkout = QPushButton("Finalizar Compra")
        self.btn_checkout.setStyleSheet("background-color: #A5D6A7; color: #1B5E20;")
        botones_layout.addWidget(self.btn_seguir)
        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_checkout)
        layout.addLayout(botones_layout)

        # Grupo de Pago (oculto)
        self.grupo_pago = QGroupBox("Datos de Pago")
        self.grupo_pago.setVisible(False)
        form_pago = QFormLayout()
        self.txt_titular = QLineEdit()
        self.txt_titular.setPlaceholderText("Nombre del titular")
        self.txt_numero = QLineEdit()
        self.txt_numero.setPlaceholderText("Número de tarjeta")
        form_pago.addRow("Titular:", self.txt_titular)
        form_pago.addRow("Nº Tarjeta:", self.txt_numero)
        self.btn_confirmar_pago = QPushButton("Confirmar Pago")
        form_pago.addRow(self.btn_confirmar_pago)
        self.grupo_pago.setLayout(form_pago)
        layout.addWidget(self.grupo_pago)

        # Estilos
        self.setStyleSheet("""
            QMainWindow { background-color: #FFF8F0; }
            QLabel { font-size: 13px; color: #5D4037; }
            QPushButton {
                background-color: #8B5E3C; color: white;
                border: none; padding: 8px 14px; border-radius: 6px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #6B3A2A; }
            QLineEdit, QSpinBox {
                padding: 6px; border: 1px solid #D4A574; border-radius: 6px;
                background-color: #FFFAF5; color: #3E2723; font-size: 13px;
            }
            QTableWidget {
                background-color: #FFFAF5; border: 1px solid #D4A574;
                alternate-background-color: #F5E1C0;
                gridline-color: #D4A574; font-size: 13px; color: #3E2723;
            }
            QHeaderView::section {
                background-color: #8B5E3C; color: white; padding: 6px;
                font-weight: bold; border: none;
            }
            QGroupBox {
                font-weight: bold; color: #5D4037; border: 1px solid #D4A574;
                border-radius: 6px; margin-top: 10px; padding-top: 10px;
            }
        """)

    def cargar_items(self, items: list):
        self.tabla.setRowCount(0)
        for item in items:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(item.titulo))
            self.tabla.setItem(fila, 1, QTableWidgetItem(f"${item.precio:.2f}"))
            spin = QSpinBox()
            spin.setMinimum(0)
            spin.setMaximum(99)
            spin.setValue(item.cantidad)
            self.tabla.setCellWidget(fila, 2, spin)
            self.tabla.setItem(fila, 3, QTableWidgetItem(f"${item.subtotal():.2f}"))

    def obtener_cantidades_actualizadas(self) -> dict:
        cantidades = {}
        for fila in range(self.tabla.rowCount()):
            titulo = self.tabla.item(fila, 0).text()
            spin = self.tabla.cellWidget(fila, 2)
            cantidad = spin.value()
            cantidades[titulo] = cantidad
        return cantidades

    def obtener_producto_seleccionado(self) -> str:
        seleccion = self.tabla.currentRow()
        if seleccion >= 0:
            return self.tabla.item(seleccion, 0).text()
        return ""

    def obtener_codigo_cupon(self) -> str:
        return self.txt_cupon.text().strip()

    def actualizar_totales(self, subtotal: float, impuesto: float, total: float, descuento: float = 0.0):
        self.lbl_subtotal.setText(f"Subtotal: ${subtotal:.2f}")
        self.lbl_impuesto.setText(f"Impuesto (13%): ${impuesto:.2f}")
        self.lbl_total.setText(f"Total: ${total:.2f}")
        if descuento > 0:
            self.lbl_descuento.setText(f"Descuento: -${descuento:.2f}")
            self.lbl_descuento.setVisible(True)
        else:
            self.lbl_descuento.setVisible(False)

    def mostrar_seccion_pago(self, mostrar: bool):
        self.grupo_pago.setVisible(mostrar)

    def obtener_datos_pago(self):
        return self.txt_titular.text().strip(), self.txt_numero.text().strip()

    def limpiar_pago(self):
        self.txt_titular.clear()
        self.txt_numero.clear()

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        QMessageBox.critical(self, titulo, mensaje)

    def cerrar(self):
        self.close()


# --- Prueba visual de la vista ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ventana = CarritoView()
    class ItemFalso:
        def __init__(self, titulo, precio, cantidad):
            self.titulo, self.precio, self.cantidad = titulo, precio, cantidad
        def subtotal(self):
            return self.precio * self.cantidad
    items_falsos = [
        ItemFalso("Cien años de soledad", 19.99, 2),
        ItemFalso("El principito", 12.50, 1)
    ]
    ventana.cargar_items(items_falsos)
    ventana.actualizar_totales(52.48, 6.82, 59.30)
    ventana.show()
    sys.exit(app.exec())