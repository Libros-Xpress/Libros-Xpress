"""
Módulo: catalogo_controller.py
Propósito: Controlador que conecta la vista del catálogo con el modelo de productos.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from PySide6.QtWidgets import QMessageBox
from src.models.producto_model import ProductoModel
from src.views.catalogo_view import CatalogoView

class CatalogoController:
    """
    Controlador del catálogo. Maneja las interacciones del usuario y actualiza la vista.
    """

    def __init__(self, vista: CatalogoView, modelo: ProductoModel):
        """
        Args:
            vista (CatalogoView): Instancia de la vista del catálogo.
            modelo (ProductoModel): Instancia del modelo de productos.
        """
        self.vista = vista
        self.modelo = modelo
        self._configurar_senales()
        self._cargar_filtros()

    def _configurar_senales(self):
        """Conecta los eventos de la vista con los métodos del controlador."""
        self.vista.btn_buscar.clicked.connect(self.realizar_busqueda)
        self.vista.txt_busqueda.returnPressed.connect(self.realizar_busqueda)

    def _cargar_filtros(self):
        """Carga los combos de autor y categoría desde el modelo."""
        try:
            autores = self.modelo.obtener_autores()
            categorias = self.modelo.obtener_categorias()
            self.vista.cargar_autores(autores)
            self.vista.cargar_categorias(categorias)
        except Exception as e:
            self.vista.mostrar_error("Error", f"No se pudieron cargar los filtros.\n{e}")

    def realizar_busqueda(self):
        """Ejecuta la búsqueda según los criterios ingresados y actualiza la vista."""
        try:
            texto = self.vista.obtener_texto_busqueda()
            autor_sel = self.vista.obtener_autor_seleccionado()
            categoria_sel = self.vista.obtener_categoria_seleccionada()

            # Convertir "Todos" o "Todas" a None para que el modelo ignore ese filtro
            autor = autor_sel if autor_sel != "Todos" else None
            categoria = categoria_sel if categoria_sel != "Todas" else None

            resultados = self.modelo.buscar(texto=texto, autor=autor, categoria=categoria)
            self.vista.mostrar_productos(resultados)

            if not resultados:
                self.vista.mostrar_mensaje("Sin resultados", "No se encontraron productos con esos criterios.")
        except Exception as e:
            self.vista.mostrar_error("Error en la búsqueda", f"Ocurrió un error: {e}")


# --- Prueba del controlador (simulación) ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    import tempfile
    import json
    import os

    # Arrange
    datos = {
        "productos": [
            {"id": 1, "titulo": "Python Avanzado", "autor": "Guido", "categoria": "Programación", "precio": 35.0, "portada": ""},
            {"id": 2, "titulo": "PySide6 Guía", "autor": "Qt", "categoria": "Programación", "precio": 29.99, "portada": ""}
        ]
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    app = QApplication(sys.argv)
    vista = CatalogoView()
    modelo = ProductoModel(ruta_tmp)
    controlador = CatalogoController(vista, modelo)

    # Act - simular una búsqueda automática
    vista.txt_busqueda.setText("Python")
    controlador.realizar_busqueda()

    # Assert básico: verificar que la vista tenga al menos un producto en el layout
    assert vista.scroll_layout.count() > 0, "Debería haber al menos un widget en la vista"
    print("✅ Prueba del controlador: búsqueda ejecutada y vista actualizada.")

    # Limpiar
    os.unlink(ruta_tmp)
    sys.exit()