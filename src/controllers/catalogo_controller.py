"""
Módulo: catalogo_controller.py
Propósito: Controlador del catálogo con integración al carrito y panel de administración.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.2.0 - Sprint 2 (Panel de administración)
"""

import sys
import os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication
from src.models.producto_model import ProductoModel
from src.views.catalogo_view import CatalogoView


class CatalogoController:
    """
    Controlador del catálogo. Maneja las interacciones del usuario y la comunicación con el carrito y panel admin.
    """

    def __init__(self, vista: CatalogoView, modelo: ProductoModel, carrito_ctrl, admin_ctrl=None, es_admin=False):
        """
        Args:
            vista (CatalogoView): Instancia de la vista del catálogo.
            modelo (ProductoModel): Instancia del modelo de productos.
            carrito_ctrl: Instancia de CarritoController para agregar productos.
            admin_ctrl: Instancia de AdminProductosController (opcional, solo si es admin).
            es_admin (bool): Indica si el usuario actual es administrador.
        """
        self.vista = vista
        self.modelo = modelo
        self.carrito_ctrl = carrito_ctrl
        self.admin_ctrl = admin_ctrl
        self.es_admin = es_admin
        self._configurar_senales()
        self._cargar_filtros()
        # Mostrar el botón de panel admin si corresponde
        if self.es_admin:
            self.vista.btn_admin.setVisible(True)
        self.mostrar_todos()

    def _configurar_senales(self):
        """Conecta los eventos de la vista con los métodos del controlador."""
        self.vista.btn_buscar.clicked.connect(self.realizar_busqueda)
        self.vista.txt_busqueda.returnPressed.connect(self.realizar_busqueda)
        self.vista.btn_carrito.clicked.connect(self.abrir_carrito)
        if self.es_admin and self.admin_ctrl:
            self.vista.btn_admin.clicked.connect(self.abrir_admin)

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

    def abrir_admin(self):
        """Abre la ventana de administración de productos."""
        if self.admin_ctrl:
            self.admin_ctrl.vista.show()
            self.admin_ctrl.cargar_tabla()


# --- Prueba del controlador (simulación con mocks del carrito y admin) ---
if __name__ == "__main__":
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
    vista.show()  # Necesario para que los widgets hijos reflejen visibilidad real
    modelo = ProductoModel(ruta_tmp)

    # Mock del carrito controller
    class MockCarritoCtrl:
        def __init__(self):
            self.agregados = []
        def agregar_al_carrito(self, titulo, precio):
            self.agregados.append((titulo, precio))
        def actualizar_vista(self):
            pass
        vista = None

    mock_carrito = MockCarritoCtrl()

    # Mock del admin controller (para probar que se inicialice correctamente)
    class MockAdminCtrl:
        def __init__(self):
            self.abierto = False
        def cargar_tabla(self):
            pass
        def vista(self):
            pass

    mock_admin = MockAdminCtrl()

    # Act: instanciar controlador con admin
    controlador = CatalogoController(vista, modelo, mock_carrito, admin_ctrl=mock_admin, es_admin=True)
    app.processEvents()  # Procesar eventos para actualizar la UI

    # Assert: el botón admin debe estar visible
    assert vista.btn_admin.isVisible(), "El botón Panel Admin debe estar visible para administradores"
    print("✅ Prueba del controlador con panel admin: botón visible y controlador iniciado correctamente.")

    # Limpiar archivo temporal
    os.unlink(ruta_tmp)
    vista.close()
    app.quit()
    sys.exit()