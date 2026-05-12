"""
Módulo: login_view.py
Propósito: Diálogo de autenticación (login y registro) con diseño decorativo.
Autor: David Solís
Versión: 2.0.0 – Fase 2 (Login / Registro)
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QStackedWidget, QMessageBox, QComboBox, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LoginView(QDialog):
    """Ventana de acceso (QDialog) con diseño de la paleta Digital-Shift."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Libros/Xpress – Acceso")
        self.setFixedSize(480, 480)
        self._configurar_ui()
        self._aplicar_estilos()
        self._centrar_en_pantalla()

    def _centrar_en_pantalla(self):
        centro = self.screen().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centro)
        self.move(frame.topLeft())

    def _configurar_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(10)


        # Título principal
        lbl_titulo = QLabel("LIBROS/XPRESS")
        lbl_titulo.setFont(QFont("Segoe UI", 32, QFont.Bold))
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        # Separador decorativo
        separador = QLabel("━━━━━━━━━━━━━━━━━━━━")
        separador.setFont(QFont("Segoe UI", 8))
        separador.setAlignment(Qt.AlignCenter)
        separador.setStyleSheet("color: #D4A574;")
        layout.addWidget(separador)

        self.stacked = QStackedWidget()
        layout.addWidget(self.stacked)

        # ================= PÁGINA 0: LOGIN =================
        pagina_login = QWidget()
        login_layout = QVBoxLayout(pagina_login)
        login_layout.setSpacing(8)

        login_layout.addWidget(QLabel("Usuario"))
        self.txt_usuario_login = QLineEdit()
        self.txt_usuario_login.setPlaceholderText("Nombre de usuario")
        login_layout.addWidget(self.txt_usuario_login)

        login_layout.addWidget(QLabel("Contraseña"))
        self.txt_password_login = QLineEdit()
        self.txt_password_login.setPlaceholderText("Contraseña")
        self.txt_password_login.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.txt_password_login)

        self.btn_login = QPushButton("Entrar")
        login_layout.addWidget(self.btn_login)

        self.btn_ir_registro = QPushButton("¿No tienes cuenta? Regístrate")
        self.btn_ir_registro.setFlat(True)
        login_layout.addWidget(self.btn_ir_registro)

        self.btn_recuperar = QPushButton("¿Olvidaste tu contraseña?")
        self.btn_recuperar.setFlat(True)
        login_layout.addWidget(self.btn_recuperar)

        self.stacked.addWidget(pagina_login)  # índice 0

        # ================= PÁGINA 1: REGISTRO =================
        pagina_registro = QWidget()
        reg_layout = QVBoxLayout(pagina_registro)
        reg_layout.setSpacing(6)

        reg_layout.addWidget(QLabel("Usuario"))
        self.txt_usuario_reg = QLineEdit()
        self.txt_usuario_reg.setPlaceholderText("Elige un nombre de usuario")
        reg_layout.addWidget(self.txt_usuario_reg)

        reg_layout.addWidget(QLabel("Correo electrónico"))
        self.txt_email_reg = QLineEdit()
        self.txt_email_reg.setPlaceholderText("ejemplo@correo.com")
        reg_layout.addWidget(self.txt_email_reg)

        reg_layout.addWidget(QLabel("Contraseña"))
        self.txt_password_reg = QLineEdit()
        self.txt_password_reg.setPlaceholderText("Contraseña")
        self.txt_password_reg.setEchoMode(QLineEdit.Password)
        reg_layout.addWidget(self.txt_password_reg)

        reg_layout.addWidget(QLabel("Confirmar contraseña"))
        self.txt_password_confirm = QLineEdit()
        self.txt_password_confirm.setPlaceholderText("Repite la contraseña")
        self.txt_password_confirm.setEchoMode(QLineEdit.Password)
        reg_layout.addWidget(self.txt_password_confirm)

        reg_layout.addWidget(QLabel("Rol"))
        self.cmb_rol = QComboBox()
        self.cmb_rol.addItems(["Cliente", "Admin"])
        reg_layout.addWidget(self.cmb_rol)

        self.btn_registrar = QPushButton("Crear cuenta")
        reg_layout.addWidget(self.btn_registrar)

        self.btn_ir_login = QPushButton("¿Ya tienes cuenta? Inicia sesión")
        self.btn_ir_login.setFlat(True)
        reg_layout.addWidget(self.btn_ir_login)

        self.stacked.addWidget(pagina_registro)  # índice 1

    def _aplicar_estilos(self):
        self.setStyleSheet("""
            QDialog { background-color: #FFF8F0; }
            QLabel { color: #5D4037; font-size: 13px; font-weight: bold; }
            QLineEdit {
                padding: 10px; border: 1px solid #D4A574; border-radius: 6px;
                background-color: #FFFAF5; color: #3E2723; font-size: 13px;
            }
            QPushButton {
                background-color: #8B5E3C; color: white; padding: 10px;
                border: none; border-radius: 6px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #6B3A2A; }
            QPushButton[flat="true"] {
                background: transparent; color: #8B5E3C; text-decoration: underline;
                font-weight: normal; padding: 5px;
            }
            QComboBox {
                padding: 8px; border: 1px solid #D4A574; border-radius: 6px;
                background-color: #FFFAF5; color: #3E2723; font-size: 13px;
            }
        """)

    # Métodos de acceso a datos
    def obtener_datos_login(self):
        return (self.txt_usuario_login.text().strip(),
                self.txt_password_login.text().strip())

    def obtener_datos_registro(self):
        return (self.txt_usuario_reg.text().strip(),
                self.txt_password_reg.text().strip(),
                self.txt_password_confirm.text().strip(),
                self.cmb_rol.currentText(),
                self.txt_email_reg.text().strip())

    def limpiar_login(self):
        self.txt_usuario_login.clear()
        self.txt_password_login.clear()

    def limpiar_registro(self):
        self.txt_usuario_reg.clear()
        self.txt_email_reg.clear()
        self.txt_password_reg.clear()
        self.txt_password_confirm.clear()

    def mostrar_login(self):
        self.stacked.setCurrentIndex(0)

    def mostrar_registro(self):
        self.stacked.setCurrentIndex(1)

    def mostrar_mensaje(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, titulo, mensaje):
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