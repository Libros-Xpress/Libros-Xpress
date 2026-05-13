import sys, os, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QInputDialog
from src.controllers.auth_controller import AuthController
from src.controllers.catalogo_controller import CatalogoController
from src.controllers.carrito_controller import CarritoController
from src.controllers.admin_productos_controller import AdminProductosController
from src.controllers.historial_controller import HistorialController
from src.controllers.venta_fisica_controller import VentaFisicaController
from src.models.usuario_model import UsuarioModel
from src.models.producto_model import ProductoModel
from src.models.carrito_model import Carrito, PedidoModel
from src.models.cupon_model import CuponModel
from src.views.login_view import LoginView
from src.views.catalogo_view import CatalogoView
from src.views.carrito_view import CarritoView
from src.views.admin_productos_view import AdminProductosView
from src.views.historial_view import HistorialView
from src.views.venta_fisica_view import VentaFisicaView

app = QApplication.instance() or QApplication(sys.argv)

# --- Auth ---
def test_auth_controller_login():
    datos = {"usuarios": [{"username":"admin","password":"123","rol":"Admin"}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    modelo = UsuarioModel(ruta)
    vista = LoginView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = AuthController(vista, modelo)
    vista.txt_usuario_login.setText("admin")
    vista.txt_password_login.setText("123")
    vista.btn_login.clicked.emit()
    assert ctrl.usuario_actual == "admin"
    assert ctrl.rol_actual == "Admin"
    os.unlink(ruta)

def test_auth_controller_registro():
    datos = {"usuarios": []}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    modelo = UsuarioModel(ruta)
    vista = LoginView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = AuthController(vista, modelo)
    # Simular registro exitoso
    vista.txt_usuario_reg.setText("nuevo")
    vista.txt_password_reg.setText("abc")
    vista.txt_password_confirm.setText("abc")
    vista.txt_email_reg.setText("test@mail.com")
    vista.cmb_rol.setCurrentText("Cliente")
    vista.btn_registrar.clicked.emit()
    assert modelo.existe_usuario("nuevo")
    os.unlink(ruta)

def test_auth_controller_recuperar():
    datos = {"usuarios": []}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    modelo = UsuarioModel(ruta)
    vista = LoginView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = AuthController(vista, modelo)
    # Mock de QInputDialog.getText
    original = QInputDialog.getText
    QInputDialog.getText = lambda *args, **kwargs: ("test@mail.com", True)
    ctrl.recuperar_contrasena()
    QInputDialog.getText = original  # restaurar
    os.unlink(ruta)

# --- Catálogo ---
def test_catalogo_controller_init():
    datos = {"productos": [{"id":1,"titulo":"Test","autor":"A","categoria":"C","precio":10.0,"portada":"","stock":5}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    modelo = ProductoModel(ruta)
    vista = CatalogoView()
    carrito = Carrito()
    pedido_model = PedidoModel("data/pedidos.json")
    vista_carrito = CarritoView()
    carrito_ctrl = CarritoController(vista_carrito, carrito, pedido_model, "test")
    ctrl = CatalogoController(vista, modelo, carrito_ctrl, es_admin=True, usuario_actual="test")
    assert ctrl.es_admin == True
    assert ctrl.usuario_actual == "test"
    os.unlink(ruta)

def test_catalogo_busqueda():
    datos = {"productos": [{"id":1,"titulo":"Libro X","autor":"A","categoria":"C","precio":10.0,"portada":"","stock":5}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    modelo = ProductoModel(ruta)
    vista = CatalogoView()
    carrito = Carrito()
    pedido_model = PedidoModel("data/pedidos.json")
    vista_carrito = CarritoView()
    carrito_ctrl = CarritoController(vista_carrito, carrito, pedido_model, "test")
    ctrl = CatalogoController(vista, modelo, carrito_ctrl, es_admin=True, usuario_actual="test")
    vista.txt_busqueda.setText("Libro")
    ctrl.realizar_busqueda()
    assert vista.scroll_layout.count() > 0
    os.unlink(ruta)

# --- Carrito ---
def test_carrito_controller_agregar():
    datos = {"pedidos": []}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    carrito = Carrito()
    pedido_model = PedidoModel(ruta)
    vista = CarritoView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = CarritoController(vista, carrito, pedido_model, "test")
    ctrl.agregar_al_carrito("Libro", 10.0)
    assert not carrito.esta_vacio()
    assert carrito.total() == 10.0
    os.unlink(ruta)

def test_carrito_aplicar_cupon():
    datos_pedidos = {"pedidos": []}
    datos_cupones = {"cupones": [{"codigo":"DESC10","tipo":"porcentaje","valor":10,"activo":True}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_pedidos, tmp); ruta_ped = tmp.name
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_cupones, tmp); ruta_cup = tmp.name
    carrito = Carrito()
    pedido_model = PedidoModel(ruta_ped)
    cupon_model = CuponModel(ruta_cup)
    vista = CarritoView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = CarritoController(vista, carrito, pedido_model, "test", cupon_model)
    ctrl.agregar_al_carrito("Libro", 25.0)
    vista.txt_cupon.setText("DESC10")
    vista.btn_aplicar_cupon.clicked.emit()
    assert ctrl.descuento_aplicado > 0
    os.unlink(ruta_ped)
    os.unlink(ruta_cup)

# --- Admin Productos ---
def test_admin_controller():
    datos = {"productos": []}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    modelo = ProductoModel(ruta)
    vista = AdminProductosView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = AdminProductosController(vista, modelo)
    modelo.agregar_producto("Test","A","C",5.0,"",10)
    ctrl.cargar_tabla()
    assert vista.tabla.rowCount() == 1
    vista.tabla.selectRow(0)
    ctrl.eliminar_producto()
    assert len(modelo.productos) == 0
    os.unlink(ruta)

# --- Historial ---
def test_historial_controller():
    datos = {"pedidos": [{"id":1,"fecha":"2026-05-01","cliente":"test","total":20.0,"estado":"Pendiente","items":[]}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp); ruta = tmp.name
    modelo = PedidoModel(ruta)
    vista = HistorialView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = HistorialController(vista, modelo)
    ctrl.cargar_historial("test")
    assert vista.tabla.rowCount() == 1
    os.unlink(ruta)

# --- Venta Física ---
def test_venta_fisica_controller():
    datos_prod = {"productos": [{"id":1,"titulo":"Libro","autor":"A","categoria":"C","precio":10.0,"portada":"","stock":5}]}
    datos_ped = {"pedidos": []}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_prod, tmp); ruta_prod = tmp.name
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos_ped, tmp); ruta_ped = tmp.name
    modelo_prod = ProductoModel(ruta_prod)
    modelo_ped = PedidoModel(ruta_ped)
    vista = VentaFisicaView()
    vista.mostrar_mensaje = lambda t, m: None
    vista.mostrar_error = lambda t, m: None
    ctrl = VentaFisicaController(vista, modelo_prod, modelo_ped, "test")
    # Simular selección de producto y venta
    vista.cmb_producto.setCurrentIndex(0)
    vista.spin_cantidad.setValue(2)
    vista.btn_registrar.clicked.emit()
    assert modelo_prod.productos[0].stock == 3
    assert len(modelo_ped.pedidos) == 1
    os.unlink(ruta_prod)
    os.unlink(ruta_ped)