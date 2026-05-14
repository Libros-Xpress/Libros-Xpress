"""
Módulo: admin_productos_controller.py
Propósito: Controlador para el panel de administración de productos (CRUD) con gestión de stock.
Autor: Robert Cerón
Versión: 2.0.1 – Corrección de stock
"""

import sys
import os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication
from src.models.producto_model import ProductoModel
from src.views.admin_productos_view import AdminProductosView, ProductoDialog

class AdminProductosController:
    """Controlador para gestionar productos desde el panel de administración."""

    def __init__(self, vista: AdminProductosView, modelo: ProductoModel, refresh_callback=None):
        self.vista = vista
        self.modelo = modelo
        self.refresh_callback = refresh_callback
        self._configurar_senales()
        self.cargar_tabla()

    def _configurar_senales(self):
        self.vista.btn_nuevo.clicked.connect(self.nuevo_producto)
        self.vista.btn_editar.clicked.connect(self.editar_producto)
        self.vista.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.vista.btn_refrescar.clicked.connect(self.cargar_tabla)
        self.vista.btn_cerrar.clicked.connect(self.vista.cerrar)

    def cargar_tabla(self):
        self.vista.cargar_productos(self.modelo.productos)

    def nuevo_producto(self):
        dialogo = ProductoDialog(parent=self.vista)
        if dialogo.exec() == ProductoDialog.Accepted:
            datos = dialogo.obtener_datos()
            if not datos["titulo"] or not datos["autor"] or not datos["categoria"]:
                self.vista.mostrar_error("Campos incompletos", "Título, autor y categoría son obligatorios.")
                return
            try:
                self.modelo.agregar_producto(**datos)
                self.cargar_tabla()
                if self.refresh_callback:
                    self.refresh_callback()
                self.vista.mostrar_mensaje("Éxito", "Producto agregado correctamente.")
            except Exception as e:
                self.vista.mostrar_error("Error", str(e))

    def editar_producto(self):
        seleccion = self.vista.obtener_producto_seleccionado()
        if not seleccion:
            self.vista.mostrar_error("Seleccione producto", "Debe seleccionar un producto para editar.")
            return
        dialogo = ProductoDialog(seleccion, parent=self.vista)
        if dialogo.exec() == ProductoDialog.Accepted:
            datos = dialogo.obtener_datos()
            if not datos["titulo"] or not datos["autor"] or not datos["categoria"]:
                self.vista.mostrar_error("Campos incompletos", "Título, autor y categoría son obligatorios.")
                return
            try:
                ok = self.modelo.actualizar_producto(seleccion["id"], **datos)
                if ok:
                    self.cargar_tabla()
                    if self.refresh_callback:
                        self.refresh_callback()
                    self.vista.mostrar_mensaje("Éxito", "Producto actualizado.")
                else:
                    self.vista.mostrar_error("Error", "No se encontró el producto.")
            except Exception as e:
                self.vista.mostrar_error("Error", str(e))

    def eliminar_producto(self):
        seleccion = self.vista.obtener_producto_seleccionado()
        if not seleccion:
            self.vista.mostrar_error("Seleccione producto", "Debe seleccionar un producto para eliminar.")
            return
        try:
            ok = self.modelo.eliminar_producto(seleccion["id"])
            if ok:
                self.cargar_tabla()
                if self.refresh_callback:
                    self.refresh_callback()
                self.vista.mostrar_mensaje("Éxito", "Producto eliminado.")
            else:
                self.vista.mostrar_error("Error", "No se pudo eliminar el producto.")
        except Exception as e:
            self.vista.mostrar_error("Error", str(e))


# --- Prueba simulada del controlador (con stock) ---
if __name__ == "__main__":
    import tempfile, json

    app = QApplication(sys.argv)

    datos = {"productos": [{"id": 1, "titulo": "Test", "autor": "A", "categoria": "C", "precio": 5.0, "portada": "", "stock": 5}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    modelo = ProductoModel(ruta_tmp)
    vista = AdminProductosView()
    vista.show()
    vista.mostrar_mensaje = lambda t, m: print(f"i {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"x {t}: {m}")

    refresh_llamado = [False]
    def refresh_mock():
        refresh_llamado[0] = True

    controlador = AdminProductosController(vista, modelo, refresh_callback=refresh_mock)

    # Agregar producto con stock
    modelo.agregar_producto("Nuevo", "B", "D", 10.0, "", stock=10)
    controlador.cargar_tabla()
    assert vista.tabla.rowCount() == 2
    assert vista.tabla.item(1, 5).text() == "10"  # columna stock del nuevo producto

    # Editar stock
    vista.tabla.selectRow(0)
    modelo.actualizar_producto(1, "Test Mod", "A", "C", 7.5, "", stock=3)
    controlador.cargar_tabla()
    assert vista.tabla.item(0, 5).text() == "3"

    # Eliminar
    vista.tabla.selectRow(1)
    controlador.eliminar_producto()
    assert vista.tabla.rowCount() == 1

    assert refresh_llamado[0]

    os.unlink(ruta_tmp)
    print("Prueba del controlador de administración con stock pasó correctamente.")
    app.quit()
    sys.exit()