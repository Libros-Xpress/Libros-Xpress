"""
Módulo: admin_productos_controller.py
Propósito: Controlador para el panel de administración de productos (CRUD).
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
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
        """
        Args:
            vista: AdminProductosView
            modelo: ProductoModel (compartido con catálogo)
            refresh_callback: Función a llamar para refrescar el catálogo después de cambios.
        """
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
        """Carga todos los productos en la tabla de la vista."""
        self.vista.cargar_productos(self.modelo.productos)

    def nuevo_producto(self):
        """Abre diálogo para crear un nuevo producto."""
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
        """Edita el producto seleccionado."""
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
        """Elimina el producto seleccionado."""
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


# --- Prueba simulada del controlador ---
if __name__ == "__main__":
    import tempfile, json

    app = QApplication(sys.argv)

    # Arrange: crear JSON temporal con un producto
    datos = {"productos": [{"id": 1, "titulo": "Test", "autor": "A", "categoria": "C", "precio": 5.0, "portada": ""}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    modelo = ProductoModel(ruta_tmp)
    vista = AdminProductosView()
    vista.show()
    # Mock de mensajes para evitar bloqueos
    vista.mostrar_mensaje = lambda titulo, mensaje: print(f"ℹ️ {titulo}: {mensaje}")
    vista.mostrar_error = lambda titulo, mensaje: print(f"❌ {titulo}: {mensaje}")

    # Flag como lista para evitar problema de nonlocal
    refresh_llamado = [False]
    def refresh_mock():
        refresh_llamado[0] = True

    controlador = AdminProductosController(vista, modelo, refresh_callback=refresh_mock)

    # Act - Agregar producto (simulamos directamente con modelo, luego refrescamos)
    modelo.agregar_producto("Nuevo", "B", "D", 10.0, "")
    controlador.cargar_tabla()
    assert vista.tabla.rowCount() == 2, "Debería haber 2 filas"

    # Eliminar el segundo producto
    vista.tabla.selectRow(1)
    controlador.eliminar_producto()
    assert vista.tabla.rowCount() == 1

    # Editar el primero
    vista.tabla.selectRow(0)
    modelo.actualizar_producto(1, "Test Mod", "A", "C", 7.5, "")
    controlador.cargar_tabla()
    assert vista.tabla.item(0, 4).text() == "$7.50", "El precio no se actualizó correctamente"

    # Verificar que el callback se llamó al menos una vez
    assert refresh_llamado[0], "El callback de refresco no fue invocado"

    os.unlink(ruta_tmp)
    print("✅ Prueba del controlador de administración pasó correctamente.")
    app.quit()
    sys.exit()