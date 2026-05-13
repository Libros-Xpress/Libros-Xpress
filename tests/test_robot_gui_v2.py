import sys, os, tempfile, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMessageBox
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

# ------------------------------------------------------------
# Bloqueo completo de ventanas emergentes (QMessageBox)
# ------------------------------------------------------------
_original_methods = {}

def _suppress_popups():
    """ Redirige todos los QMessageBox a la consola, devolviendo Ok/Yes para no bloquear. """
    global _original_methods
    if _original_methods:
        return  # ya suprimidos

    _original_methods = {
        'information': QMessageBox.information,
        'warning': QMessageBox.warning,
        'critical': QMessageBox.critical,
        'question': QMessageBox.question,
        'about': QMessageBox.about,
    }

    def _console_info(parent, title, text, *args, **kwargs):
        print(f"    [POPUP SUPRIMIDO - INFO] {title}: {text}")
        return QMessageBox.Ok

    def _console_warning(parent, title, text, *args, **kwargs):
        print(f"    [POPUP SUPRIMIDO - WARN] {title}: {text}")
        return QMessageBox.Ok

    def _console_critical(parent, title, text, *args, **kwargs):
        print(f"    [POPUP SUPRIMIDO - CRITICAL] {title}: {text}")
        return QMessageBox.Ok

    def _console_question(parent, title, text, *args, **kwargs):
        print(f"    [POPUP SUPRIMIDO - QUESTION] {title}: {text}")
        return QMessageBox.Yes

    def _console_about(parent, title, text):
        print(f"    [POPUP SUPRIMIDO - ABOUT] {title}: {text}")

    QMessageBox.information = staticmethod(_console_info)
    QMessageBox.warning = staticmethod(_console_warning)
    QMessageBox.critical = staticmethod(_console_critical)
    QMessageBox.question = staticmethod(_console_question)
    QMessageBox.about = staticmethod(_console_about)


def _restore_popups():
    """ Restaura los métodos originales de QMessageBox. """
    global _original_methods
    if _original_methods:
        QMessageBox.information = _original_methods['information']
        QMessageBox.warning = _original_methods['warning']
        QMessageBox.critical = _original_methods['critical']
        QMessageBox.question = _original_methods['question']
        QMessageBox.about = _original_methods['about']
        _original_methods = {}

# ------------------------------------------------------------
# Funciones auxiliares (lógica original funcional)
# ------------------------------------------------------------
def _crear_app():
    """Obtiene o crea la instancia de QApplication."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def _temp_json(datos):
    """Crea un archivo JSON temporal con los datos proporcionados y devuelve la ruta."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(datos, f)
        return f.name

def _login(qtbot, usuario, password, rol="Admin"):
    """
    Ejecuta el proceso de login con datos temporales.
    Retorna el AuthController y la ruta del archivo temporal de usuarios (se debe borrar luego).
    """
    print(f"\n>>> INICIANDO SESIÓN como {usuario} ({rol})")
    datos_usu = {"usuarios": [{"username": usuario, "password": password, "rol": rol}]}
    ruta = _temp_json(datos_usu)
    modelo = UsuarioModel(ruta)
    vista = LoginView()
    auth = AuthController(vista, modelo)

    # Silenciamos mensajes de la vista
    vista.mostrar_mensaje = lambda t, m: print(f"    [LOGIN] {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"    [LOGIN ERROR] {t}: {m}")

    qtbot.addWidget(vista)
    vista.show()
    time.sleep(2)   # espera a que se muestre

    print("    - Escribiendo usuario...")
    qtbot.keyClicks(vista.txt_usuario_login, usuario, delay=150)
    time.sleep(1)
    print("    - Escribiendo contraseña...")
    qtbot.keyClicks(vista.txt_password_login, password, delay=150)
    time.sleep(1)
    print("    - Haciendo clic en 'Entrar'...")
    qtbot.mouseClick(vista.btn_login, Qt.LeftButton)
    time.sleep(1.5)
    qtbot.waitUntil(lambda: not vista.isVisible(), timeout=5000)
    print("    ✓ Sesión iniciada correctamente.\n")
    return auth, ruta


def _setup_catalogo(qtbot, auth_ctrl, productos=None):
    """
    Crea y muestra el catálogo con datos temporales.
    Retorna la vista del catálogo, controlador del carrito, vista del carrito, y rutas temporales.
    """
    if productos is None:
        productos = [{"id":1,"titulo":"Libro Test","autor":"A","categoria":"C","precio":20.0,"portada":"","stock":5}]

    print("    - Creando catálogo temporal...")
    ruta_prod = _temp_json({"productos": productos})
    ruta_ped = _temp_json({"pedidos": []})
    modelo_prod = ProductoModel(ruta_prod)
    carrito = Carrito()
    pedido_model = PedidoModel(ruta_ped)

    vista_carrito = CarritoView()
    carrito_ctrl = CarritoController(vista_carrito, carrito, pedido_model, auth_ctrl.usuario_actual)

    # Silenciar mensajes del carrito
    vista_carrito.mostrar_mensaje = lambda t, m: print(f"    [CARRITO] {t}: {m}")
    vista_carrito.mostrar_error = lambda t, m: print(f"    [CARRITO ERROR] {t}: {m}")

    vista_catalogo = CatalogoView()
    catalogo_ctrl = CatalogoController(vista_catalogo, modelo_prod, carrito_ctrl,
                                    es_admin=(auth_ctrl.rol_actual == "Admin"),
                                    usuario_actual=auth_ctrl.usuario_actual)

    # Silenciar mensajes del catálogo
    vista_catalogo.mostrar_mensaje = lambda t, m: print(f"    [CATÁLOGO] {t}: {m}")
    vista_catalogo.mostrar_error = lambda t, m: print(f"    [CATÁLOGO ERROR] {t}: {m}")

    qtbot.addWidget(vista_catalogo)
    vista_catalogo.show()
    time.sleep(2)   # catálogo visible un momento

    return vista_catalogo, carrito_ctrl, vista_carrito, ruta_prod, ruta_ped


# ------------------------------------------------------------
# PRUEBAS (con cierre garantizado y supresión de popups)
# ------------------------------------------------------------
def test_flujo_admin(qtbot):
    _suppress_popups()
    try:
        print("\n" + "=" * 60)
        print("   PRUEBA 1: FLUJO COMPLETO DE ADMINISTRADOR")
        print("=" * 60)
        _crear_app()
        auth, ruta_usu = _login(qtbot, "admin", "123", "Admin")
        assert auth.usuario_actual == "admin"
        assert auth.rol_actual == "Admin"

        print(">>> Abriendo catálogo como Admin...")
        vista_catalogo, _, _, ruta_prod, ruta_ped = _setup_catalogo(qtbot, auth)
        time.sleep(1)

        print(">>> Verificando botones exclusivos de administrador...")
        assert vista_catalogo.btn_admin.isVisible()
        assert vista_catalogo.btn_venta_fisica.isVisible()
        print("    ✓ 'Panel Admin' y 'Venta Física' están visibles (solo Admin).\n")
        time.sleep(1)

        # Cierre limpio
        vista_catalogo.close()
        os.unlink(ruta_usu)
        os.unlink(ruta_prod)
        os.unlink(ruta_ped)
        QApplication.processEvents()
        print(">>> PRUEBA ADMIN COMPLETADA CON ÉXITO\n")
    finally:
        _restore_popups()


def test_flujo_cliente(qtbot):
    _suppress_popups()
    try:
        print("\n" + "=" * 60)
        print("   PRUEBA 2: FLUJO COMPLETO DE CLIENTE")
        print("=" * 60)
        _crear_app()
        auth, ruta_usu = _login(qtbot, "cliente", "abc", "Cliente")
        assert auth.rol_actual == "Cliente"

        print(">>> Abriendo catálogo como Cliente...")
        vista_catalogo, carrito_ctrl, vista_carrito, ruta_prod, ruta_ped = _setup_catalogo(qtbot, auth,
            [{"id":1,"titulo":"Libro Cliente","autor":"B","categoria":"D","precio":10.0,"portada":"","stock":3}])
        time.sleep(1)

        print(">>> Verificando que los botones de admin NO están visibles...")
        assert not vista_catalogo.btn_admin.isVisible()
        assert not vista_catalogo.btn_venta_fisica.isVisible()
        print("    ✓ Botones admin ocultos para Cliente.\n")

        print(">>> Agregando producto al carrito...")
        carrito_ctrl.agregar_al_carrito("Libro Cliente", 10.0)
        time.sleep(1)
        assert not carrito_ctrl.carrito.esta_vacio()
        print("    ✓ Producto agregado.\n")

        print(">>> Abriendo ventana del carrito...")
        vista_carrito.show()
        time.sleep(2)
        qtbot.waitUntil(lambda: vista_carrito.isVisible(), timeout=3000)
        assert vista_carrito.tabla.rowCount() == 1
        print("    ✓ El carrito muestra 1 producto.\n")
        time.sleep(1)

        # Cierre limpio
        vista_carrito.close()
        vista_catalogo.close()
        os.unlink(ruta_usu)
        os.unlink(ruta_prod)
        os.unlink(ruta_ped)
        QApplication.processEvents()
        print(">>> PRUEBA CLIENTE COMPLETADA CON ÉXITO\n")
    finally:
        _restore_popups()


def test_carrito_y_cupon(qtbot):
    _suppress_popups()
    try:
        print("\n" + "=" * 60)
        print("   PRUEBA 3: CARRITO Y APLICACIÓN DE CUPÓN")
        print("=" * 60)
        _crear_app()
        auth, ruta_usu = _login(qtbot, "admin", "123", "Admin")
        vista_catalogo, carrito_ctrl, vista_carrito, ruta_prod, ruta_ped = _setup_catalogo(qtbot, auth)

        print(">>> Agregando 2 unidades de 'Libro Test' al carrito...")
        carrito_ctrl.agregar_al_carrito("Libro Test", 20.0)
        time.sleep(0.7)
        carrito_ctrl.agregar_al_carrito("Libro Test", 20.0)
        time.sleep(0.7)

        print(">>> Abriendo carrito...")
        vista_carrito.show()
        time.sleep(2)

        print(">>> Escribiendo código promocional 'DESC10'...")
        vista_carrito.txt_cupon.setText("DESC10")
        time.sleep(1)

        print(">>> Aplicando cupón...")
        vista_carrito.btn_aplicar_cupon.clicked.emit()
        qtbot.waitUntil(lambda: vista_carrito.lbl_descuento.isVisible(), timeout=5000)
        time.sleep(1.5)

        assert "Descuento" in vista_carrito.lbl_descuento.text()
        total_final = float(vista_carrito.lbl_total.text().replace("Total: $",""))
        assert total_final < carrito_ctrl.carrito.total_con_impuesto()
        print(f"    ✓ Descuento aplicado (10%). Total final: ${total_final:.2f}\n")
        time.sleep(1)

        # Cierre limpio (también cerramos el catálogo)
        vista_carrito.close()
        vista_catalogo.close()
        os.unlink(ruta_usu)
        os.unlink(ruta_prod)
        os.unlink(ruta_ped)
        QApplication.processEvents()
        print(">>> PRUEBA CARRITO Y CUPÓN COMPLETADA CON ÉXITO\n")
    finally:
        _restore_popups()


def test_historial(qtbot):
    _suppress_popups()
    try:
        print("\n" + "=" * 60)
        print("   PRUEBA 4: CONSULTA DE HISTORIAL DE PEDIDOS")
        print("=" * 60)
        _crear_app()
        auth, ruta_usu = _login(qtbot, "admin", "123", "Admin")

        # Preparamos pedido manualmente ANTES de abrir el catálogo
        ruta_ped = _temp_json({"pedidos": []})
        ruta_prod = _temp_json({"productos": [{"id":1,"titulo":"Libro Test","autor":"A","categoria":"C","precio":20.0,"portada":"","stock":5}]})
        modelo_prod = ProductoModel(ruta_prod)
        carrito = Carrito()
        pedido_model = PedidoModel(ruta_ped)
        carrito.agregar_item("Libro Test", 20.0, 1)
        pedido_model.crear_pedido(auth.usuario_actual, carrito)
        print(">>> Pedido de prueba creado.")

        # Ahora abrimos catálogo (el historial se verificará a través del modelo)
        vista_catalogo, _, _, _, _ = _setup_catalogo(qtbot, auth,
            [{"id":1,"titulo":"Libro Test","autor":"A","categoria":"C","precio":20.0,"portada":"","stock":5}])
        time.sleep(1)

        assert len(pedido_model.pedidos) == 1
        assert pedido_model.pedidos[0]['cliente'] == auth.usuario_actual
        print("    ✓ El pedido aparece en el historial del usuario.\n")

        # Cierre limpio
        vista_catalogo.close()
        os.unlink(ruta_usu)
        os.unlink(ruta_ped)
        os.unlink(ruta_prod)
        QApplication.processEvents()
        print(">>> PRUEBA HISTORIAL COMPLETADA CON ÉXITO\n")
    finally:
        _restore_popups()
