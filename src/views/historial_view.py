"""
Módulo: historial_view.py
Propósito: Interfaz gráfica para consultar el historial de pedidos y descargar facturas.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.1.0 - Sprint 4 (Descarga de facturas)
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt

class HistorialView(QMainWindow):
    """Ventana para mostrar el historial de pedidos del usuario."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de Pedidos - Libros-Xpress")
        self.setMinimumSize(650, 450)
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

        # Tabla de pedidos
        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha", "Total", "Estado"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        # Botones inferiores
        botones_layout = QHBoxLayout()
        self.btn_descargar_factura = QPushButton("Descargar Factura")
        self.btn_descargar_factura.setStyleSheet("background-color: #0078d4; color: white;")
        btn_cerrar = QPushButton("Cerrar")
        botones_layout.addWidget(self.btn_descargar_factura)
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cerrar)
        layout.addLayout(botones_layout)

        # Conectar botón cerrar
        btn_cerrar.clicked.connect(self.close)

        # Estilos
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QTableWidget { background-color: white; border: 1px solid #ddd; }
            QPushButton { padding: 8px 16px; border-radius: 4px; }
        """)

    def cargar_historial(self, pedidos: list):
        """Llena la tabla con los pedidos del usuario."""
        self.tabla.setRowCount(0)
        for pedido in pedidos:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(pedido.get('id', ''))))
            self.tabla.setItem(fila, 1, QTableWidgetItem(pedido.get('fecha', '')))
            self.tabla.setItem(fila, 2, QTableWidgetItem(f"${pedido.get('total', 0):.2f}"))
            self.tabla.setItem(fila, 3, QTableWidgetItem(pedido.get('estado', 'Pendiente')))

    def obtener_pedido_seleccionado(self) -> dict:
        """Retorna un diccionario con los datos del pedido seleccionado, o None si no hay selección."""
        fila = self.tabla.currentRow()
        if fila < 0:
            return None
        return {
            "id": int(self.tabla.item(fila, 0).text()),
            "fecha": self.tabla.item(fila, 1).text(),
            "total": float(self.tabla.item(fila, 2).text().replace("$", "")),
            "estado": self.tabla.item(fila, 3).text()
        }

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        QMessageBox.critical(self, titulo, mensaje)


# --- Prueba visual ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = HistorialView()
    # Simular datos
    pedidos_ejemplo = [
        {"id": 1, "fecha": "2026-05-01", "total": 45.20, "estado": "Entregado"},
        {"id": 2, "fecha": "2026-05-05", "total": 32.99, "estado": "Pendiente"}
    ]
    ventana.cargar_historial(pedidos_ejemplo)
    ventana.show()
    sys.exit(app.exec())