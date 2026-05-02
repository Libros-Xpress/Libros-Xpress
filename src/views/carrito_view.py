"""
Módulo: carrito_view.py
Propósito: Interfaz gráfica del carrito de compras y checkout para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QHeaderView, QMessageBox, QLineEdit, QFormLayout, QGroupBox
)
from PySide6.QtCore import Qt

class CarritoView(QMainWindow):
    """
    Ventana del carrito de compras.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carrito de Compras - Libros-Xpress")
        self.setMinimumSize(600, 400)
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

        # Título
        titulo = QLabel("Tu Carrito")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)

        # Tabla de items
        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad", "Subtotal"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tabla.setColumnWidth(2, 80)
        layout.addWidget(self.tabla)

        # Resumen
        resumen_layout = QHBoxLayout()
        self.lbl_subtotal = QLabel("Subtotal: $0.00")
        self.lbl_impuesto = QLabel("Impuesto (13%): $0.00")
        self.lbl_total = QLabel("Total: $0.00")
        self.lbl_total.setStyleSheet("font-weight: bold; font-size: 14px;")
        resumen_layout.addWidget(self.lbl_subtotal)
        resumen_layout.addWidget(self.lbl_impuesto)
        resumen_layout.addStretch()
        resumen_layout.addWidget(self.lbl_total)
        layout.addLayout(resumen_layout)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_seguir = QPushButton("Seguir Comprando")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar Seleccionado")
        self.btn_checkout = QPushButton("Finalizar Compra")
        self.btn_checkout.setStyleSheet("background-color: #28a745; color: white;")
        botones_layout.addWidget(self.btn_seguir)
        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_checkout)
        layout.addLayout(botones_layout)

        # Grupo de Pago (inicialmente oculto)
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
        self.btn_confirmar_pago.setStyleSheet("background-color: #0078d4; color: white;")
        form_pago.addRow(self.btn_confirmar_pago)
        self.grupo_pago.setLayout(form_pago)
        layout.addWidget(self.grupo_pago)

        # Estilos
        self.setStyleSheet("""
            QMainWindow { background-color: #f9f9f9; }
            QTableWidget { background-color: white; border: 1px solid #ddd; }
            QPushButton { padding: 8px; border-radius: 4px; }
            QPushButton:hover { opacity: 0.9; }
        """)

    def cargar_items(self, items: list):
        """Carga la tabla con los items del carrito. items: lista de ItemCarrito."""
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
        """Retorna un diccionario {titulo: cantidad} según los valores de los spinboxes."""
        cantidades = {}
        for fila in range(self.tabla.rowCount()):
            titulo = self.tabla.item(fila, 0).text()
            spin = self.tabla.cellWidget(fila, 2)
            cantidad = spin.value()
            cantidades[titulo] = cantidad
        return cantidades

    def obtener_producto_seleccionado(self) -> str:
        """Retorna el título del producto seleccionado en la tabla."""
        seleccion = self.tabla.currentRow()
        if seleccion >= 0:
            return self.tabla.item(seleccion, 0).text()
        return ""

    def actualizar_totales(self, subtotal: float, impuesto: float, total: float):
        self.lbl_subtotal.setText(f"Subtotal: ${subtotal:.2f}")
        self.lbl_impuesto.setText(f"Impuesto (13%): ${impuesto:.2f}")
        self.lbl_total.setText(f"Total: ${total:.2f}")

    def mostrar_seccion_pago(self, mostrar: bool):
        self.grupo_pago.setVisible(mostrar)

    def obtener_datos_pago(self):
        """Retorna (titular, numero) del formulario de pago."""
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