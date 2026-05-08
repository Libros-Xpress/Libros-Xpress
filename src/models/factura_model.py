"""
Módulo: factura_model.py
Propósito: Generación de facturas en formato PDF para pedidos confirmados, usando solo PySide6.
Autor: [Robert Cerón, David Solís, Juan Castro]
Versión: 1.0.0 - Sprint 4 (Generación de facturas sin dependencias externas)
"""

import os
import sys
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtGui import QTextDocument
from PySide6.QtCore import QMarginsF


class FacturaModel:
    """Modelo para generar facturas PDF de pedidos utilizando PySide6."""

    def __init__(self, carpeta_salida: str = "facturas"):
        self.carpeta_salida = carpeta_salida
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)

    def generar_factura_pdf(self, pedido: dict) -> str:
        """
        Genera un archivo PDF a partir de los datos del pedido.
        Retorna la ruta donde se guardó el PDF.
        """
        ruta_pdf = os.path.join(self.carpeta_salida, f"factura_{pedido['id']}.pdf")

        # Construir el contenido HTML de la factura
        html = self._construir_html(pedido)

        # Configurar la impresora virtual (PDF)
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(ruta_pdf)
        printer.setPageMargins(QMarginsF(20, 20, 20, 20))

        # Crear el documento HTML y renderizarlo
        doc = QTextDocument()
        doc.setHtml(html)
        doc.print_(printer)

        return ruta_pdf

    def _construir_html(self, pedido: dict) -> str:
        """Construye una cadena HTML con el detalle de la factura."""
        items_html = ""
        for item in pedido.get('items', []):
            subtotal = item['cantidad'] * item['precio_unitario']
            items_html += f"""
            <tr>
                <td>{item['titulo']}</td>
                <td style="text-align:center;">{item['cantidad']}</td>
                <td style="text-align:right;">${item['precio_unitario']:.2f}</td>
                <td style="text-align:right;">${subtotal:.2f}</td>
            </tr>
            """

        subtotal_total = sum(item['cantidad'] * item['precio_unitario'] for item in pedido.get('items', []))
        impuesto = round(subtotal_total * 0.13, 2)
        descuento = pedido.get('descuento', 0.0)
        total = pedido.get('total', subtotal_total + impuesto - descuento)

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                h1 {{ color: #0078d4; font-size: 24px; margin-bottom: 10px; }}
                p {{ margin: 4px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th {{ background-color: #0078d4; color: white; padding: 8px; text-align: left; }}
                td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
                .total {{ font-weight: bold; font-size: 16px; text-align: right; margin-top: 20px; }}
                .gracias {{ text-align: center; color: #777; margin-top: 30px; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h1>Factura #{pedido['id']}</h1>
            <p><strong>Fecha:</strong> {pedido.get('fecha', 'N/A')}</p>
            <p><strong>Cliente:</strong> {pedido.get('cliente', 'N/A')}</p>
            <p><strong>Estado:</strong> {pedido.get('estado', 'Pendiente')}</p>

            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th style="text-align:center;">Cantidad</th>
                        <th style="text-align:right;">Precio Unit.</th>
                        <th style="text-align:right;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>

            <p style="text-align:right;">Subtotal: ${subtotal_total:.2f}</p>
            <p style="text-align:right;">Impuesto (13%): ${impuesto:.2f}</p>
            {"<p style='text-align:right;'>Descuento: -$" + f"{descuento:.2f}" + "</p>" if descuento > 0 else ""}
            <p style="text-align:right; font-weight:bold;">Total: ${total:.2f}</p>

            <p class="gracias">Gracias por tu compra en Libros-Xpress</p>
            <p class="gracias">Este documento es una representación digital de tu factura.</p>
        </body>
        </html>
        """
        return html


# --- Prueba unitaria ---
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    # Crear aplicación Qt (necesaria para QPrinter)
    app = QApplication(sys.argv)

    # Datos de ejemplo
    pedido_ejemplo = {
        "id": 101,
        "fecha": "2026-05-07",
        "cliente": "admin",
        "estado": "Pendiente",
        "items": [
            {"titulo": "Cien años de soledad", "cantidad": 2, "precio_unitario": 19.99},
            {"titulo": "El principito", "cantidad": 1, "precio_unitario": 12.50}
        ],
        "descuento": 5.0,
        "total": 47.68
    }

    modelo_factura = FacturaModel("facturas")
    ruta_guardada = modelo_factura.generar_factura_pdf(pedido_ejemplo)

    print(f"✅ Prubea unitaria y Factura de prueba generada correctamente en: {ruta_guardada}")
    sys.exit()