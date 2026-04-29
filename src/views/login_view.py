"""
Módulo: login_view.py
Propósito: Interfaz gráfica de autenticación (login y registro) para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LoginView(QMainWindow):
    """
    Ventana de autenticación (login/registro).
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Libros-Xpress - Acceso")
        self.setFixedSize(420, 320)
        self._configurar_ui()
        self._centrar_en_pantalla()

    def _centrar_en_pantalla(self):
        """Centra la ventana en la pantalla."""
        centro = self.screen().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centro)
        self.move(frame.topLeft())

    def _configurar_ui(self):
        """Construye los formularios de login y registro dentro de un QStackedWidget."""
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QVBoxLayout(central)

        self.stacked = QStackedWidget()
        layout_principal.addWidget(self.stacked)

        # ---- Página 0: Login ----
        pagina_login = QWidget()
        layout_login = QVBoxLayout(pagina_login)
        layout_login.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo_login = QLabel("Iniciar Sesión")
        titulo_login.setFont(QFont("Arial", 16, QFont.Bold))
        titulo_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_login.addWidget(titulo_login)

        layout_login.addWidget(QLabel("Usuario:"))
        self.txt_usuario_login = QLineEdit()
        self.txt_usuario_login.setPlaceholderText("Nombre de usuario")
        layout_login.addWidget(self.txt_usuario_login)

        layout_login.addWidget(QLabel("Contraseña:"))
        self.txt_password_login = QLineEdit()
        self.txt_password_login.setPlaceholderText("Contraseña")
        self.txt_password_login.setEchoMode(QLineEdit.EchoMode.Password)
        layout_login.addWidget(self.txt_password_login)

        self.btn_login = QPushButton("Entrar")
        layout_login.addWidget(self.btn_login)

        self.btn_ir_registro = QPushButton("¿No tienes cuenta? Regístrate aquí")
        self.btn_ir_registro.setFlat(True)
        self.btn_ir_registro.setStyleSheet("color: #0078d4; text-decoration: underline;")
        layout_login.addWidget(self.btn_ir_registro)

        self.btn_recuperar = QPushButton("¿Olvidaste tu contraseña?")
        self.btn_recuperar.setFlat(True)
        self.btn_recuperar.setStyleSheet("color: #666;")
        layout_login.addWidget(self.btn_recuperar)

        # ---- Página 1: Registro ----
        pagina_registro = QWidget()
        layout_registro = QVBoxLayout(pagina_registro)
        layout_registro.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo_registro = QLabel("Crear Cuenta Nueva")
        titulo_registro.setFont(QFont("Arial", 16, QFont.Bold))
        titulo_registro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_registro.addWidget(titulo_registro)

        layout_registro.addWidget(QLabel("Usuario:"))
        self.txt_usuario_reg = QLineEdit()
        self.txt_usuario_reg.setPlaceholderText("Elige un nombre de usuario")
        layout_registro.addWidget(self.txt_usuario_reg)

        layout_registro.addWidget(QLabel("Contraseña:"))
        self.txt_password_reg = QLineEdit()
        self.txt_password_reg.setPlaceholderText("Contraseña")
        self.txt_password_reg.setEchoMode(QLineEdit.EchoMode.Password)
        layout_registro.addWidget(self.txt_password_reg)

        layout_registro.addWidget(QLabel("Confirmar contraseña:"))
        self.txt_password_confirm = QLineEdit()
        self.txt_password_confirm.setPlaceholderText("Repite la contraseña")
        self.txt_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        layout_registro.addWidget(self.txt_password_confirm)

        layout_registro.addWidget(QLabel("Rol:"))
        self.cmb_rol = QComboBox()
        self.cmb_rol.addItems(["Cliente", "Admin"])  # Para simplicidad, ambos disponibles
        layout_registro.addWidget(self.cmb_rol)

        self.btn_registrar = QPushButton("Crear Cuenta")
        layout_registro.addWidget(self.btn_registrar)

        self.btn_ir_login = QPushButton("¿Ya tienes cuenta? Inicia sesión")
        self.btn_ir_login.setFlat(True)
        self.btn_ir_login.setStyleSheet("color: #0078d4; text-decoration: underline;")
        layout_registro.addWidget(self.btn_ir_login)

        # Añadir páginas al stacked
        self.stacked.addWidget(pagina_login)    # índice 0
        self.stacked.addWidget(pagina_registro) # índice 1

        # Estilos generales
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QLabel { font-size: 13px; }
            QPushButton {
                background-color: #0078d4; color: white;
                border: none; padding: 8px; border-radius: 4px;
            }
            QPushButton:hover { background-color: #005a9e; }
            QPushButton[flat="true"] { background-color: transparent; color: #0078d4; text-decoration: underline; }
            QLineEdit { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
            QComboBox { padding: 6px; border: 1px solid #ccc; border-radius: 4px; }
        """)

    # --- Métodos de acceso a datos de los campos ---
    def obtener_datos_login(self):
        """Retorna (usuario, password) del formulario de login."""
        return (self.txt_usuario_login.text().strip(),
                self.txt_password_login.text().strip())

    def obtener_datos_registro(self):
        """Retorna (usuario, password, confirm, rol) del formulario de registro."""
        return (self.txt_usuario_reg.text().strip(),
                self.txt_password_reg.text().strip(),
                self.txt_password_confirm.text().strip(),
                self.cmb_rol.currentText())

    def limpiar_login(self):
        """Limpia los campos de login."""
        self.txt_usuario_login.clear()
        self.txt_password_login.clear()

    def limpiar_registro(self):
        """Limpia los campos de registro."""
        self.txt_usuario_reg.clear()
        self.txt_password_reg.clear()
        self.txt_password_confirm.clear()

    # --- Navegación entre páginas ---
    def mostrar_login(self):
        self.stacked.setCurrentIndex(0)

    def mostrar_registro(self):
        self.stacked.setCurrentIndex(1)

    # --- Mensajes al usuario ---
    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        QMessageBox.critical(self, titulo, mensaje)

    def cerrar_ventana(self):
        self.close()


# --- Prueba visual de la vista ---
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ventana = LoginView()
    ventana.show()
    sys.exit(app.exec())
