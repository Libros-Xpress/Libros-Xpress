"""
Módulo: catalogo_view.py
Propósito: Catálogo visual con búsqueda, carrito, panel admin, historial y diseño Digital‑Shift.
Autor: David Solís
Versión: 2.0.0 – Fase 3 (Catálogo)
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QScrollArea, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QBrush

# ── helpers visuales ──────────────────────────────────────────────
def crear_portada_placeholder(titulo, ancho=160, alto=210):
    """Genera un QPixmap decorativo con el título del libro centrado."""
    pix = QPixmap(ancho, alto)
    pix.fill(QColor("#F5E1C0"))                     # fondo marrón claro
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)

    # Borde sutil
    pen = QPen(QColor("#D4A574"), 2)
    painter.setPen(pen)
    painter.drawRoundedRect(2, 2, ancho-4, alto-4, 10, 10)

    # Ícono de libro
    font_icono = QFont("Segoe UI Emoji", 30)
    painter.setFont(font_icono)
    painter.setPen(QColor("#8B5E3C"))
    painter.drawText(pix.rect(), Qt.AlignHCenter | Qt.AlignTop, "\n\n📖")

    # Título del libro
    font_titulo = QFont("Segoe UI", 11, QFont.Bold)
    painter.setFont(font_titulo)
    painter.setPen(QColor("#5D4037"))
    painter.drawText(pix.rect().adjusted(8, 70, -8, -8),
                     Qt.AlignHCenter | Qt.TextWordWrap, titulo)
    painter.end()
    return pix

# ── clase principal ──────────────────────────────────────────────
class CatalogoView(QMainWindow):
    """Ventana principal del catálogo de Libros/Xpress."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Libros/Xpress – Catálogo")
        self.setMinimumSize(900, 650)
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
        layout_principal = QVBoxLayout(central)

        # ── Barra superior (información de usuario) ──
        self.lbl_usuario = QLabel()
        self.lbl_usuario.setFont(QFont("Segoe UI", 10))
        self.lbl_usuario.setStyleSheet("color: #6B3A2A; padding: 4px;")
        layout_principal.addWidget(self.lbl_usuario)

        # ── Barra de herramientas ──
        barra = QHBoxLayout()
        barra.addWidget(QLabel("Buscar:"))
        self.txt_busqueda = QLineEdit()
        self.txt_busqueda.setPlaceholderText("Título del libro…")
        barra.addWidget(self.txt_busqueda)

        barra.addWidget(QLabel("Autor:"))
        self.cmb_autor = QComboBox()
        self.cmb_autor.addItem("Todos")
        barra.addWidget(self.cmb_autor)

        barra.addWidget(QLabel("Categoría:"))
        self.cmb_categoria = QComboBox()
        self.cmb_categoria.addItem("Todas")
        barra.addWidget(self.cmb_categoria)

        self.btn_buscar = QPushButton("Buscar")
        barra.addWidget(self.btn_buscar)

        self.btn_carrito = QPushButton("🛒 Carrito")
        barra.addWidget(self.btn_carrito)

        self.btn_admin = QPushButton("Panel Admin")
        self.btn_admin.setVisible(False)
        barra.addWidget(self.btn_admin)

        self.btn_venta_fisica = QPushButton("Venta Física")
        self.btn_venta_fisica.setVisible(False)
        barra.addWidget(self.btn_venta_fisica)

        self.btn_historial = QPushButton("Historial")
        barra.addWidget(self.btn_historial)

        layout_principal.addLayout(barra)

        # ── Área de resultados ──
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # centrar contenido
        self.scroll_layout.setHorizontalSpacing(20)
        self.scroll_layout.setVerticalSpacing(20)
        self.scroll_area.setWidget(self.scroll_widget)
        layout_principal.addWidget(self.scroll_area)

        # ── Estilos ──
        self.setStyleSheet("""
            QMainWindow { background-color: #FFF8F0; }
            QLabel { font-size: 13px; color: #5D4037; }
            QPushButton {
                background-color: #8B5E3C; color: white;
                border: none; padding: 8px 14px; border-radius: 6px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #6B3A2A; }
            QLineEdit, QComboBox {
                padding: 6px; border: 1px solid #D4A574; border-radius: 6px;
                background-color: #FFFAF5; color: #3E2723; font-size: 13px;
            }
            QComboBox::drop-down { border: none; }
        """)

    # ── limpieza ──
    def limpiar_resultados(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # ── mostrar productos ──
    def mostrar_productos(self, productos, on_agregar=None):
        self.limpiar_resultados()
        if not productos:
            lbl = QLabel("No se encontraron productos.")
            lbl.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(lbl, 0, 0)
            return

        columnas = 3
        for i, prod in enumerate(productos):
            fila, col = i // columnas, i % columnas

            # Tarjeta compacta
            tarjeta = QWidget()
            tarjeta.setStyleSheet("""
                QWidget { background-color: #FFFAF5; border-radius: 12px;
                          padding: 10px; }
            """)
            tarjeta.setFixedWidth(230)          # ancho fijo
            ly = QVBoxLayout(tarjeta)
            ly.setSpacing(4)

            # Portada (tamaño ajustado)
            lbl_img = QLabel()
            pix = QPixmap(prod.portada)
            if pix.isNull():
                pix = crear_portada_placeholder(prod.titulo, 160, 210)
            else:
                pix = pix.scaled(160, 210, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl_img.setPixmap(pix)
            lbl_img.setAlignment(Qt.AlignCenter)
            ly.addWidget(lbl_img)

            # Título
            lbl_tit = QLabel(prod.titulo)
            lbl_tit.setWordWrap(True)
            lbl_tit.setAlignment(Qt.AlignCenter)
            lbl_tit.setStyleSheet("font-weight: bold; font-size: 13px; color: #3E2723;")
            ly.addWidget(lbl_tit)

            # Precio
            lbl_precio = QLabel(f"${prod.precio:.2f}")
            lbl_precio.setAlignment(Qt.AlignCenter)
            lbl_precio.setStyleSheet("font-size: 15px; font-weight: bold; color: #8B5E3C;")
            ly.addWidget(lbl_precio)

            # Stock
            stock = getattr(prod, 'stock', 0)
            color_stock = "#2E7D32" if stock > 0 else "#C0392B"
            texto_stock = f"Stock: {stock}" if stock > 0 else "AGOTADO"
            lbl_stock = QLabel(texto_stock)
            lbl_stock.setAlignment(Qt.AlignCenter)
            lbl_stock.setStyleSheet(f"font-size: 11px; color: {color_stock};")
            ly.addWidget(lbl_stock)

            # Botón Agregar
            btn = QPushButton("Agregar al carrito")
            btn.setStyleSheet("""
                QPushButton { background-color: #A5D6A7; color: #1B5E20;
                              font-weight: bold; border: none; padding: 6px;
                              border-radius: 6px; font-size: 12px; }
                QPushButton:hover { background-color: #81C784; }
            """)
            if on_agregar:
                btn.clicked.connect(lambda _, t=prod.titulo, p=prod.precio: on_agregar(t, p))
            ly.addWidget(btn)

            self.scroll_layout.addWidget(tarjeta, fila, col)

    # ── accesos ──
    def obtener_texto_busqueda(self):       return self.txt_busqueda.text().strip()
    def obtener_autor_seleccionado(self):  return self.cmb_autor.currentText()
    def obtener_categoria_seleccionada(self): return self.cmb_categoria.currentText()

    def cargar_autores(self, lista):
        self.cmb_autor.clear()
        self.cmb_autor.addItem("Todos")
        self.cmb_autor.addItems(lista)

    def cargar_categorias(self, lista):
        self.cmb_categoria.clear()
        self.cmb_categoria.addItem("Todas")
        self.cmb_categoria.addItems(lista)

    def mostrar_usuario(self, nombre, rol):
        self.lbl_usuario.setText(f"Conectado: {nombre} ({rol})")

    def mostrar_mensaje(self, t, m):   QMessageBox.information(self, t, m)
    def mostrar_error(self, t, m):     QMessageBox.critical(self, t, m)


# ── prueba visual ──
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    v = CatalogoView()
    class Falso:
        def __init__(self, t, a, p, portada, stock):
            self.titulo, self.autor, self.precio, self.portada, self.stock = t, a, p, portada, stock
    v.mostrar_productos([
        Falso("Cien años de soledad", "G. García Márquez", 19.99, "", 10),
        Falso("El principito", "A. de Saint-Exupéry", 12.50, "", 0),
        Falso("1984", "George Orwell", 15.00, "", 3),
        Falso("Python para todos", "John Doe", 22.00, "", 7),
    ], on_agregar=lambda t, p: print(f"Agregado: {t} ${p}"))
    v.cargar_autores(["G. García Márquez", "A. de Saint-Exupéry"])
    v.cargar_categorias(["Novela", "Infantil"])
    v.mostrar_usuario("admin", "Administrador")
    v.show()
    sys.exit(app.exec())