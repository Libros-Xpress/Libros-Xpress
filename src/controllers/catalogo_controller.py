"""
Módulo: catalogo_controller.py
Propósito: Controlador del catálogo con integración al carrito, panel admin, historial y venta física.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.4.0 - Sprint 4 (Sincronización de stock)
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
    Controlador del catálogo. Maneja las interacciones del usuario y la comunicación con el carrito, panel admin, historial y venta física.
    """

    def __init__(self, vista: CatalogoView, modelo: ProductoModel, carrito_ctrl,
                 admin_ctrl=None, es_admin=False, usuario_actual="", historial_ctrl=None,
                 venta_fisica_ctrl=None):
        """
        Args:
            vista (CatalogoView): Instancia de la vista del catálogo.
            modelo (ProductoModel): Instancia del modelo de productos.
            carrito_ctrl: Instancia de CarritoController para agregar productos.
            admin_ctrl: Instancia de AdminProductosController (opcional, solo si es admin).
            es_admin (bool): Indica si el usuario actual es administrador.
            usuario_actual (str): Nombre del usuario autenticado.
            historial_ctrl: Instancia de HistorialController (opcional).
            venta_fisica_ctrl: Instancia de VentaFisicaController (opcional, solo admin).
        """
        self.vista = vista
        self.modelo = modelo
        self.carrito_ctrl = carrito_ctrl
        self.admin_ctrl = admin_ctrl
        self.es_admin = es_admin
        self.usuario_actual = usuario_actual
        self.historial_ctrl = historial_ctrl
        self.venta_fisica_ctrl = venta_fisica_ctrl
        self._configurar_senales()
        self._cargar_filtros()
        # Mostrar botones de administrador si corresponde
        if self.es_admin:
            self.vista.btn_admin.setVisible(True)
            self.vista.btn_venta_fisica.setVisible(True)
        self.mostrar_todos()

    def _configurar_senales(self):
        """Conecta los eventos de la vista con los métodos del controlador."""
        self.vista.btn_buscar.clicked.connect(self.realizar_busqueda)
        self.vista.txt_busqueda.returnPressed.connect(self.realizar_busqueda)
        self.vista.btn_carrito.clicked.connect(self.abrir_carrito)
        if self.es_admin and self.admin_ctrl:
            self.vista.btn_admin.clicked.connect(self.abrir_admin)
        if self.es_admin and self.venta_fisica_ctrl:
            self.vista.btn_venta_fisica.clicked.connect(self.abrir_venta_fisica)
        if hasattr(self.vista, 'btn_historial'):
            self.vista.btn_historial.clicked.connect(self.abrir_historial)

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

    def abrir_historial(self):
        """Abre la ventana de historial de pedidos del usuario actual."""
        if self.historial_ctrl:
            self.historial_ctrl.vista.show()
            self.historial_ctrl.cargar_historial(self.usuario_actual)

    def abrir_venta_fisica(self):
        """Abre la ventana de venta física para registrar una venta presencial."""
        if self.venta_fisica_ctrl:
            self.venta_fisica_ctrl.vista.show()
            self.venta_fisica_ctrl.cargar_productos()


# --- Prueba del controlador (simulación con mocks del carrito, admin, historial y venta física) ---
if __name__ == "__main__":
    import tempfile
    import json
    import os

    # Arrange: datos de productos temporales
    datos = {
        "productos": [
            {"id": 1, "titulo": "Python Avanzado", "autor": "Guido", "categoria": "Programación", "precio": 35.0, "portada": "", "stock": 5},
            {"id": 2, "titulo": "PySide6 Guía", "autor": "Qt", "categoria": "Programación", "precio": 29.99, "portada": "", "stock": 3}
        ]
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    app = QApplication(sys.argv)
    vista = CatalogoView()
    vista.show()
    modelo = ProductoModel(ruta_tmp)

    # Mocks necesarios
    class MockCarritoCtrl:
        def __init__(self):
            self.agregados = []
        def agregar_al_carrito(self, titulo, precio):
            self.agregados.append((titulo, precio))
        def actualizar_vista(self):
            pass
        vista = None

    class MockAdminCtrl:
        def __init__(self):
            self.abierto = False
        def cargar_tabla(self):
            pass
        def vista(self):
            pass

    class MockVista:
        def show(self):
            pass

    class MockHistorialCtrl:
        def __init__(self):
            self.vista = MockVista()
            self.abierto = False
            self.usuario = ""
        def cargar_historial(self, usuario):
            self.abierto = True
            self.usuario = usuario

    class MockVentaFisicaCtrl:
        def __init__(self):
            self.vista = MockVista()
            self.abierto = False
        def cargar_productos(self):
            self.abierto = True

    mock_carrito = MockCarritoCtrl()
    mock_admin = MockAdminCtrl()
    mock_historial = MockHistorialCtrl()
    mock_venta_fisica = MockVentaFisicaCtrl()

    # Act: instanciar controlador con todos los módulos
    controlador = CatalogoController(
        vista, modelo, mock_carrito,
        admin_ctrl=mock_admin, es_admin=True,
        usuario_actual="test_user", historial_ctrl=mock_historial,
        venta_fisica_ctrl=mock_venta_fisica
    )
    app.processEvents()

    # Assert: botones de admin visibles
    assert vista.btn_admin.isVisible(), "El botón Panel Admin debe estar visible"
    assert vista.btn_venta_fisica.isVisible(), "El botón Venta Física debe estar visible"
    # Probar apertura de venta física
    controlador.abrir_venta_fisica()
    assert mock_venta_fisica.abierto, "La ventana de venta física debió abrirse"
    # Probar historial
    controlador.abrir_historial()
    assert mock_historial.abierto, "El historial debió abrirse"
    print("✅ Prueba del controlador con venta física e historial: todo correcto.")

    os.unlink(ruta_tmp)
    vista.close()
    app.quit()
    sys.exit()