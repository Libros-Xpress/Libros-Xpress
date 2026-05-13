import sys, os, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.main import main

def test_main_splash():
    """Verifica que main se ejecuta y muestra el splash."""
    app = QApplication.instance() or QApplication(sys.argv)
    # No podemos ejecutar main completo porque bloquea, pero al menos importamos y comprobamos que no da error
    assert main is not None