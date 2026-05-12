"""
Módulo: historial_view.py
Propósito: Historial de pedidos y descarga de facturas con diseño Digital‑Shift.
Autor: David Solís
Versión: 2.0.0 – Fase 6 (Historial)
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class HistorialView(QMainWindow):
    """Ventana para mostrar el historial de pedidos del usuario."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de Pedidos – Libros/Xpress")
        self.setMinimumSize(700, 480)
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
        self.btn_descargar_factura.setStyleSheet("background-color: #A5D6A7; color: #1B5E20;")
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        botones_layout.addWidget(self.btn_descargar_factura)
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cerrar)
        layout.addLayout(botones_layout)

        # Estilos
        self.setStyleSheet("""
            QMainWindow { background-color: #FFF8F0; }
            QTableWidget {
                background-color: #FFFAF5; border: 1px solid #D4A574;
                alternate-background-color: #F5E1C0;
                gridline-color: #D4A574; font-size: 13px; color: #3E2723;
            }
            QHeaderView::section {
                background-color: #8B5E3C; color: white; padding: 6px;
                font-weight: bold; border: none;
            }
            QPushButton {
                background-color: #8B5E3C; color: white;
                border: none; padding: 8px 14px; border-radius: 6px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #6B3A2A; }
        """)

    def cargar_historial(self, pedidos: list):
        self.tabla.setRowCount(0)
        for pedido in pedidos:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(pedido.get('id', ''))))
            self.tabla.setItem(fila, 1, QTableWidgetItem(pedido.get('fecha', '')))
            self.tabla.setItem(fila, 2, QTableWidgetItem(f"${pedido.get('total', 0):.2f}"))
            self.tabla.setItem(fila, 3, QTableWidgetItem(pedido.get('estado', 'Pendiente')))

    def obtener_pedido_seleccionado(self) -> dict:
        fila = self.tabla.currentRow()
        if fila < 0:
            return None
        return {
            "id": int(self.tabla.item(fila, 0).text()),
            "fecha": self.tabla.item(fila, 1).text(),
            "total": float(self.tabla.item(fila, 2).text().replace("$", "")),
            "estado": self.tabla.item(fila, 3).text()
        }

    def mostrar_mensaje(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)


# --- Prueba visual ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = HistorialView()
    pedidos_ejemplo = [
        {"id": 1, "fecha": "2026-05-01", "total": 45.20, "estado": "Entregado"},
        {"id": 2, "fecha": "2026-05-05", "total": 32.99, "estado": "Pendiente"}
    ]
    ventana.cargar_historial(pedidos_ejemplo)
    ventana.show()
    sys.exit(app.exec())