"""
Módulo: carrito_model.py
Propósito: Modelo de carrito de compras y pedidos para Libros-Xpress.
Autor: [Robert Cerón - David Solís - Juan Castro]
Versión: 1.0.0
"""

from typing import List, Optional
import json
from datetime import date

class ItemCarrito:
    """Representa un producto en el carrito."""
    def __init__(self, titulo: str, precio: float, cantidad: int = 1):
        self.titulo = titulo
        self.precio = precio
        self.cantidad = cantidad

    def subtotal(self) -> float:
        """Calcula el subtotal del item."""
        return self.precio * self.cantidad

    def __repr__(self):
        return f"ItemCarrito({self.titulo}, cant={self.cantidad})"


class Carrito:
    """Gestiona la lista de items del carrito en memoria."""
    def __init__(self):
        self.items: List[ItemCarrito] = []

    def agregar_item(self, titulo: str, precio: float, cantidad: int = 1):
        """Agrega un producto o incrementa su cantidad si ya existe."""
        for item in self.items:
            if item.titulo == titulo:
                item.cantidad += cantidad
                return
        self.items.append(ItemCarrito(titulo, precio, cantidad))

    def eliminar_item(self, titulo: str):
        """Elimina un item del carrito por su título."""
        self.items = [item for item in self.items if item.titulo != titulo]

    def actualizar_cantidad(self, titulo: str, cantidad: int):
        """Cambia la cantidad de un item; si es 0 lo elimina."""
        if cantidad <= 0:
            self.eliminar_item(titulo)
            return
        for item in self.items:
            if item.titulo == titulo:
                item.cantidad = cantidad
                return

    def total(self) -> float:
        """Calcula el total del carrito (suma de subtotales)."""
        return sum(item.subtotal() for item in self.items)

    def impuesto(self, tasa: float = 0.13) -> float:
        """Calcula el impuesto sobre el total."""
        return round(self.total() * tasa, 2)

    def total_con_impuesto(self) -> float:
        """Total más impuesto."""
        return round(self.total() + self.impuesto(), 2)

    def vaciar(self):
        """Limpia el carrito."""
        self.items.clear()

    def esta_vacio(self) -> bool:
        return len(self.items) == 0


class PedidoModel:
    """
    Modelo para guardar y cargar pedidos desde data/pedidos.json.
    """
    def __init__(self, ruta_json: str = "data/pedidos.json"):
        self.ruta_json = ruta_json
        self.pedidos: List[dict] = []
        self.cargar_pedidos()

    def cargar_pedidos(self):
        """Carga los pedidos desde el JSON."""
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.pedidos = data.get('pedidos', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Advertencia: No se pudieron cargar pedidos. {e}")
            self.pedidos = []

    def guardar_pedidos(self):
        """Guarda la lista de pedidos en el JSON."""
        try:
            with open(self.ruta_json, 'w', encoding='utf-8') as f:
                json.dump({"pedidos": self.pedidos}, f, indent=4)
        except Exception as e:
            raise IOError(f"No se pudo guardar pedidos: {e}")

    def crear_pedido(self, cliente: str, carrito: Carrito) -> dict:
        """
        Crea un nuevo pedido a partir del carrito, lo guarda y retorna el pedido.
        """
        if carrito.esta_vacio():
            raise ValueError("El carrito está vacío.")
        pedido = {
            "id": len(self.pedidos) + 1,
            "fecha": str(date.today()),
            "cliente": cliente,
            "items": [{"titulo": item.titulo, "cantidad": item.cantidad, "precio_unitario": item.precio} for item in carrito.items],
            "total": carrito.total_con_impuesto()
        }
        self.pedidos.append(pedido)
        self.guardar_pedidos()
        return pedido

    def obtener_pedidos_cliente(self, cliente: str) -> List[dict]:
        """Retorna los pedidos de un cliente."""
        return [p for p in self.pedidos if p['cliente'] == cliente]


# --- Pruebas Unitarias (AAA) ---
if __name__ == "__main__":
    # Pruebas del Carrito (memoria)
    carrito = Carrito()
    # Arrange
    carrito.agregar_item("Libro A", 10.0, 2)
    carrito.agregar_item("Libro B", 15.0, 1)
    # Act
    total = carrito.total()
    imp = carrito.impuesto()
    total_imp = carrito.total_con_impuesto()
    # Assert
    assert total == 35.0, "El total debe ser 35.0"
    assert imp == 4.55, f"Impuesto esperado 4.55, obtenido {imp}"
    assert total_imp == 39.55, "Total con impuesto incorrecto"

    # Agregar existente
    carrito.agregar_item("Libro A", 10.0, 1)
    assert carrito.items[0].cantidad == 3, "La cantidad debe ser 3"

    # Eliminar
    carrito.eliminar_item("Libro B")
    assert len(carrito.items) == 1

    # Actualizar cantidad a 0 -> eliminar
    carrito.actualizar_cantidad("Libro A", 0)
    assert carrito.esta_vacio()

    # Pruebas de PedidoModel con archivo temporal
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        json.dump({"pedidos": []}, tmp)
        ruta_tmp = tmp.name

    pedido_model = PedidoModel(ruta_tmp)
    carrito2 = Carrito()
    carrito2.agregar_item("Libro X", 20.0, 2)
    # Crear pedido
    pedido = pedido_model.crear_pedido("admin", carrito2)
    assert pedido['id'] == 1
    assert pedido['total'] == 45.2  # 40 + 13% = 45.2

    # Ver persistencia recargando
    pedido_model2 = PedidoModel(ruta_tmp)
    assert len(pedido_model2.pedidos) == 1
    assert pedido_model2.obtener_pedidos_cliente("admin")[0]['id'] == 1

    os.unlink(ruta_tmp)
    print("✅ Pruebas unitarias del modelo de carrito pasaron correctamente.")