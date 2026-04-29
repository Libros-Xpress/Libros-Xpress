"""
Módulo: catalogo_view.py
Propósito: Interfaz gráfica del catálogo de productos con búsqueda avanzada.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QScrollArea, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os

class CatalogoView(QMainWindow):
    """
    Ventana principal del catálogo de Libros-Xpress.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Libros-Xpress - Catálogo")
        self.setMinimumSize(800, 600)
        self._configurar_ui()
        self._centrar_en_pantalla()

    def _centrar_en_pantalla(self):
        """Centra la ventana en la pantalla."""
        centro = self.screen().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centro)
        self.move(frame.topLeft())

    def _configurar_ui(self):
        """Construye y organiza los widgets de la interfaz."""
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QVBoxLayout(central)

        # --- Barra de búsqueda y filtros ---
        barra_layout = QHBoxLayout()
        barra_layout.addWidget(QLabel("Buscar:"))
        self.txt_busqueda = QLineEdit()
        self.txt_busqueda.setPlaceholderText("Título del libro...")
        barra_layout.addWidget(self.txt_busqueda)

        barra_layout.addWidget(QLabel("Autor:"))
        self.cmb_autor = QComboBox()
        self.cmb_autor.addItem("Todos")
        barra_layout.addWidget(self.cmb_autor)

        barra_layout.addWidget(QLabel("Categoría:"))
        self.cmb_categoria = QComboBox()
        self.cmb_categoria.addItem("Todas")
        barra_layout.addWidget(self.cmb_categoria)

        self.btn_buscar = QPushButton("Buscar")
        barra_layout.addWidget(self.btn_buscar)

        layout_principal.addLayout(barra_layout)

        # --- Área de resultados con scroll ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        layout_principal.addWidget(self.scroll_area)

        # Aplicar estilos básicos
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QLabel { font-size: 13px; }
            QPushButton {
                background-color: #0078d4; color: white;
                border: none; padding: 8px 16px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #005a9e; }
            QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
            QComboBox { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
        """)

    def limpiar_resultados(self):
        """Elimina todos los widgets del área de resultados."""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def mostrar_productos(self, productos):
        """
        Muestra los productos en la cuadrícula de resultados.

        Args:
            productos (list[Producto]): Lista de productos a mostrar.
        """
        self.limpiar_resultados()
        if not productos:
            lbl = QLabel("No se encontraron productos.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scroll_layout.addWidget(lbl, 0, 0)
            return

        columnas = 3
        for indice, producto in enumerate(productos):
            fila = indice // columnas
            columna = indice % columnas

            # Contenedor por producto
            contenedor = QWidget()
            contenedor.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")
            layout_producto = QVBoxLayout(contenedor)

            # Imagen de portada
            lbl_imagen = QLabel()
            pixmap = QPixmap(producto.portada)
            if pixmap.isNull():
                # Imagen por defecto
                pixmap = QPixmap(200, 250)
                pixmap.fill(Qt.GlobalColor.gray)
            else:
                pixmap = pixmap.scaled(200, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            lbl_imagen.setPixmap(pixmap)
            lbl_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_producto.addWidget(lbl_imagen)

            # Título
            lbl_titulo = QLabel(producto.titulo)
            lbl_titulo.setWordWrap(True)
            lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
            layout_producto.addWidget(lbl_titulo)

            # Precio
            lbl_precio = QLabel(f"${producto.precio:.2f}")
            lbl_precio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_precio.setStyleSheet("color: #0078d4; font-weight: bold; font-size: 16px;")
            layout_producto.addWidget(lbl_precio)

            self.scroll_layout.addWidget(contenedor, fila, columna)

    def obtener_texto_busqueda(self) -> str:
        """Retorna el texto ingresado en la barra de búsqueda."""
        return self.txt_busqueda.text().strip()

    def obtener_autor_seleccionado(self) -> str:
        """Retorna el autor seleccionado, o 'Todos'."""
        return self.cmb_autor.currentText()

    def obtener_categoria_seleccionada(self) -> str:
        """Retorna la categoría seleccionada, o 'Todas'."""
        return self.cmb_categoria.currentText()

    def cargar_autores(self, autores: list):
        """Carga la lista de autores en el combo."""
        self.cmb_autor.clear()
        self.cmb_autor.addItem("Todos")
        self.cmb_autor.addItems(autores)

    def cargar_categorias(self, categorias: list):
        """Carga la lista de categorías en el combo."""
        self.cmb_categoria.clear()
        self.cmb_categoria.addItem("Todas")
        self.cmb_categoria.addItems(categorias)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        """Muestra un QMessageBox informativo."""
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        """Muestra un QMessageBox de error."""
        QMessageBox.critical(self, titulo, mensaje)


# --- Prueba de interfaz (visual) ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ventana = CatalogoView()
    # Simular carga de algunos productos de prueba
    class ProdFalso:
        def __init__(self, titulo, autor, precio, portada):
            self.titulo = titulo
            self.autor = autor
            self.precio = precio
            self.portada = portada
    prod_prueba = [
        ProdFalso("Libro A", "Autor A", 9.99, ""),
        ProdFalso("Libro B", "Autor B", 14.99, "")
    ]
    ventana.mostrar_productos(prod_prueba)
    ventana.cargar_autores(["Autor A", "Autor B"])
    ventana.cargar_categorias(["Ficción", "No ficción"])
    ventana.show()
    sys.exit(app.exec())