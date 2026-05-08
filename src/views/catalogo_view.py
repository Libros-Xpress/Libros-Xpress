"""
Módulo: catalogo_view.py
Propósito: Interfaz gráfica del catálogo de productos con búsqueda avanzada, carrito, panel admin, historial, venta física y visualización de stock.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.4.0 - Sprint 4 (Sincronización de stock y facturación)
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QScrollArea, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


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
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QVBoxLayout(central)

        # --- Barra de herramientas completa ---
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

        self.btn_carrito = QPushButton("🛒 Carrito")
        barra_layout.addWidget(self.btn_carrito)

        self.btn_admin = QPushButton("Panel Admin")
        self.btn_admin.setVisible(False)
        barra_layout.addWidget(self.btn_admin)

        # Nuevo botón para venta física (solo admin, sincronización de stock)
        self.btn_venta_fisica = QPushButton("Venta Física")
        self.btn_venta_fisica.setVisible(False)
        barra_layout.addWidget(self.btn_venta_fisica)

        self.btn_historial = QPushButton("Historial")
        barra_layout.addWidget(self.btn_historial)

        layout_principal.addLayout(barra_layout)

        # --- Área de resultados con scroll ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        layout_principal.addWidget(self.scroll_area)

        # Estilos básicos
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

    def mostrar_productos(self, productos, on_agregar=None):
        """
        Muestra los productos en la cuadrícula de resultados, ahora con stock visible.

        Args:
            productos (list[Producto]): Lista de productos a mostrar.
            on_agregar (callable, opcional): Función(titulo, precio) al hacer clic en 'Agregar'.
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

            # Stock disponible (nuevo Sprint 4)
            lbl_stock = QLabel(f"Stock: {producto.stock}")
            lbl_stock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_stock.setStyleSheet("font-size: 12px; color: #555;")
            layout_producto.addWidget(lbl_stock)

            # Botón Agregar al carrito
            btn_agregar = QPushButton("Agregar")
            btn_agregar.setStyleSheet("background-color: #28a745; color: white; padding: 5px; border-radius: 4px;")
            if on_agregar:
                btn_agregar.clicked.connect(lambda checked, t=producto.titulo, p=producto.precio: on_agregar(t, p))
            layout_producto.addWidget(btn_agregar)

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


# --- Prueba visual de la vista ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = CatalogoView()

    # Simular carga de algunos productos de prueba (ahora con stock)
    class ProdFalso:
        def __init__(self, titulo, autor, precio, portada, stock):
            self.titulo = titulo
            self.autor = autor
            self.precio = precio
            self.portada = portada
            self.stock = stock

    prod_prueba = [
        ProdFalso("Libro A", "Autor A", 9.99, "", 5),
        ProdFalso("Libro B", "Autor B", 14.99, "", 2)
    ]

    # Asignar un callback dummy para probar los botones "Agregar"
    def dummy_agregar(titulo, precio):
        print(f"[Prueba] Agregado al carrito: {titulo} ${precio:.2f}")

    ventana.mostrar_productos(prod_prueba, on_agregar=dummy_agregar)
    ventana.cargar_autores(["Autor A", "Autor B"])
    ventana.cargar_categorias(["Ficción", "No ficción"])
    # Mostrar botones de admin y venta física para prueba visual
    ventana.btn_admin.setVisible(True)
    ventana.btn_venta_fisica.setVisible(True)
    ventana.show()
    sys.exit(app.exec())