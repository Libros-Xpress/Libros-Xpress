import sys, os, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QFileDialog
from src.views.admin_productos_view import AdminProductosView, ProductoDialog

app = QApplication.instance() or QApplication(sys.argv)

# ─── Datos falsos ───
class Prod:
    def __init__(self, i, t, a, c, p, po, s=0):
        self.id, self.titulo, self.autor, self.categoria, self.precio, self.portada, self.stock = i, t, a, c, p, po, s

# ─── Pruebas de la vista AdminProductosView ───
def test_admin_crear_vista():
    vista = AdminProductosView()
    assert vista.windowTitle() == "Administrar Productos – Libros/Xpress"
    vista.close()

def test_admin_cargar_productos():
    vista = AdminProductosView()
    vista.cargar_productos([
        Prod(1, "Libro A", "Autor A", "Cat A", 25.0, "", 10),
        Prod(2, "Libro B", "Autor B", "Cat B", 15.0, "", 3)
    ])
    assert vista.tabla.rowCount() == 2
    assert vista.tabla.item(0, 1).text() == "Libro A"
    assert vista.tabla.item(0, 4).text() == "$25.00"
    vista.close()

def test_admin_obtener_seleccionado():
    vista = AdminProductosView()
    vista.cargar_productos([Prod(1, "Test", "Autor", "Cat", 9.99, "img.png")])
    vista.tabla.selectRow(0)
    sel = vista.obtener_producto_seleccionado()
    assert sel["id"] == 1
    assert sel["titulo"] == "Test"
    assert sel["portada"] == "img.png"
    vista.close()

def test_admin_sin_seleccion():
    vista = AdminProductosView()
    vista.cargar_productos([Prod(1, "X", "Y", "Z", 0, "")])
    # No seleccionamos nada
    assert vista.obtener_producto_seleccionado() is None
    vista.close()

def test_admin_mensajes():
    vista = AdminProductosView()
    # Mostrar mensajes (no lanzan excepciones)
    vista.mostrar_mensaje("OK", "Todo bien")
    vista.mostrar_error("Error", "Algo malo")
    vista.cerrar()
    vista.close()

# ─── Pruebas del diálogo ProductoDialog ───
def test_dialog_nuevo():
    dlg = ProductoDialog()
    assert dlg.windowTitle() == "Nuevo Producto"
    dlg.txt_titulo.setText("Nuevo Libro")
    dlg.txt_autor.setText("Autor X")
    dlg.txt_categoria.setText("Cat X")
    dlg.spin_precio.setValue(12.99)
    dlg.txt_portada.setText("assets/img/portada.jpg")
    datos = dlg.obtener_datos()
    assert datos["titulo"] == "Nuevo Libro"
    assert datos["precio"] == 12.99
    assert datos["portada"] == "assets/img/portada.jpg"
    dlg.close()

def test_dialog_editar():
    datos_iniciales = {
        "titulo": "Libro Viejo", "autor": "Autor Viejo",
        "categoria": "Cat Vieja", "precio": 7.5, "portada": ""
    }
    dlg = ProductoDialog(datos_iniciales)
    assert dlg.windowTitle() == "Editar Producto"
    datos = dlg.obtener_datos()
    assert datos["titulo"] == "Libro Viejo"
    assert datos["precio"] == 7.5
    dlg.close()

def test_dialog_seleccionar_portada(monkeypatch):
    """Simula la selección de un archivo de imagen."""
    dlg = ProductoDialog()
    # Mock de QFileDialog.getOpenFileName
    def mock_get_open_file_name(*args, **kwargs):
        return (os.path.join(os.getcwd(), "assets", "img", "test.jpg"), "Imágenes (*.jpg)")
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_get_open_file_name)

    # Llamamos al método interno que selecciona la portada
    dlg.seleccionar_portada()
    ruta = dlg.txt_portada.text()
    assert "assets" in ruta
    assert "test.jpg" in ruta
    dlg.close()

def test_dialog_actualizar_preview():
    dlg = ProductoDialog()
    # Si no hay ruta válida, muestra texto "Sin imagen"
    dlg.txt_portada.setText("")
    dlg._actualizar_preview()
    assert dlg.lbl_preview.text() == "Sin imagen"
    dlg.close()

def test_dialog_cancelar():
    dlg = ProductoDialog()
    dlg.reject()  # simula clic en Cancelar
    # No debe lanzar errores
    dlg.close()