"""
Módulo: admin_productos_view.py
Propósito: Panel de administración de productos (CRUD) con diseño Digital‑Shift y carga de portadas.
Autor: David Solís
Versión: 2.0.0 – Fase 5 (Panel Admin)
"""

import os, shutil
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QDialogButtonBox,
    QFileDialog, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class AdminProductosView(QMainWindow):
    """Ventana del panel de administración de productos."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administrar Productos – Libros/Xpress")
        self.setMinimumSize(850, 620)
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

        # Estilos generales
        self.setStyleSheet("""
            QMainWindow { background-color: #FFF8F0; }
            QLabel { font-size: 13px; color: #5D4037; }
            QPushButton {
                background-color: #8B5E3C; color: white;
                border: none; padding: 8px 14px; border-radius: 6px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #6B3A2A; }
            QLineEdit, QDoubleSpinBox, QComboBox {
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
        """)

    def cargar_productos(self, productos: list):
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
    """Diálogo para agregar o editar un producto, con selector de portada."""

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

        layout.addRow("Título:", self.txt_titulo)
        layout.addRow("Autor:", self.txt_autor)
        layout.addRow("Categoría:", self.txt_categoria)
        layout.addRow("Precio:", self.spin_precio)

        # ── Portada ──
        portada_layout = QHBoxLayout()
        self.txt_portada = QLineEdit(self.datos.get("portada", "") if self.datos else "")
        portada_layout.addWidget(self.txt_portada)
        btn_examinar = QPushButton("Examinar...")
        btn_examinar.clicked.connect(self.seleccionar_portada)
        portada_layout.addWidget(btn_examinar)
        layout.addRow("Portada:", portada_layout)

        # Previsualización
        self.lbl_preview = QLabel()
        self.lbl_preview.setFixedSize(120, 160)
        self.lbl_preview.setStyleSheet("border: 1px solid #D4A574; border-radius: 6px;")
        layout.addRow("Vista previa:", self.lbl_preview)

        self.botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        layout.addRow(self.botones)

        # Mostrar vista previa inicial
        self._actualizar_preview()

    def seleccionar_portada(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar portada",
                                              "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if ruta:
            # Copiar a assets/img/ si no está ya dentro
            destino_dir = os.path.join(os.getcwd(), "assets", "img")
            os.makedirs(destino_dir, exist_ok=True)
            nombre_base = os.path.basename(ruta)
            ruta_destino = os.path.join(destino_dir, nombre_base)
            if not os.path.exists(ruta_destino):
                shutil.copy(ruta, ruta_destino)
            self.txt_portada.setText(os.path.join("assets", "img", nombre_base))
            self._actualizar_preview()

    def _actualizar_preview(self):
        ruta = self.txt_portada.text().strip()
        pixmap = QPixmap(ruta)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(120, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_preview.setPixmap(pixmap)
        else:
            self.lbl_preview.setText("Sin imagen")

    def obtener_datos(self) -> dict:
        return {
            "titulo": self.txt_titulo.text().strip(),
            "autor": self.txt_autor.text().strip(),
            "categoria": self.txt_categoria.text().strip(),
            "precio": self.spin_precio.value(),
            "portada": self.txt_portada.text().strip()
        }


# ── Prueba visual ──
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = AdminProductosView()
    class P:
        def __init__(self, i, t, a, c, p, po):
            self.id, self.titulo, self.autor, self.categoria, self.precio, self.portada = i, t, a, c, p, po
    ventana.cargar_productos([P(1,"Test","Autor","Cat",9.99,"")])
    ventana.show()
    sys.exit(app.exec())