"""
Módulo: catalogo_controller.py
Propósito: Controlador que conecta la vista del catálogo con el modelo de productos e integra el carrito.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.1.0 - Sprint 2 (Integración carrito)
"""

import sys
import os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QMessageBox
from src.models.producto_model import ProductoModel
from src.views.catalogo_view import CatalogoView


class CatalogoController:
    """
    Controlador del catálogo. Maneja las interacciones del usuario y la comunicación con el carrito.
    """

    def __init__(self, vista: CatalogoView, modelo: ProductoModel, carrito_ctrl):
        """
        Args:
            vista (CatalogoView): Instancia de la vista del catálogo.
            modelo (ProductoModel): Instancia del modelo de productos.
            carrito_ctrl: Instancia de CarritoController para agregar productos.
        """
        self.vista = vista
        self.modelo = modelo
        self.carrito_ctrl = carrito_ctrl
        self._configurar_senales()
        self._cargar_filtros()
        # Mostrar todos los productos al iniciar
        self.mostrar_todos()

    def _configurar_senales(self):
        """Conecta los eventos de la vista con los métodos del controlador."""
        self.vista.btn_buscar.clicked.connect(self.realizar_busqueda)
        self.vista.txt_busqueda.returnPressed.connect(self.realizar_busqueda)
        self.vista.btn_carrito.clicked.connect(self.abrir_carrito)

    def _cargar_filtros(self):
        """Carga los combos de autor y categoría desde el modelo."""
        try:
            autores = self.modelo.obtener_autores()
            categorias = self.modelo.obtener_categorias()
            self.vista.cargar_autores(autores)
            self.vista.cargar_categorias(categorias)
        except Exception as e:
            self.vista.mostrar_error("Error", f"No se pudieron cargar los filtros.\n{e}")

    def mostrar_todos(self):
        """Muestra todos los productos sin filtro."""
        try:
            productos = self.modelo.buscar()
            self.vista.mostrar_productos(productos, on_agregar=self.carrito_ctrl.agregar_al_carrito)
        except Exception as e:
            self.vista.mostrar_error("Error", f"No se pudo cargar el catálogo.\n{e}")

    def realizar_busqueda(self):
        """Ejecuta la búsqueda según los criterios ingresados y actualiza la vista."""
        try:
            texto = self.vista.obtener_texto_busqueda()
            autor_sel = self.vista.obtener_autor_seleccionado()
            categoria_sel = self.vista.obtener_categoria_seleccionada()

            autor = autor_sel if autor_sel != "Todos" else None
            categoria = categoria_sel if categoria_sel != "Todas" else None

            resultados = self.modelo.buscar(texto=texto, autor=autor, categoria=categoria)
            self.vista.mostrar_productos(resultados, on_agregar=self.carrito_ctrl.agregar_al_carrito)

            if not resultados:
                self.vista.mostrar_mensaje("Sin resultados", "No se encontraron productos con esos criterios.")
        except Exception as e:
            self.vista.mostrar_error("Error en la búsqueda", f"Ocurrió un error: {e}")

    def abrir_carrito(self):
        """Abre la ventana del carrito y actualiza su contenido."""
        self.carrito_ctrl.vista.show()
        self.carrito_ctrl.actualizar_vista()


# --- Prueba del controlador (simulación con mock del carrito) ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    import tempfile
    import json
    import os

    # Arrange: datos de productos temporales
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

    # Mock del carrito controller: simula tener el método agregar_al_carrito
    class MockCarritoCtrl:
        def __init__(self):
            self.agregados = []
        def agregar_al_carrito(self, titulo, precio):
            self.agregados.append((titulo, precio))
        def actualizar_vista(self):
            pass
        # La vista del carrito no se usa en la prueba, se puede omitir
        vista = None

    mock_carrito = MockCarritoCtrl()
    controlador = CatalogoController(vista, modelo, mock_carrito)

    # Act - simular una búsqueda automática
    vista.txt_busqueda.setText("Python")
    controlador.realizar_busqueda()

    # Assert: la vista debe tener al menos un widget (el producto encontrado)
    assert vista.scroll_layout.count() > 0, "Debería haber al menos un widget en la vista"
    print("✅ Prueba del controlador: búsqueda ejecutada y vista actualizada.")

    # Limpiar archivo temporal
    os.unlink(ruta_tmp)
    sys.exit()