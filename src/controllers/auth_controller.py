"""
Módulo: auth_controller.py
Propósito: Controlador de autenticación adaptado al QDialog (Login/Registro) con recuperación simulada.
Autor: Robert Cerón - David Solís - Juan Castro
Versión: 2.0.0 - Fase 2 (Login / Registro)
"""

import sys, os
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import QApplication, QInputDialog
from src.models.usuario_model import UsuarioModel
from src.views.login_view import LoginView

class AuthController:
    """Controlador de autenticación que conecta la vista de login (QDialog) con el modelo de usuarios."""

    def __init__(self, vista: LoginView, modelo: UsuarioModel):
        self.vista = vista
        self.modelo = modelo
        self.usuario_actual = None
        self.rol_actual = None
        self._configurar_senales()

    def _configurar_senales(self):
        self.vista.btn_login.clicked.connect(self.iniciar_sesion)
        self.vista.btn_registrar.clicked.connect(self.registrar_usuario)
        self.vista.btn_ir_registro.clicked.connect(self.vista.mostrar_registro)
        self.vista.btn_ir_login.clicked.connect(self.vista.mostrar_login)
        self.vista.btn_recuperar.clicked.connect(self.recuperar_contrasena)
        self.vista.txt_usuario_login.returnPressed.connect(self.iniciar_sesion)
        self.vista.txt_password_login.returnPressed.connect(self.iniciar_sesion)
        self.vista.txt_password_confirm.returnPressed.connect(self.registrar_usuario)

    def _validar_campos_vacios(self, *campos):
        return any(not c for c in campos)

    def iniciar_sesion(self):
        usuario, password = self.vista.obtener_datos_login()
        if self._validar_campos_vacios(usuario, password):
            self.vista.mostrar_error("Campos incompletos", "Usuario y contraseña son obligatorios.")
            return

        autenticado = self.modelo.autenticar(usuario, password)
        if autenticado:
            self.usuario_actual = autenticado.username
            self.rol_actual = autenticado.rol
            self.vista.mostrar_mensaje("Acceso correcto", f"Bienvenido {autenticado.username} ({autenticado.rol})")
            self.vista.accept()   # <-- Cierra el diálogo con resultado Aceptado
        else:
            self.vista.mostrar_error("Error de autenticación", "Usuario o contraseña incorrectos.")
            self.vista.limpiar_login()

    def registrar_usuario(self):
        usuario, password, confirm, rol, email = self.vista.obtener_datos_registro()
        if self._validar_campos_vacios(usuario, password, confirm, email):
            self.vista.mostrar_error("Campos incompletos", "Todos los campos (incluido el correo) son obligatorios.")
            return
        if password != confirm:
            self.vista.mostrar_error("Contraseñas no coinciden", "Las contraseñas ingresadas no son iguales.")
            return
        if len(password) < 3:
            self.vista.mostrar_error("Contraseña insegura", "La contraseña debe tener al menos 3 caracteres.")
            return

        try:
            exito = self.modelo.registrar(usuario, password, rol)
            if exito:
                self.vista.mostrar_mensaje("Registro exitoso", "Cuenta creada. Ahora puedes iniciar sesión.")
                self.vista.limpiar_registro()
                self.vista.mostrar_login()
            else:
                self.vista.mostrar_error("Usuario existente", "El nombre de usuario ya está en uso. Elige otro.")
        except IOError as e:
            self.vista.mostrar_error("Error de archivo", str(e))

    def recuperar_contrasena(self):
        email, ok = QInputDialog.getText(self.vista, "Recuperar contraseña",
                                         "Introduce el correo electrónico registrado:")
        if ok and email:
            self.vista.mostrar_mensaje("Recuperación",
                                       f"Se ha enviado un enlace de recuperación a {email}.\n"
                                       "Revisa tu bandeja de entrada para restablecer tu contraseña.")
        elif ok:
            self.vista.mostrar_error("Campo vacío", "Debes ingresar un correo electrónico.")


# --- Prueba del controlador (adaptada al QDialog y nuevo campo email) ---
if __name__ == "__main__":
    import sys, tempfile, json, os
    from PySide6.QtWidgets import QApplication

    # Arrange
    datos = {"usuarios": [{"username": "admin", "password": "123", "rol": "Admin"}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    app = QApplication(sys.argv)
    vista = LoginView()
    vista.show()

    # Mock de mensajes
    vista.mostrar_mensaje = lambda t, m: print(f"i {t}: {m}")
    vista.mostrar_error = lambda t, m: print(f"x {t}: {m}")

    modelo = UsuarioModel(ruta_tmp)
    controlador = AuthController(vista, modelo)

    # Act - simular login con credenciales correctas
    vista.txt_usuario_login.setText("admin")
    vista.txt_password_login.setText("123")
    vista.btn_login.clicked.emit()
    app.processEvents()

    # Assert
    assert not vista.isVisible(), "La ventana debió cerrarse tras login exitoso."
    print("Prueba del controlador de autenticación (v2.0.0) pasó correctamente.")

    os.unlink(ruta_tmp)
    vista.close()
    app.quit()
    sys.exit()