"""
Módulo: cupon_model.py
Propósito: Carga y validación de cupones de descuento para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

import json
from typing import Optional, Dict, Any

class CuponModel:
    """
    Modelo para gestionar los cupones de descuento desde data/cupones.json.
    """

    def __init__(self, ruta_json: str = "data/cupones.json"):
        """
        Args:
            ruta_json (str): Ruta al archivo JSON de cupones.
        """
        self.ruta_json = ruta_json
        self.cupones = []
        self.cargar_cupones()

    def cargar_cupones(self):
        """Carga la lista de cupones desde el archivo JSON."""
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cupones = data.get('cupones', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar cupones: {e}")
            self.cupones = []

    def validar_cupon(self, codigo: str) -> Optional[Dict[str, Any]]:
        """
        Busca un cupón por su código y retorna sus datos si está activo.

        Args:
            codigo (str): Código del cupón a validar.

        Returns:
            Optional[Dict]: Diccionario con los datos del cupón o None si no es válido.
        """
        for cupon in self.cupones:
            if cupon['codigo'].upper() == codigo.upper() and cupon.get('activo', True):
                return cupon
        return None

    def aplicar_descuento(self, cupon: Dict[str, Any], total: float) -> float:
        """
        Aplica el descuento del cupón al total.

        Args:
            cupon (dict): Datos del cupón (debe tener 'tipo' y 'valor').
            total (float): Total actual sobre el cual aplicar el descuento.

        Returns:
            float: Total después del descuento.
        """
        tipo = cupon.get('tipo', 'fijo')
        valor = cupon.get('valor', 0)
        if tipo == 'porcentaje':
            descuento = total * (valor / 100)
        else:  # fijo
            descuento = valor
        nuevo_total = max(0, total - descuento)
        return round(nuevo_total, 2)


# --- Pruebas Unitarias (AAA) ---
if __name__ == "__main__":
    import tempfile, os

    # Arrange
    datos = {"cupones": [
        {"codigo": "DESC10", "tipo": "porcentaje", "valor": 10, "activo": True},
        {"codigo": "FIJO5", "tipo": "fijo", "valor": 5, "activo": True},
        {"codigo": "CADUCADO", "tipo": "porcentaje", "valor": 20, "activo": False}
    ]}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump(datos, tmp)
        ruta_tmp = tmp.name

    modelo = CuponModel(ruta_tmp)

    # Act
    cupon_valido = modelo.validar_cupon("DESC10")
    cupon_fijo = modelo.validar_cupon("fijo5")  # debe ignorar mayúsculas
    cupon_inactivo = modelo.validar_cupon("CADUCADO")
    cupon_inexistente = modelo.validar_cupon("NOEXISTE")

    # Assert
    assert cupon_valido is not None
    assert cupon_fijo is not None
    assert cupon_inactivo is None
    assert cupon_inexistente is None

    # Act - aplicar descuentos
    total1 = modelo.aplicar_descuento(cupon_valido, 100.0)  # 10% -> 90.0
    total2 = modelo.aplicar_descuento(cupon_fijo, 100.0)   # 5 fijo -> 95.0

    assert total1 == 90.0, "Descuento porcentual incorrecto"
    assert total2 == 95.0, "Descuento fijo incorrecto"

    os.unlink(ruta_tmp)
    print("✅ Pruebas unitarias del modelo de cupones pasaron correctamente.")