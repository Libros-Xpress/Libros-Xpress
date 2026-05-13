import sys, os, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.models.usuario_model import UsuarioModel
from src.views.login_view import LoginView
from src.controllers.auth_controller import AuthController
from src.views.catalogo_view import CatalogoView
from src.controllers.catalogo_controller import CatalogoController
from src.models.producto_model import ProductoModel
from src.models.carrito_model import Carrito, PedidoModel
from src.views.carrito_view import CarritoView
from src.controllers.carrito_controller import CarritoController

def _crear_app():
    return QApplication.instance() or QApplication(sys.argv)

def _temp_json(datos):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(datos, f)
        return f.name

def _login(qtbot, usuario, password, rol="Admin"):
    datos_usu = {"usuarios": [{"username": usuario, "password": password, "rol": rol}]}
    ruta = _temp_json(datos_usu)
    modelo = UsuarioModel(ruta)
    vista = LoginView()
    auth = AuthController(vista, modelo)
    vista.mostrar_mensaje = lambda t, m: print(f"[LOG] {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"[LOG ERROR] {t}: {m}")
    qtbot.addWidget(vista)
    vista.show()
    qtbot.keyClicks(vista.txt_usuario_login, usuario)
    qtbot.wait(200)
    qtbot.keyClicks(vista.txt_password_login, password)
    qtbot.wait(200)
    qtbot.mouseClick(vista.btn_login, Qt.LeftButton)
    qtbot.wait(200)
    qtbot.waitUntil(lambda: not vista.isVisible(), timeout=5000)
    os.unlink(ruta)
    return auth

def _setup_catalogo(qtbot, auth_ctrl, productos=None):
    if productos is None:
        productos = [{"id":1,"titulo":"Libro Test","autor":"A","categoria":"C","precio":20.0,"portada":"","stock":5}]
    ruta_prod = _temp_json({"productos": productos})
    ruta_ped = _temp_json({"pedidos": []})
    modelo_prod = ProductoModel(ruta_prod)
    carrito = Carrito()
    pedido_model = PedidoModel(ruta_ped)
    vista_carrito = CarritoView()
    carrito_ctrl = CarritoController(vista_carrito, carrito, pedido_model, auth_ctrl.usuario_actual)
    vista_carrito.mostrar_mensaje = lambda t, m: print(f"[CARRITO] {t}: {m}")
    vista_carrito.mostrar_error = lambda t, m: print(f"[CARRITO ERROR] {t}: {m}")
    vista_catalogo = CatalogoView()
    catalogo_ctrl = CatalogoController(vista_catalogo, modelo_prod, carrito_ctrl,
                                       es_admin=(auth_ctrl.rol_actual == "Admin"),
                                       usuario_actual=auth_ctrl.usuario_actual)
    qtbot.addWidget(vista_catalogo)
    vista_catalogo.show()
    return vista_catalogo, carrito_ctrl, vista_carrito, ruta_prod, ruta_ped

def test_flujo_admin(qtbot):
    app = _crear_app()
    auth = _login(qtbot, "admin", "123", "Admin")
    assert auth.usuario_actual == "admin"
    assert auth.rol_actual == "Admin"
    vista_catalogo, _, _, ruta_prod, ruta_ped = _setup_catalogo(qtbot, auth)
    qtbot.wait(300)
    assert vista_catalogo.btn_admin.isVisible()
    assert vista_catalogo.btn_venta_fisica.isVisible()
    print("[ROBOT] Flujo admin verificado.")
    vista_catalogo.close()
    os.unlink(ruta_prod)
    os.unlink(ruta_ped)

def test_flujo_cliente(qtbot):
    app = _crear_app()
    auth = _login(qtbot, "cliente", "abc", "Cliente")
    assert auth.rol_actual == "Cliente"
    productos = [{"id":1,"titulo":"Libro Cliente","autor":"B","categoria":"D","precio":10.0,"portada":"","stock":3}]
    vista_catalogo, carrito_ctrl, vista_carrito, ruta_prod, ruta_ped = _setup_catalogo(qtbot, auth, productos)
    qtbot.wait(300)
    assert not vista_catalogo.btn_admin.isVisible()
    assert not vista_catalogo.btn_venta_fisica.isVisible()
    carrito_ctrl.agregar_al_carrito("Libro Cliente", 10.0)
    qtbot.wait(200)
    assert not carrito_ctrl.carrito.esta_vacio()
    vista_carrito.show()
    qtbot.waitUntil(lambda: vista_carrito.isVisible(), timeout=3000)
    assert vista_carrito.tabla.rowCount() == 1
    vista_carrito.close()
    vista_catalogo.close()
    os.unlink(ruta_prod)
    os.unlink(ruta_ped)
    print("[ROBOT] Flujo cliente verificado.")

def test_carrito_y_cupon(qtbot):
    app = _crear_app()
    auth = _login(qtbot, "admin", "123", "Admin")
    _, carrito_ctrl, vista_carrito, ruta_prod, ruta_ped = _setup_catalogo(qtbot, auth)
    carrito_ctrl.agregar_al_carrito("Libro Test", 20.0)
    carrito_ctrl.agregar_al_carrito("Libro Test", 20.0)
    vista_carrito.show()
    qtbot.wait(200)
    vista_carrito.txt_cupon.setText("DESC10")
    vista_carrito.btn_aplicar_cupon.clicked.emit()
    qtbot.waitUntil(lambda: vista_carrito.lbl_descuento.isVisible(), timeout=5000)
    assert "Descuento" in vista_carrito.lbl_descuento.text()
    total_final = float(vista_carrito.lbl_total.text().replace("Total: $",""))
    assert total_final < carrito_ctrl.carrito.total_con_impuesto()
    vista_carrito.close()
    os.unlink(ruta_prod)
    os.unlink(ruta_ped)
    print("[ROBOT] Carrito y cupon verificado.")

def test_historial(qtbot):
    app = _crear_app()
    auth = _login(qtbot, "admin", "123", "Admin")
    ruta_ped = _temp_json({"pedidos": []})
    datos_prod = {"productos": [{"id":1,"titulo":"Libro Test","autor":"A","categoria":"C","precio":20.0,"portada":"","stock":5}]}
    ruta_prod = _temp_json(datos_prod)
    modelo_prod = ProductoModel(ruta_prod)
    pedido_model = PedidoModel(ruta_ped)
    carrito = Carrito()
    carrito.agregar_item("Libro Test", 20.0, 1)
    pedido_model.crear_pedido(auth.usuario_actual, carrito)
    vista_catalogo, _, _, _, _ = _setup_catalogo(qtbot, auth, datos_prod["productos"])
    assert len(pedido_model.pedidos) == 1
    assert pedido_model.pedidos[0]['cliente'] == auth.usuario_actual
    vista_catalogo.close()
    os.unlink(ruta_ped)
    os.unlink(ruta_prod)
    print("[ROBOT] Historial verificado (pedido creado).")
