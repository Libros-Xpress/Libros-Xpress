"""
Módulo: admin_productos_view.py
Propósito: Interfaz gráfica del panel de administración de productos (CRUD) para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QDialogButtonBox
)
from PySide6.QtCore import Qt

class AdminProductosView(QMainWindow):
    """Ventana del panel de administración de productos."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrar Productos - Libros-Xpress")
        self.setMinimumSize(800, 600)
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

        # Tabla de productos
        self.tabla = QTableWidget(0, 6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Título", "Autor", "Categoría", "Precio", "Portada"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        # Botones de acción
        botones_layout = QHBoxLayout()
        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_refrescar = QPushButton("Refrescar")
        self.btn_cerrar = QPushButton("Cerrar")
        botones_layout.addWidget(self.btn_nuevo)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_refrescar)
        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_cerrar)
        layout.addLayout(botones_layout)

        # Estilos
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QPushButton { padding: 8px 16px; border-radius: 4px; }
            QPushButton:hover { opacity: 0.9; }
        """)

    def cargar_productos(self, productos: list):
        """Llena la tabla con los productos."""
        self.tabla.setRowCount(0)
        for prod in productos:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(prod.id)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(prod.titulo))
            self.tabla.setItem(fila, 2, QTableWidgetItem(prod.autor))
            self.tabla.setItem(fila, 3, QTableWidgetItem(prod.categoria))
            self.tabla.setItem(fila, 4, QTableWidgetItem(f"${prod.precio:.2f}"))
            self.tabla.setItem(fila, 5, QTableWidgetItem(prod.portada))

    def obtener_producto_seleccionado(self) -> dict:
        """Retorna un diccionario con los datos de la fila seleccionada, o None."""
        fila = self.tabla.currentRow()
        if fila < 0:
            return None
        return {
            "id": int(self.tabla.item(fila, 0).text()),
            "titulo": self.tabla.item(fila, 1).text(),
            "autor": self.tabla.item(fila, 2).text(),
            "categoria": self.tabla.item(fila, 3).text(),
            "precio": float(self.tabla.item(fila, 4).text().replace("$", "")),
            "portada": self.tabla.item(fila, 5).text()
        }

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        QMessageBox.critical(self, titulo, mensaje)

    def cerrar(self):
        self.close()


class ProductoDialog(QDialog):
    """Diálogo para agregar o editar un producto."""

    def __init__(self, datos: dict = None, parent=None):
        super().__init__(parent)
        self.datos = datos
        self.setWindowTitle("Editar Producto" if datos else "Nuevo Producto")
        self._configurar_ui()

    def _configurar_ui(self):
        layout = QFormLayout(self)
        self.txt_titulo = QLineEdit(self.datos.get("titulo", "") if self.datos else "")
        self.txt_autor = QLineEdit(self.datos.get("autor", "") if self.datos else "")
        self.txt_categoria = QLineEdit(self.datos.get("categoria", "") if self.datos else "")
        self.spin_precio = QDoubleSpinBox()
        self.spin_precio.setRange(0, 9999.99)
        self.spin_precio.setDecimals(2)
        if self.datos:
            self.spin_precio.setValue(self.datos.get("precio", 0.0))
        self.txt_portada = QLineEdit(self.datos.get("portada", "") if self.datos else "")
        layout.addRow("Título:", self.txt_titulo)
        layout.addRow("Autor:", self.txt_autor)
        layout.addRow("Categoría:", self.txt_categoria)
        layout.addRow("Precio:", self.spin_precio)
        layout.addRow("Portada (ruta):", self.txt_portada)

        self.botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        layout.addRow(self.botones)

    def obtener_datos(self) -> dict:
        """Retorna un diccionario con los datos ingresados."""
        return {
            "titulo": self.txt_titulo.text().strip(),
            "autor": self.txt_autor.text().strip(),
            "categoria": self.txt_categoria.text().strip(),
            "precio": self.spin_precio.value(),
            "portada": self.txt_portada.text().strip()
        }


# --- Prueba visual de la vista ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Crear algunos productos falsos para probar la vista
    class ProdFalso:
        def __init__(self, id, titulo, autor, categoria, precio, portada):
            self.id = id
            self.titulo = titulo
            self.autor = autor
            self.categoria = categoria
            self.precio = precio
            self.portada = portada

    productos_prueba = [
        ProdFalso(1, "Cien años de soledad", "Gabriel García Márquez", "Novela", 19.99, ""),
        ProdFalso(2, "El principito", "Antoine de Saint-Exupéry", "Infantil", 12.50, ""),
        ProdFalso(3, "1984", "George Orwell", "Ciencia ficción", 15.00, "")
    ]

    ventana = AdminProductosView()
    ventana.cargar_productos(productos_prueba)
    ventana.show()
    sys.exit(app.exec())