"""
Módulo: auth_controller.py
Propósito: Controlador de autenticación (login, registro) para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from PySide6.QtWidgets import QMessageBox
from src.models.usuario_model import UsuarioModel
from src.views.login_view import LoginView

class AuthController:
    """
    Controlador de autenticación. Conecta la vista de login con el modelo de usuarios.
    """

    def __init__(self, vista: LoginView, modelo: UsuarioModel):
        """
        Args:
            vista (LoginView): Instancia de la vista de login.
            modelo (UsuarioModel): Instancia del modelo de usuarios.
        """
        self.vista = vista
        self.modelo = modelo
        self._configurar_senales()

    def _configurar_senales(self):
        """Conecta los botones de la vista con los métodos del controlador."""
        self.vista.btn_login.clicked.connect(self.iniciar_sesion)
        self.vista.btn_registrar.clicked.connect(self.registrar_usuario)
        self.vista.btn_ir_registro.clicked.connect(self.vista.mostrar_registro)
        self.vista.btn_ir_login.clicked.connect(self.vista.mostrar_login)
        self.vista.btn_recuperar.clicked.connect(self.recuperar_contrasena)
        # También permitir iniciar sesión al presionar Enter en campos de login
        self.vista.txt_usuario_login.returnPressed.connect(self.iniciar_sesion)
        self.vista.txt_password_login.returnPressed.connect(self.iniciar_sesion)
        # Y en registro, Enter en confirmación dispara registro
        self.vista.txt_password_confirm.returnPressed.connect(self.registrar_usuario)

    def _validar_campos_vacios(self, *campos):
        """Retorna True si algún campo está vacío."""
        for campo in campos:
            if not campo:
                return True
        return False

    def iniciar_sesion(self):
        """Lógica de inicio de sesión."""
        usuario, password = self.vista.obtener_datos_login()
        if self._validar_campos_vacios(usuario, password):
            self.vista.mostrar_error("Campos incompletos", "Usuario y contraseña son obligatorios.")
            return

        autenticado = self.modelo.autenticar(usuario, password)
        if autenticado:
            self.vista.mostrar_mensaje("Acceso correcto", f"Bienvenido {autenticado.username} ({autenticado.rol})")
            self.vista.cerrar_ventana()  # La app continuará con el catálogo
        else:
            self.vista.mostrar_error("Error de autenticación", "Usuario o contraseña incorrectos.")
            self.vista.limpiar_login()

    def registrar_usuario(self):
        """Lógica de registro de nuevo usuario."""
        usuario, password, confirm, rol = self.vista.obtener_datos_registro()
        if self._validar_campos_vacios(usuario, password, confirm):
            self.vista.mostrar_error("Campos incompletos", "Todos los campos son obligatorios.")
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
        """Muestra un mensaje de recuperación (no implementada)."""
        self.vista.mostrar_mensaje("Recuperar contraseña",
                                "Contacta al administrador para restablecer tu contraseña.")


# --- Prueba del controlador (simulación) ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    import tempfile
    import json
    import os

    # Arrange
    datos = {"usuarios": [{"username": "admin", "password": "123", "rol": "Admin"}]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    app = QApplication(sys.argv)
    vista = LoginView()
    modelo = UsuarioModel(ruta_tmp)
    controlador = AuthController(vista, modelo)

    # Act - simular login con credenciales correctas
    vista.txt_usuario_login.setText("admin")
    vista.txt_password_login.setText("123")
    # Simular clic en botón login
    vista.btn_login.click()  # Debería mostrar mensaje de bienvenida y cerrar la ventana

    # Assert básica: no explotó, y la ventana se cerró
    assert not vista.isVisible(), "La ventana debió cerrarse tras login exitoso."
    print("✅ Prueba del controlador de autenticación pasó correctamente.")

    os.unlink(ruta_tmp)
    # Cerrar aplicación residual
    app.quit()