import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.views.splash_view import SplashView
from src.views.admin_productos_view import AdminProductosView
from src.views.historial_view import HistorialView
from src.views.venta_fisica_view import VentaFisicaView

app = QApplication.instance() or QApplication(sys.argv)

def test_splash_view():
    splash = SplashView()
    assert splash is not None
    splash.close()

def test_admin_productos_view():
    vista = AdminProductosView()
    assert vista is not None
    vista.close()

def test_historial_view():
    vista = HistorialView()
    assert vista is not None
    vista.close()

def test_venta_fisica_view():
    vista = VentaFisicaView()
    assert vista is not None
    vista.close()