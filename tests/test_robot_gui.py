import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.views.login_view import LoginView

def test_robot_interfaz_login(qtbot):
    app = QApplication.instance() or QApplication(sys.argv)
    vista = LoginView()
    qtbot.addWidget(vista)
    vista.show()

    assert vista.isVisible()
    qtbot.keyClicks(vista.txt_usuario_login, "admin")
    qtbot.keyClicks(vista.txt_password_login, "123")

    assert vista.txt_usuario_login.text() == "admin"
    assert vista.txt_password_login.text() == "123"

    print("[ROBOT] Interacción con la GUI verificada exitosamente.")
    vista.close()
